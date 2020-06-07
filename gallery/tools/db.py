import json
import psycopg2
from tools.secrets import get_secret_image_gallery

connection = None

def get_secret():
	jsonString = get_secret_image_gallery()
	return json.loads(jsonString) # returns python dictionary

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

def execute(query,args=None):
	global connection
	cursor = connection.cursor()
	if not args:
		cursor.execute(query)
	else:
		cursor.execute(query, args)
	return cursor

def listUsers():
	res = execute('select * from users;')
	return res

def insertUser(new_account):
	res = execute("insert into users (username, password, full_name) values (%s, %s, %s);", (new_account[0], new_account[1], new_account[2]));
	connection.commit()


def editUser(userToEdit):
	username = userToEdit[0]
	password = userToEdit[1]
	full_name = userToEdit[2]
	if (password != ''):
		res = execute("update users set password = %s where username=%s;", (password, username))
	if (full_name != ''):
		res = execute("update users set full_name = %s where username=%s;", (full_name, username))
	connection.commit()	

def checkExists(username):
	res = execute('select * from users where username=%s;', (username,))
	row = res.fetchone()
	if (row):
		return True
	return False

def deleteUser(unluckyUser):
	res = execute("delete from users where username = %s;", (unluckyUser,))
	connection.commit()

def main():
	connect()
	res = listUsers()
	print(res)
	for row in res:
		print(row)

if __name__ == '__main__':
	main()	
