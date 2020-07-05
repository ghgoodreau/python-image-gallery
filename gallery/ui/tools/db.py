import psycopg2
import json
from .secrets import *
import os
# rewriting this because user_admin is incompatible with scaling to a web app

# setup stuff
connection = None

#db info
# users table
# username, password, full_name

#s3_imgs table
#username, img_name

#to connect = psql -h mydbip -U user

## IF HOSTED ON CLOUD
def get_secret():
	jsonString = get_secret_image_gallery()
	return json.loads(jsonString)

def get_password(secret):
	return secret['password']

def get_host(secret):
	return secret['host']

def get_username(secret):
	return secret['username']

def get_dbname(secret):
	return secret['database_name']

# def connect():
# 	global connection
# 	secret = get_secret()
# 	connection = psycopg2.connect(host=get_host(secret), dbname=get_dbname(secret), user=get_username(secret), password=get_password(secret))

## IF LOCAL
d_bname = os.environ.get('IG_DATABASE')
db_port = os.environ.get('PG_PORT')
db_host = os.environ.get('PG_HOST')
db_user = os.environ.get('IG_USER')
db_password = os.environ.get('IG_PASSWRD')

def connect():
	global connection
	connection = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password, port=db_port)

def execute(query, args=None):
	global connection
	cursor = connection.cursor()
	if not args:
		cursor.execute(query)
	else:
		cursor.execute(query, args)
	return cursor
# end setup stuff

# lists all users
def listUsers():
    list_users = execute('select * from users;')
    return list_users


#returns a specific user with all their info
def getUser(username):
    get_user = execute('select * from users where username=%s;', (username,))
    return get_user

#function to check if a user exits already. Returns true if user exists, false otherwise.
def checkUserExists(usernameToCheck):
	checking = execute('select * from users where username=%s;', (usernameToCheck,))
	row = checking.fetchone()
	if (row):
		return True
	return False

# function to add user.
def addUser(username):
	adduser_name = username[0]
	adduser_pass = username[1]
	adduser_fullname = username[2]
	try:
		adding = execute('insert into users values (%s, %s, %s);', (adduser_name, adduser_pass, adduser_fullname))
		connection.commit()
	except:
		pass

# function to edit user details
def editUser(username):
    edituser_name = username[0]
    edituser_pass = username[1]
    edituser_fullname = username[2]
    if (checkUserExists(edituser_name) == True):
	    if (edituser_pass != ''):
                edit_pass = execute('update users set password=%s where username=%s;', (edituser_pass, edituser_name))
	    if (edituser_fullname != ''):
                edit_fullname = execute('update users set full_name=%s where username=%s;', (edituser_fullname, edituser_name))
	    connection.commit()

# function to delete user. no confirm necessary as that will be application side
def deleteUser(username):
    user_to_delete = username[0]
    if (checkUserExists(user_to_delete) == True):
            deleting = execute('delete from users where username=%s', (user_to_delete,))
            connection.commit()

# methods for s3 (separate table in image_gallery db) #confirmed working
def addImage(username, img_name):
	s3_addimage = execute('insert into s3_imgs values (%s, %s);', (username, img_name))
	connection.commit()

# unsure if this works yet
def getImages(username):
	s3_getimages = execute('select * from s3_imgs where username=%s', (username,))

# delete images
def deleteImage(username, img_name):
	s3_deleteimage = execute('delete from s3_imgs where username=%s and img_name=%s', (username, img_name))
	connection.commit()
# main method for testing only
def main():
    connect()
    test = listUsers()
    for row in test:
        print(row)

if __name__ == '__main__':
	main()
