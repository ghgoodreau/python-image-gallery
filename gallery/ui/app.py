from flask import Flask
from flask import request
from flask import render_template
from tools.user_admin import connect
from tools.secrets import get_secret_image_gallery

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/admin')
def admin_render():
    connect()
    user_list = listAllNoPass().fetchall()
    return render_template('admin.html', user_list=user_list)
