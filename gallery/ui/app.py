from flask import Flask, render_template, request, redirect, url_for, session
from .tools import *
from .tools.secrets import *
from .tools.db import *
from .tools.pg_user_dao import PostgresUserDAO
from .tools.user import User
from .tools.s3 import *
from base64 import b64encode

app = Flask(__name__)
app.secret_key = b'asdihhqweih123' # this should be in AWS secrets in a deployed setting for security purposes
BUCKET = 'm6-image-gallery-ghg' # this should be in AWS secrets in a deployed setting for security purposes

#DAO from m5
def get_user_dao():
    return PostgresUserDAO()

# home page!
@app.route('/')
def hello_world():
    return render_template('home.html')

# debugs the session username
@app.route('/debugSession')
def debugSession():
   return session['username']

# checks if user logged in is in the database
def check_login():
    return 'username' in session and get_user_dao().get_user_by_name(session['username'])

# checks if user logged in is an admin (admin is hard coded as dongji right now)
def check_admin():
    return 'username' in session and session['username'] == 'dongji'

# admin page, locked behind admin account
@app.route('/admin')
def admin_render():
    connect()
    if not check_admin():
        return redirect('/login')
    listOfUsers = listUsers().fetchall()
    return render_template('admin.html', user_list = listOfUsers)

# new user page
@app.route('/admin/newUser')
def new_render():
    connect()
    if not check_admin():
        return redirect('/login')
    return render_template('addUser.html')

# modify user page
@app.route('/admin/modifyUser/<username>')
def modify_render(username):
    connect()
    if not check_admin():
        return redirect('/login')
    return render_template('modifyUser.html', username = username)

# adding user
@app.route('/admin/addingUser', methods=['POST'])
def adding_user_render():
    new_user = [request.form['adding_username'], request.form['adding_password'], request.form['adding_full_name']]
    connect()
    if not check_admin():
        return redirect('/login')
    #without this if statement, timeout occurs
    if(checkUserExists(request.form['adding_username']) == False):
      addUser(new_user)
    return redirect(url_for('admin_render'))

# editing user
@app.route('/admin/editingUser', methods=['POST'])
def editing_user_render():
    edit_user = [request.form['editing_username'], request.form['editing_password'], request.form['editing_full_name']]
    connect()
    if not check_admin():
        return redirect('/login')
    editUser(edit_user)
    return redirect(url_for('admin_render'))

# confirms the deletion of user
@app.route('/admin/confirmDelete/<username>')
def deleting_user_render(username):
    connect()
    if not check_admin():
        return redirect('/login')
    return render_template('confirm.html', username = username)

# process of deleting user
@app.route('/admin/deletingUser', methods=['POST'])
def confirmed_delete_render():
    user_to_delete = [request.form['deleting_username']]
    connect()
    if not check_admin():
        return redirect('/login')
    deleteUser(user_to_delete)
    return redirect(url_for('admin_render'))

# the initial route to login page where you will be prompted to login
@app.route('/login', methods=['GET', 'POST'])
def login_render():
    connect()
    if request.method == 'POST':
        user = get_user_dao().get_user_by_name(request.form["login_user"])
        if user is None or user.password != request.form["login_pass"]:
         return redirect('/invalidLogin')
        else:
            session['username'] = user.username
            return redirect("/")
    else:
        return render_template('login.html')

# invalid login page. may make this a full html doc for links later.
@app.route('/invalidLogin')
def invalid_login():
    return "Invalid Username or Password."

# the actual action of logging in (once you click the login button)
# must start a new sesh and authenticate the user, then redirect home
# @app.route('/login/loggingIn', methods=['POST'])
# def login_redirect():
#     connect()
#     # do things here that authenticate user
#     return redirect(url_for('hello_world'))

# page where you select and upload your image
@app.route('/upload', methods=['GET', 'POST'])
def upload_render():
    connect()
    if not check_login():
        return redirect('/login')
    return render_template('upload.html',user = get_user_dao().get_user_by_name(session['username']))

# uploading image
@app.route('/uploading', methods=['GET', 'POST'])
def uploading_render():
   if request.method == 'POST':
      username = session['username']
      image = request.files['file']
      path = username + '/' + image.filename
      put_object(BUCKET, path, image) # s3 side
      addImage(username, path) # database side
      return redirect("/view")

#view gallery page
@app.route('/view', methods=['GET', 'POST'])
def view_render():
    connect()
    if not check_login():
        return redirect('/login')
    username = session['username']
    imports = {}
    images = get_user_dao().get_images_by_name(username)
    for image in images:
        image_object = get_object(BUCKET, image)
        imports[image] = b64encode(image_object).decode("utf-8")
    return render_template('view.html', user=session['username'], images=imports)

# not working right now but not a requirement
@app.route('/logout')
def logout_render():
    connect()
    session['username'] = None
    return redirect("/login")

# delete images
@app.route('/delete', methods=['POST', 'GET'])
def delete_button():
    connect()
    if not check_login():
        return redirect('/login')
    delete_object(BUCKET, request.form['key'])
    deleteImage(session['username'], request.form['key'])
    return redirect("/view")
