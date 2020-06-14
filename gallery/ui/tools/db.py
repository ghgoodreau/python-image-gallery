import psycopg2
import json
from secrets import get_secret_image_gallery

# rewriting this because user_admin is incompatible with scaling to a web app


# setup stuff
connection = None

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

def connect():
	global connection
	secret = get_secret()
	connection = psycopg2.connect(host=get_host(secret), dbname=get_dbname(secret), user=get_username(secret), password=get_password(secret))

def execute(query, args=None):
	global connection
	cursor = connection.cursor()
	if not args:
		cursor.execute(query)
	else:
		cursor.execute(query, args)
	return cursor

# lists all users
def listUsers():
    list_users = execute('select * from users;')
    return list_users

# needed to print on admin page without password
def listUsersWithoutPassword():
    list_nopassword = execute('select username, full_name from users;')
    return res

#returns a specific user with all their info
def getUser(username):
    get_user = execute('select * from users where username=%s', (username,))
    return get_user

# returns a specific user with no password
def getUserNoPass(username):
    get_user_nopass = execute('select username, full_name from users where username=%s', (username,))
    return get_user_nopass

def main():
	connect()
    test = listUsers()
    print(test)
    for row in test:
        print(row)

if __name__ == '__main__':
	main()
