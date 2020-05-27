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
				switch = {
								'1': listUsers(),
								'2': listUsers(),
								'3': listUsers(),
								'4': listUsers(),
								'5': listUsers(),
				}
				func = switch.get(result)
				return func

def listUsers():
				res = execute('select * from users;')
				for row in res:
								print(row)

def main():
	flag = True
	connect()
	while(flag == True):
		result = promptUser()
		func = evalPrompt(result)
		func()

if __name__ == '__main__':
	main()
	
