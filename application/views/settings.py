from flask import Flask, Blueprint, render_template, url_for, request, redirect, session, make_response 
from ..models import tables
from ..restrictions import * 
from login import logged_in, change_password, change_email

settings_page = Blueprint('settings', __name__, template_folder='../templates')

languages = {
'en' : 'English',
'fr': 'French',
} 

backups = {
'1m' : 'Every month',
'2m' : 'Every 2 months',
'6m' : 'Every 6 months',
'12m': 'Every 12 months'
}

@settings_page.route('/settings', methods=['GET', 'POST'])
def show():
    if not logged_in():
        return redirect(url_for('login.show'))
    role = get_role(session['email'])
    tables = get_tables(role)
    params = dict(title_name='Settings')
    params['role'] = role
    params['tables'] = tables
    params['languages'] = languages
    params['backups'] = backups
 
    if request.method == 'GET':
        return render_template('settings.html', **params)
    elif request.method == 'POST':
	return save_settings(request, params)
    

def save_settings(request, params):
    email_changed = False
    password_changed = False
    lang = get_lang_or_default(request.form['lang'])
    backup = set_backup_time(request.form['backup'])
    params['lang'] = lang
    params['backup'] = backup
    
    new_password = request.form['new_password']
    new_email = request.form['new_email']
    old_password = request.form['password']
    print "new password is" + str(new_password)
    print "new email is" + str(new_email)
    if old_password:
        if new_email:
	    email_changed = change_email(session['email'], new_email, old_password)
	    if email_changed:
     	        params['email_class'] = 'text-success'
	        params['email_info'] = "Email was changed successfully."
	    else:
		params['email_class'] = 'text-danger'
		params['email_info'] = "there was an error changing your email."
        if new_password:
	    password_changed = change_password(session['email'], old_password, new_password)
	    if password_changed:
                params['password_class'] = 'text-success'
		params['pw_info'] = 'Password was changed successfully.'
	    else:
	        params['password_class'] = 'text-danger'
	        params['pw_info'] = "there was an error changing your password."
    else:
	params['old_pw_info'] = 'Your old password is needed'
	params['old_password_class'] = 'text-danger'
	
    resp = make_response(render_template('settings.html', **params))
    resp.set_cookie('lang', lang)
    return resp

def get_lang_or_default(lang):
	if lang not in languages:
		return 'en'
	return lang

def set_backup_time(backup):
	return backup
