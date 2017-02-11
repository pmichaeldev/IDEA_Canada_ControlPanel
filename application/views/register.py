from flask import Flask, Blueprint, render_template, url_for, request, session, redirect
from .. import utils
from ..models import Employees
from ..restrictions import *
from ..database import db
from login import user_exists, logged_in

register_page = Blueprint('register', __name__, template_folder='../templates')

@register_page.route('/register', methods=["GET", "POST"])
def show():
	email = None
	try:
	    email = session["email"]
	except KeyError:
		pass
	if logged_in() and is_admin_user(email):
	    params = dict(title_name='Register', roles=ROLES)
	    if request.method == 'POST':
		error = False
		name = request.form['name']
		phone = request.form['phone']
		email = utils.normalize(request.form['email'])
		password = request.form['password']
		verify = request.form['verify']
		r = request.form['restriction']
		params['name'] = name
		params['phone'] = phone
		params['email'] = email
		if not name:
		    params['name_info'] = "The name can't be empty"
		    error = True
		if not phone:
		    params['phone_info'] = "The phone number can't be empty"
		    error = True
		if not utils.valid_email(email):
		    params['email_info'] = "That is not a valid email."
		    error = True
		if not utils.valid_password(password):
		    params['pw_info'] = "That is not a valid password."
		    error = True
		if verify != password:
		    params['verify_info'] = "The passwords don't match."
		    error = True
		if user_exists(email):
		    params['email_info'] = "That email is alredy in use."
		    error = True
		if not r:
		    params['restriction_info'] =  "You need to specify a user type."
	            error = True
		if error:
		    params['info_class'] = 'text-danger'
		    return render_template("register.html", **params)
		else:
		    # put user in database
		    # now we can safely say,
		    # the username, password, email are valid
		    # the usernanme, email are not already in our database
		    h = utils.gen_hash(password)
		    salt , h = utils.get_salt_hash(h)
		    new_user = Employees(name, phone, email, r, h, salt)
		    db.session.add(new_user)
		    db.session.commit()
		    return redirect(url_for("login.show"))
	    else:
		return render_template("register.html", **params)
	else:
	    return redirect(url_for("login.show"))


def is_admin_user(email):
    if email is None:
        return False
    email = normalize(email)
    user = Employees.query.filter_by(email=email).first()
    if user is None:
        return False
    if user.restriction == ADMIN_ROLE:
        return True
    return False
 
