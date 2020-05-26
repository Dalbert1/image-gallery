import psycopg2

db_host = "demo-database-1.c923ckbw7nv.us-east-2.rds.amazonaws.com"
db_name = "image_gallery"
db_user = "image_gallery"

password_file = "/home/ec2-user/.image_gallery_config" # NOT IN GITHUB DIR

connection = None

def get_password():
	f = open(password_file, "r")
	result = f.readline()
	f.close()
	return result[:-1] #drops new line char at end of result
	
def connect():
	global connection #declare as global
	connection = psycopg2.connect("host"=db_host, dbname=db_name, user=db_user, password=get_password())

def execute(query,args=None):
	global connection
	cursor = connection.cursor()
	if not args:
		cursor.execute(query)
	else:
		cursor.execute(query, args)
	return cursor
	
def main():
	connect()
	res = execute('select * from users;')
	for row in res:
		print(row)
	res = execute("update users set password=%s where username='fred'", ('banana',)) # passing in tuple, must include comma if only one item
	for row in res:
		print(row) #shows password changed for Fred
		
if __name__ == '__main__':
	main()
