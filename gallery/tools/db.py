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
	connection.close()

if __name__ == '__main__':
	main()
