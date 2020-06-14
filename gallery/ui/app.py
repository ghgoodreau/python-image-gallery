from flask import Flask, render_template, request, redirect, url_for
from tools.secrets import *
from tools.db import *

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/admin')
def admin_render():
    connect()
    listOfUsers = listUsersWithoutPassword().fetchall()
    return render_template('admin.html', user_list = listOfUsers)

@app.route('/admin/newUser')
def new_user():
    return render_template('newUser.html')
