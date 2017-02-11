from flask import Flask, Blueprint, render_template, url_for, request, session, redirect
from ..models import tables
from ..restrictions import * 
from login import logged_in

help_page = Blueprint('help', __name__, template_folder='../templates')

@help_page.route('/help')
def show():
    if not logged_in():
	    return redirect(url_for('login.show'))
    role = get_role(session['email'])
    tables = get_tables(role)
    params = dict(title_name='Help', tables=tables)
    return render_template('help.html', **params)


