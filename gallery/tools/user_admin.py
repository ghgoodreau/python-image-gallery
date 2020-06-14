import psycopg2
import json
from secrets import get_secret_image_gallery

db_name = "image_gallery"
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

# function that prints a menu
def printMenu():
	print(" ")
	print("1)  List users")
	print("2)  Add user")
	print("3)  Edit user")
	print("4)  Delete user")
	print("5)  Quit")

# function that lists all users in the database
def listUsers():
	print(" ")
	listing = execute('select * from users')
	for row in listing:
		print(row)

# function to add user.
def addUser():
	print(" ")
	adduser_name = input("Username> ")
	adduser_pass = input("Password> ")
	adduser_fullname = input("Full name> ")
	try:
		adding = execute('insert into users values (%s, %s, %s)', (adduser_name, adduser_pass, adduser_fullname))
		connection.commit()
	except:
		print('User already exists.')

#function to check if a user exits already. Returns true if user exists, false otherwise.
def checkUserExists(usernameToCheck):
	checking = execute('select * from users where username=%s;', (usernameToCheck,))
	row = checking.fetchone()
	if (row):
		return True;
	return False;

# function to edit user details
def editUser():
	print(" ")
	edituser_name = input("Username to edit> ")
	if (checkUserExists(edituser_name) == True):
		edituser_pass = input("New password (press enter to keep current)> ")
		edituser_fullname = input("New full name (press enter to keep current)> ")
		if (edituser_pass != ''):
			editingpass = execute("update users set password=%s where username=%s;", (edituser_pass, edituser_name))
		if (edituser_fullname != ''):
			editingfullname = execute("update users set full_name=%s where username=%s;", (edituser_fullname, edituser_name))
		connection.commit()
	else:
		print('No user with that name exists.')
	# Error: No such user.

# completed function to delete user details
def deleteUser():
	print(" ")
	deleteuser_name = input("Enter username to delete: ")
	if (checkUserExists(deleteuser_name) == True):
		deleteuser_choice = input("Are you sure you want to delete that user? (y/n)> ")
		if deleteuser_choice == 'y':
	# still need to verify that deleteuser_name exists within the table
			try:
				deleting = execute('delete from users where username=%s', (deleteuser_name,))
				print("Deletion successful.")
				connection.commit()
			except:
				print("Error deleting.")
	else:
		print("User doesn't exist.")

# completed main function
def main():
	connect()
	choice = '0'
	# while loop that repeats printing the menu until user inputs quit choice
	while choice != '5':
		printMenu()
		choice = input("Enter command> ")
		if choice == "1":
			listUsers()
		if choice == "2":
			addUser()
		if choice == "3":
			editUser()
		if choice == "4":
			deleteUser()
	# choice is 5
	print(" ")
	print("See ya!")

if __name__ == '__main__':
	main()
