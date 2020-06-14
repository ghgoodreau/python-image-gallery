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
def new_render():
    connect()
    return render_template('addUser.html')

@app.route('/admin/modifyUser/<username>')
def modify_render(username):
    connect()
    return render_template('modifyUser.html', username = username)

@app.route('/admin/addingUser', methods=['POST'])
def adding_user_render():
    new_user = [request.form['adding_username'], request.form['adding_password'], request.form['adding_full_name']]
    connect()
    #without this if statement, timeout occurs
    if(checkUserExists(request.form['adding_username']) == False):
      addUser(new_user)
    return redirect(url_for('admin_render'))

@app.route('/admin/editingUser', methods=['POST'])
def editing_user_render():
    edit_user = [request.form['editing_username'], request.form['editing_password'], request.form['editing_full_name']]
    connect()
    editUser(edit_user)
    return redirect(url_for('admin_render'))

@app.route('admin/confirmDelete/<username>')
def deleting_user_render(username):
    connect()
    return render_template('confirm.html', username = username)

@app.route('admin/deletingUser/<username>', methods=['POST'])
def confirmed_delete_render(username):
    connect()
    deleteUser(username)
    return redirect(url_for('admin_render'))
