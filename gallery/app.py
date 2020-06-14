from flask import Flask
from flask import request
from flask import render_template
from tools.user_admin import *

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/admin')
def admin_render():
    return render_template('admin.html')
