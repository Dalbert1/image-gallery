import json
import psycopg2
import os
from gallery.tools.secrets import get_secret_image_gallery

connection = None

def get_secret():
	jsonString = get_secret_image_gallery()
	return json.loads(jsonString) # returns python dictionary

def get_secret():
   jsonString = get_secret_image_gallery()
   return json.loads(jsonString) # returns python dictionary

def get_password(secret):
   #return os.getenv("IG_PASSWD") 
   return secret['password']

def get_host(secret):
   #return os.getenv("PG_HOST") 
   return secret['host']

def get_username(secret):
  # return os.getenv("IG_USER") 
   return secret['username']
   
def get_dbname(secret):
   #return os.getenv("IG_DATABASE") #
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
	connection.commit()
	return cursor

def listUsers():
	res = execute('select * from users;')
	return res
	
def listAllNoPass():
	res = execute('select username, full_name from users;')
	return res
	
def getNoPass(username):
	res = execute('select username, full_name from users where username=%s', (username,))
	return res
	
def getUserPassword(username):
	res = execute('select password from users where username=%s;', (username,))
	return res
	
def getFullName(username):
	res = execute('select full_name from users where username=%s;', (username,))
	return res

def insertUser(new_account):
	res = execute("insert into users (username, password, full_name) values (%s, %s, %s);", (new_account[0], new_account[1], new_account[2]));
	connection.commit()
	
def insertImage(username, image_name):
	res = execute("insert into s3_images (username, image_name) values (%s, %s);", (username, image_name))
	return res
	
def deleteImage(username, image_name):
	res = execute("delete from s3_images where username=%s and image_name=%s;", (username, image_name))
	return res
	
def deleteAllUserImages(username):
	res = execute("delete from s3_images where username =%s;", (username,))
	return res
	
def listImages(username):
	res = execute()
	return res
	
def editUser(userToEdit):
	username = userToEdit[0]
	password = userToEdit[1]
	full_name = userToEdit[2]
	if (password != ''):
		res = execute("update users set password=%s where username=%s;", (password, username))
	if (full_name != ''):
		res = execute("update users set full_name=%s where username=%s;", (full_name, username))
	connection.commit()	

def checkExists(username):
	res = execute('select * from users where username=%s;', (username,))
	row = res.fetchone()
	if (row):
		return True
	return False

def deleteUser(unluckyUser):
	res = execute("delete from users where username=%s;", (unluckyUser,))
	connection.commit()

def main():
	connect()
	res = listUsers()
	print(res)
	for row in res:
		print(row)

if __name__ == '__main__':
	main()	

