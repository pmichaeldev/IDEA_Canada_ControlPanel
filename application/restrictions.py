from database import db
from models import *
from utils import normalize

RESTRICTED_ROLE = "RESTRICTED_ROLE"
USER_ROLE = "USER_ROLE"
ADMIN_ROLE = "ADMIN_ROLE"
ROLES = [RESTRICTED_ROLE, USER_ROLE, ADMIN_ROLE]

ADD = "ADD"
DELETE = "DELETE"
EDIT = "EDIT"
SEARCH = "SEARCH"
IMPORT_FILE = "IMPORT"
EXPORT_FILE = "EXPORT"

CSS_ICON_CLASS = {
		ADD: "icon-plus",
		DELETE: "icon-trash",
		EDIT: "icon-pencil",
		SEARCH: "icon-search",
		IMPORT_FILE: "icon-circle-arrow-down",
		EXPORT_FILE: "icon-circle-arrow-up"

}

TABLE_ACCESS = {
		RESTRICTED_ROLE: [{PRODUCTS:[EXPORT_FILE]},
                       	{CUSTOMERS: [EXPORT_FILE]}],

               	USER_ROLE:[{ PRODUCTS:[ADD, EDIT, IMPORT_FILE, EXPORT_FILE]},
			{CUSTOMERS: [ADD, EDIT,  IMPORT_FILE, EXPORT_FILE]},
                      	{ORDERS: [ADD, EDIT,  IMPORT_FILE, EXPORT_FILE]}],

                ADMIN_ROLE: [{PRODUCTS:[ADD, EDIT, DELETE, IMPORT_FILE, EXPORT_FILE]},
                      	{CUSTOMERS: [ADD, EDIT, DELETE, IMPORT_FILE, EXPORT_FILE]},
                       	{ORDERS: [ADD,EDIT,DELETE, IMPORT_FILE,EXPORT_FILE]},
                 	{EMPLOYEES: [ADD,EDIT,DELETE, IMPORT_FILE,EXPORT_FILE]}]
} 

def get_access(role):
	return TABLE_ACCESS[role]

def get_operations(role, table):
	for role in get_access(role):
		if table in role:
			return role[table]


def get_tables(role):
	access = get_access(role)
	tables = []
	for table in access:
		tables.append(table.keys()[0])
	return tables


def get_role(email):
    email = normalize(email)
    employee = Employees.query.filter_by(email=email).first()
    if employee == None:
        return None
    return employee.restriction
