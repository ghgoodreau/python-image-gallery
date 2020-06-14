from flask import Flask
from flask import request
from flask import render_template
from tools import *

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/admin')
def admin_render():
    connect()
    user_list = listAllNoPass().fetchall()
    return render_template('admin.html', user_list=user_list)
