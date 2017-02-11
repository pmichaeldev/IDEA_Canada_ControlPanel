from flask import Flask, Blueprint, request, abort, render_template
import datetime
from ..models import Orders, Customers, Products, ORDER_STATUS_ON_RESERVE
from ..database import db
from ..utils import normalize

order_form = Blueprint('order', __name__, template_folder='../templates', static_folder='static')
required_fields = ['first_name', 'last_name', 'email', 'product_id', 'street', 'postal_code', 'town', 'phone']

@order_form.route('/order', methods=['GET', 'POST'])
def show():
    params = dict(title_name='Order Form')
    if request.method == 'POST':
        params = set_params(params, request)
        if is_valid_order(request):
            date = datetime.datetime.utcnow()
            product_id = request.form['product_id']
            comments = request.form['comments']    
            email = request.form['email'] 
            customer_id = None
            prod_exists = None
            customer_obj = get_customer_if_exists(email)
                    # check if customer already exists
            if product_id:
               prod_exists = product_exists(product_id)
            if customer_obj:
                # if it does then find his id and link to the order
                customer_id = customer_obj.id
            else:
                # if not then add the customer to the database first. 
                first_name = request.form['first_name']
                last_name = request.form['last_name']
                street = request.form['street']
                postal_code = request.form['postal_code']
                town = request.form['town']
                phone = request.form['phone']
                new_customer = Customers(first_name, last_name, email, street, postal_code, town, phone)
                db.session.add(new_customer) 
                db.session.commit()
                customer_id = new_customer.id
            # do a final check to see if the customer exists
            if customer_id is None or prod_exists is None:
                params['error'] = "That product doesn't exist"
                return render_template('order_form.html',**params)
            # add the order to the database and link the customer
            new_order = Orders(ORDER_STATUS_ON_RESERVE, date, comments, customer_id, product_id)
            db.session.add(new_order)
            db.session.commit()
            return render_template('thanks.html')
        else: # the order is not valid
            return render_template('order_form.html',**params)
    else:
        return render_template('order_form.html',**params)

def is_valid_order(request):
    """ Basic check to see if the fields is empty """
    is_valid = True
    for field in required_fields:
        if not request.form[field]:
            return False
        return True

def get_customer_if_exists(email):
    email = normalize(email)
    customer = Customers.query.filter_by(email=email).first()
    if customer is None:
        return False
    return customer 

def product_exists(prod_id):
    prod_id = int(prod_id)
    prod = Products.query.get(prod_id)
    return prod
     
def set_params(params, request):
    for field in required_fields:
        params[field] = request.form[field]
    return params
