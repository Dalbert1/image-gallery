from db import *

def promptAdminTask():
	result = input(
		'''
Please select from the following list of options:
1) List users
2) Add user
3) Edit user
4) Delete user
5) Quit
Enter command> '''
	)
	return result

def promptNewUser():
	username = input('\nUsername> ')
	salt = input('Password> ')
	full_name = input('Full name> ')
	new_account = [username, salt, full_name]
	return new_account

def promptEdit():
	username = input('\nUsername to edit> ')
	password = ''
	full_name = ''
	if (checkExists(username) == True):
		password = input('New password (press enter to keep current)> ')
		full_name = input('New full name (press enter to keep current)> ')
	else:
		print('\nNo such user.')
		
	userToEdit = [username, password, full_name]
	return userToEdit
	
def promptDelete():
	username = input('\nPlease enter the username for the user you wish to edit: ')
	return username
	
def evalPrompt(result):
	if (result == '1'):
		listAllUsers()
	elif (result == '2'):
		newUser()
	elif (result == '3'):
		editExisting()
	elif (result == '4'):
		deleteExisting()
	elif (result == '5'):
		print('\nBye\n')
	else:
		print('\nPlease enter a valid task number.')
		
def listAllUsers():
	usersCursor = listUsers() #db.py returns cursor
	rows = usersCursor.fetchall()
	print('''
username password full name
-------------------------------''')
	for row in rows:
		print(row[0] + '\t' + row[1] + '   ' + row[2])
		
def newUser():
	new_user = promptNewUser()
	username = new_user[0].lower()
	if (checkExists(username) == False):
		insertUser(new_user)
	else:
		print('\nError: user with username ' + str(new_user[0]) + ' already exists')
		
def editExisting():
	userToEdit = promptEdit()
	editUser(userToEdit) #db.py
		
def deleteExisting():
	username = promptDelete().lower()
	if (checkExists(username)):
		confirm = input('\nAre you sure that you want to delete ' + str(username) + '? ')
		if (confirm.lower() == 'yes'):
			deleteUser(username) #db.py
			print('\nDeleted.')
	else:
		print('\nUsername not found')
		
	
def main():
	global connection
	connect()
	result = ''
	while(result != '5'):
		result = promptAdminTask()
		evalPrompt(result)
	
if __name__ == '__main__':
	main()
