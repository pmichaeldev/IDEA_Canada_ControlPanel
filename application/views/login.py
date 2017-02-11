from flask import Flask, Blueprint, render_template, url_for, request, session, redirect
from .. import utils
from ..models import Employees 
from ..database import db
from ..restrictions import get_role

login_page = Blueprint('login', __name__, template_folder='../templates', static_folder="static")

@login_page.route('/login', methods=['GET', 'POST'])
def show():
    params = dict(title_name='Login');
    if request.method == 'POST':
        error = False
        email = request.form['email']
        password = request.form['password']
        if email is session:
            return redirect(url_for("index.show"))
        params['email'] = email # this will be returned back to the page

        if not utils.valid_password(password):
            params['pw_info'] = "Incorrect password"
        if not user_exists(email):
            params['user_info'] = "Incorrect email"
            error = True
        else:
            valid_pw = valid_pw_for(email, password)
            if not valid_pw:
                params['user_info'] = "Incorrect email"
                error = True
        if not email:
            params['user_info'] = "Incorrect email"
            error = True
        if error:
            params['info_class'] = 'errorDisplay'
            return render_template("login.html", **params)
        else:
            session['email'] = email 
            return redirect(url_for("index.show"))
    else:
        if logged_in():
            return redirect(url_for("index.show"))
        return render_template("login.html", **params)


@login_page.route('/logout')
def logout():
    session.pop('email', None)
    return redirect(url_for('login.show'))

def logged_in():
    if 'email' in session:
        if get_role(session['email']) is None:
            return False
        return True
    return False

def user_exists(email):
	email = utils.normalize(email)
	exists = Employees.query.filter_by(email=email).first()
	if exists is None:
	    return False
	return True 

def valid_pw_for(email, password):
	if email and password:
		h, salt = get_user_pw(utils.normalize(email))
		return utils.check_password(h, salt, password) 
	return False

def get_user_pw(email):
	if email:
		email = utils.normalize(email)
		u = Employees.query.filter_by(email=email).first()
		return (u.hash, u.salt)
	return None

def change_password(email, old_password, new_password):
    if not logged_in():
        return False
    error = False
    email = utils.normalize(email)
    if not utils.valid_password(new_password):
        error = True
    if not valid_pw_for(email, old_password):
        error = True
    if old_password == new_password:
        error = True
    if error:
	    return False
    else:
        employee = Employees.query.filter_by(email=email).first()
        h = utils.gen_hash(new_password)
        salt , h = utils.get_salt_hash(h)
	employee.hash = h
	employee.salt = salt
	db.session.commit()
	return True

def change_email(old_email, new_email, password):
    if not logged_in():
        return False
    error = False
    old_email = utils.normalize(old_email)
    new_email = utils.normalize(new_email)
    if not utils.valid_email(new_email):
        error = True
    if user_exists(new_email):
        error = True
    if not valid_pw_for(old_email, password):
        error = True  
    if error:
        return False
    else:
	#change email 
        employee = Employees.query.filter_by(email=old_email).first()
	employee.email = new_email 
	db.session.commit()
	logout()
	session['email'] = new_email
	return True
