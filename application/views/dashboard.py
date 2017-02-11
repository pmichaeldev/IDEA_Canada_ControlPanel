from flask import Flask, Blueprint, render_template, url_for, request, session, redirect
from login import logged_in
from ..models import tables, History, Orders, Employees, Products, Customers, ORDER_STATUS_ON_RESERVE 
from ..restrictions import * 
dashboard_page = Blueprint('dashboard', __name__, template_folder='../templates')

@dashboard_page.route('/dashboard')
def show():
    if logged_in():
        # Get the reserve data, and any data needed to populate the dashboard
        # and pass in into the params
        reserve = get_orders_on_reserve()
        role = get_role(session['email'])
        tables = get_tables(role)
        columns = reserve['columns']
        history = get_history(limit=5)
        params = dict(title_name='Dashboard', tables=tables, reserve = reserve['rows'], columns=columns, history=history)
        return render_template('dashboard.html', **params)
    else:
        return redirect(url_for('login.show'))

def get_orders_on_reserve():
    reserve = {}
    orders = []
    objs = Orders.query.filter_by(status=ORDER_STATUS_ON_RESERVE).all()
    for obj in objs:
        order = {}
        customer = get_customer_by_id(obj.customer_id)
        product = get_product_by_id(obj.product_id)
        order['name'] = customer.firstname.capitalize() + " " + customer.lastname.capitalize() 
        order['product'] = product.product_name
        order['phone'] = customer.phone
        order['comments'] = obj.comments
        orders.append(order)
    reserve['columns'] = map(lambda x: x.capitalize(), ['phone', 'product', 'name', 'comments'])
    reserve['rows'] = orders
    return reserve 


def get_customer_by_id(id):
    return Customers.query.get(id)

def get_product_by_id(id):
    return Products.query.get(id)

def get_employee_by_id(id):
    return Employees.query.get(id)

def get_history(limit=5):
    history = History.query.order_by(History.date.desc()).limit(limit).all()
    history_list = []
    for h in history:
        emp = get_employee_by_id(h.employee_id)
        if h.operation == "delete":
            string = emp.name.capitalize() + " " +  h.operation + "d a record on the " + h.table + " table at " + h.date  
        elif h.operation != "delete":
            string = emp.name.capitalize() + " " +  h.operation + "ed a record on the " + h.table + " table at " + h.date 
        history_list.append(string) 
    return history_list



