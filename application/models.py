from flask import Flask
import json
from flask.ext.sqlalchemy import SQLAlchemy
from database import db

ORDER_STATUS_ON_RESERVE = "ON_RESERVE"
ORDER_STATUS_PROCESSED = "PROCESSED" 
ORDER_STATUS_IN_PROGRESS = "IN_PROGRESS"

CUSTOMERS = "customers"
ORDERS = "orders"
PRODUCTS = "products"
EMPLOYEES = "employees"

tables = {
CUSTOMERS :{"table_name": "Customers", "id": "customer_id"},
ORDERS :{"table_name": "Orders", "id": "order_id"},
PRODUCTS:{"table_name": "Products", "id": "product_id"},
EMPLOYEES:{"table_name": "Employees", "id": "employee_id"}
}

EXPORT_FILETYPES = ['txt', 'csv', 'xlsx']

# internal database for history

class History(db.Model):
    __tablename__ = "History"
    id = db.Column('history_id', db.Integer, primary_key=True)
    operation = db.Column(db.String)
    table = db.Column(db.String)
    date = db.Column(db.String)
    employee_id = db.Column(db.Integer, db.ForeignKey(tables['employees']['table_name'] + "." + tables['employees']['id'])) 
    def __init__(self, operation, employee_id, table, date):
        self.operation = operation
        self.employee_id = employee_id
        self.table = table
        self.date = date

class Customers(db.Model):
	__tablename__ = tables['customers']['table_name']
	id = db.Column(tables['customers']['id'], db.Integer, primary_key=True)
	firstname = db.Column(db.String)
	lastname = db.Column(db.String)
	email = db.Column(db.String)
	street = db.Column(db.String)
	postal_code = db.Column(db.String)
	town = db.Column(db.String)
	phone = db.Column(db.String)
	orders = db.relationship(tables['orders']['table_name'], backref="customer")

	def __init__(self, firstname, lastname, email, street, postal_code, town, phone):
		self.firstname = firstname
		self.lastname = lastname
		self.email = email
		self.street = street
		self.postal_code = postal_code
		self.town = town
		self.phone = phone

	def __repr__(self):
		return '<User %r>' % self.firstname

class Products(db.Model):
	__tablename__ = tables['products']['table_name']
	id = db.Column(tables['products']['id'], db.Integer, primary_key=True)
	product_name = db.Column(db.String(64))
	description = db.Column(db.Text)
	price = db.Column(db.String)
	qty = db.Column(db.Integer)
	orders = db.relationship(tables['orders']['table_name'], backref="product")

	def __init__(self, product_name, description, price, qty):
		self.product_name = product_name 
		self.description = description 
		self.price = price
		self.qty = qty

	def __repr__(self):
		return '<Product %r>' % self.product_name


class Orders(db.Model):
	__tablename__ = tables['orders']['table_name']
	id = db.Column(tables['orders']['id'], db.Integer, primary_key=True)
	status = db.Column(db.String(10))
	date = db.Column(db.String)
	comments = db.Column(db.String)
	customer_id= db.Column(db.Integer, db.ForeignKey(tables['customers']['table_name'] + "." + tables['customers']['id']))
	product_id = db.Column(db.Integer, db.ForeignKey(tables['products']['table_name'] + "." + tables['products']['id']))

	def __init__(self, status, date, comments, cust_id, product_id):
		self.status = status
		self.date = date
		self.comments = comments
		self.customer_id = cust_id
		self.product_id = product_id
	
	def __repr__(self):
		return '<Order %r>' % self.id

class Employees(db.Model):
	__tablename__ = tables['employees']['table_name']
	id = db.Column(tables['employees']['id'], db.Integer, primary_key=True)
	name = db.Column(db.String)
	phone = db.Column(db.String)
	email = db.Column(db.String)
	restriction = db.Column(db.String)
	hash = db.Column(db.String)
	salt = db.Column(db.String)
	def __init__(self, name, phone, email, restriction, hash, salt):
		self.name = name
		self.phone = phone
		self.email = email
		self.restriction = restriction
		self.hash = hash
		self.salt = salt
	
	def __repr__(self):
		return '<Employee %r>' % self.name
# helper functions
def table_from_string(table):
	t = None
	if table == CUSTOMERS:
		t = Customers
	elif table == ORDERS:
		t = Orders
	elif table == PRODUCTS:
		t = Products
	elif table == EMPLOYEES:
		t = Employees
	return t

def get_columns(table):
	t = table_from_string(table)
	if t is None:
		return None
	else:
		return filter(lambda x: x != 'hash' and x != 'salt', t.__mapper__.columns.keys())

def filtered_cols():
		filter = ['id','hash', 'salt', 'date']
		return filter

def to_json(record):
    response = {}
    for col in get_columns(record.__tablename__.lower()):
        response[col] = record.__getattribute__(col)
    return json.dumps(response)



