import psycopg2

db_host = "demo-database-1.cctr1zoblre6.us-east-2.rds.amazonaws.com"
db_name = "cruddemo1"
db_user = "user_admin"
connection = None
password_file = "/home/ec2-user/.image_gallery_config"

def get_password():
	f = open(password_file, "r")
	result = f.readline()
	f.close()
	return result[:-1]

def connect():
	global connection
	connection = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=get_password())

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
	res = execute('select * from users')
	for row in res:
		print(row)

# function to add user. not working quite yet due to the if/else and try catch block. returns an error even if user doesn't exist.
def addUser():
	print(" ")
	adduser_name = input("Enter user to add: ")
	adduser_pass = input("Enter password: ")
	adduser_fullname = input("Enter full name of user: ")
	try:
		added = execute('insert into users values (%s, %s, %s)', (adduser_name, adduser_pass, adduser_fullname))
		connection.commit()
	except:
		print('User already exists.')
	# Error: user with username ____ already exists

# function to edit user details
def editUser():
	print(" ")
	edituser_name = input("Enter the user to edit: ")
	valid_name = execute('select * from users where username=%s', (edituser_name,))
	print(valid_name)
	# Error: No such user.

# function to delete user details
def deleteUser():
	print(" ")
	deleteuser_name = input("Enter the name of the user you want to delete: ")
	deleteuser_choice = input("Are you sure you want to delete that user? (y/n): ")
	if deleteuser_choice == 'y':
	# still need to verify that deleteuser_name exists within the table
		try:
			deleting = execute('delete from users where username=%s', (deleteuser_name,))
			print("Deletion successful.")
			# once everything is verified working, this is where I would add connection.commit()
		except:
			print("Deletion failed.")

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
		# if choice is not 1-5, print this
		else:
			print(" ")
			print("Invalid choice. Try again.")
	# choice is 5
	print(" ")
	print("See ya!")
if __name__ == '__main__':
	main()
