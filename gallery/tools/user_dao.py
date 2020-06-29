class UserDAO:
   def get_users(self): # If you're a UserDAO you should have this method, going to subclass this class with postgres_user_dao.py
      raise Exception("Must be implemented")
      
   def delete_user(self, username):
      raise Exception("Must be implemented")
