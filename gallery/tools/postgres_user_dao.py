from . import db
from .user_dao import UserDAO
from .user import User

class PostgresUserDAO(UserDAO):
   def __init__(self):
      pass
      
   def get_users(self):
      result = []
      cursor = db.execute("select username,password,full_name from users")
      for t in cursor.fetchall():
         result.append(User(t[0], t[1], t[2]))
      return result
      
   def get_user_by_username(self, username):
      cursor = db.execute("select username,password,full_name from users where username=%s", (username,))
      row = cursor.fetchone()
      if row is None:
         return None
      else:
         return User(row[0], row[1], row[2])
      
   def delete_user(self, username):
      db.execute("delete from users where username=%s", (username,))
      
   def create_user(self, username, password, full_name):
      db.execute("insert into users (username, password, full_name) values (%s, %s, %s);", (username, password, full_name));

   def modify_user(self, username, password, full_name):
      if (password != ''):
         db.res = execute("update users set password = %s where username=%s;", (password, username))
      if (full_name != ''):
         db.execute("update users set full_name = %s where username=%s;", (full_name, username))
