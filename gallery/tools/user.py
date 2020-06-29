class User:
   def __init__(self, username, password, full_name):
      self.username = username # instance vars, can use _ for protected and __ for private
      self.password = password
      self.full_name = full_name
      
   #def username(self): if we want to reference private instance variables self.__username
      #return self.__username
   
   #def full_name(self):
      #return self.__full_name
 #test change     
   def __repr__(self): # turns itself into a string
      return "User with username "+self.username+" password: "+self.password+" full name: "+self.full_name
