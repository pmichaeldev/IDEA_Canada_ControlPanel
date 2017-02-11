from flask import Flask, Blueprint, render_template, url_for, request, session, redirect

index_page = Blueprint('index', __name__, template_folder='../templates')
from login import logged_in

@index_page.route('/')
def show():
    if logged_in():
        return redirect(url_for('dashboard.show'))
    else:
	return redirect(url_for('login.show'))


