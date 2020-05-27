import psycopg2

db_host = "m2-crud-demo.c8bvvb163dhi.us-east-2.rds.amazonaws.com"
db_name = "image_gallery"
db_user = "image_gallery"

password_file = "/home/ec2-user/.image_gallery_config"

connection = None

def get_password():
	f = open(password_file, "r")
	result = f.readline()
	f.close()
	return result[:-1] #drops new line char at end of result

def connect():
	global connection #declare as global
	connection = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=get_password())

def execute(query,args=None):
	global connection
	cursor = connection.cursor()
	if not args:
		cursor.execute(query)
	else:
		cursor.execute(query, args)
	return cursor

def promptUser():
	result = input(
		'''
Please select from the following list of options:\n
1) List users\n
2) Add user\n
3) Edit user\n
4) Delete user\n
5) Quit\n
		'''
	)
	return result

def evalPrompt(result):
	if (result == '1'):
		listUsers()
	elif (result == '2'):
		insertUser()
	elif (result == '3'):
		editUser()
	elif (result == '4'):
		deleteUser()
	else:
		print('Default')

def listUsers():
	res = execute('select username, full_name from users;')
	for row in res:
		print(row)
		
def getNewUser():
	username = input('Enter a username for the new user: ')
	salt = input('Enter a password for the new user: ')
	full_name = input('Enter the full name of the new user')
	new_account = [username, salt, fullname]
	return new_account
		
def insertUser(args):
	args = getNewUser()
	insert into users values (args[0], args[1], args[2]); #un, pwsd, fn

def editPrompt():
	editUser = input('Please enter the username for the user you wish to edit: ')
	
	editType = input(
		'''
Please select from the following list of options:\n
1) Edit Username\n
2) Edit Password\n
3) Edit Full Name\n
4) Cancel\n
		'''
	)
	
	if (editType == '1'):
		editType = 'username'
	elif (editType == '2'):
		editType = 'password'
	elif ('editType == 3'):
		editType = 'full_name'
	else:
		return
	
	editArgs = [edit_type, editUser]
	return editArgs
	
def editUser():
	editArgs= editPrompt()
	newValue = input('Enter the new value: ')
	res = execute("update users set '%s' = '%s' where username='%s';", (editArgs[0], newValue, editArgs[1])) 
	
def deleteUser():
	unluckyUser = input('Enter the username for the user you wish to delete.')
	res = execute("delete from users where username = '%s';")
	
def main():
	result = ''
	connect()
	while(result != '5'):
		result = promptUser()
		func = evalPrompt(result)

if __name__ == '__main__':
	main()
