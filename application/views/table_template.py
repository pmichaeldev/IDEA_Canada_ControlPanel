from flask import Flask, Blueprint, render_template, url_for, request, session, redirect, abort
from .. import utils
from ..models import * 
from login import logged_in
import datetime
from ..restrictions import *

table_template_page= Blueprint('table_template', __name__, template_folder='../templates', static_folder='static')

methods = {'add': '#add-op',
'delete': '#delete-op',
'edit': '#edit-op',
'import': '#import-op',
'export': '#export-op'
}

@table_template_page.route('/data/<table>', methods=['GET', 'POST'])
def show(table):
    if request.method == 'GET':
        if logged_in():
            email = session['email']
            role = get_role(email)
            tables = get_tables(role)
            if table not in tables:
                return redirect(url_for('dashboard.show'))
            else:
                # get table and the data
                return get(tables, table, role, request)
        else:
            return redirect(url_for('login.show'))
    elif request.method == 'POST':
        return post(table, request)

@table_template_page.route('/data', methods=['GET', 'POST'])
def index():
    if logged_in():
        return redirect(url_for('dashboard.show'))
    else:
        return redirect(url_for('login.show'))

# Get the data for this table
def get(access_tables, table, role, request):
    # all of these params can be cached
    # every request = a database hit = not good
    params = dict(table_name=tables[table]['table_name'], title_name=tables[table]['table_name']);
    params['columns'] = get_columns(table) 
    print params['columns']
    params['forms'] = get_forms(table, params['columns'])
    params['tables'] = access_tables 
    params['operations'] = get_operations(role, table) 
    params['export_files'] = EXPORT_FILETYPES 
    params['css_icons'] = CSS_ICON_CLASS
    params['payload'] = query_table(table)
    print params
    return render_template("table_template.html", **params)

# Post data from the request to the database
def post(table, request):
    if session['email']:
        columns = get_columns(table);
        table = table_from_string(table)
        json = request.json
        method = json['method']
        response = None
        del json['method']
        print json
        if method == methods['add']:
            add = table(**json)
            db.session.add(add)
            db.session.commit()
            response = to_json(add)
        elif method == methods['edit']:
            edit = table.query.get(json['id'])
            if table.__tablename__ == Orders.__tablename__:
                json['date'] =  get_current_time()
            for col in columns:
                edit.__setattr__(col, json[col])
            response = to_json(edit)
            db.session.commit()
        elif method == methods['delete']:
            delete  = table.query.filter_by(id=json['id']).first()
            db.session.delete(delete)
            db.session.commit()
            response = to_json(delete)
        elif method == methods['import']:
            pass
        elif method == methods['export']:
            pass
        # log history
        # log name, opertion, and data
        e_id = employee_id_from_email(session['email'])
        h = History(operation=method.split("-")[0][1:], employee_id = e_id, table=table.__tablename__,
                date=get_current_time())
        db.session.add(h)
        db.session.commit()
        return response
    else:
        abort(400)
    

def import_file(table, request):
    pass

def export_file(table, request):
    pass

def query_table(table):
    table = table_from_string(table)
    if table == Employees:
        cols = [Employees.id, Employees.name, Employees.phone, Employees.email, Employees.restriction]
        results = table.query.with_entities(*cols)
    else:
        results = table.query.all()
    return results

def get_forms(table, cols):
    table = table_from_string(table)
    forms = []
    cols = list(set(cols) - set(filtered_cols())) 
    print cols 
    for col in cols:        
        form = {}
        form['label'] = col.capitalize()
        form['type'] = "text" 
        form['name'] = col
        forms.append(form)
    return forms

def employee_id_from_email(email):
    email = utils.normalize(email)
    employee = Employees.query.filter_by(email=email).first()
    return employee.id

def get_current_time():
   return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

