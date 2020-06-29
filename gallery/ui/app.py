from flask import Flask, session, render_template, redirect, url_for, request
#from gallery.tools.user_dao import UserDAO #UserDAO
from gallery.tools.postgres_user_dao import PostgresUserDAO
from gallery.tools.user import User
from gallery.tools.db import connect
from gallery.tools.secrets import get_secret_flask_session
from functools import wraps # decorator/wrapper requires_admin below

app = Flask(__name__)

app.secret_key = get_secret_flask_session()

connect()

def get_user_dao():
   return PostgresUserDAO()
   
def check_admin():
   return 'username' in session and session['username'] == 'fred'
   
def requires_admin(view):
   @wraps(view)
   def decorated(**kwargs):
      if not check_admin():
         return redirect('/login')
      return view(**kwargs)
   return decorated
   
@app.route('/') #/admin/users replacement
def root_page(): # admin_interface()
   return render_template('login.html')
         
@app.route('/admin/users') #/admin/users replacement
@requires_admin # wrapper from above
def users(): # admin_interface()
   return render_template('users.html', users=get_user_dao().get_users())


@app.route('/admin/deleteUser/<username>')
def deleteUser():
   return render_template("confirm.html", 
                           title ="Confirm Delete", 
                           message="Are you sure you want to delete this user?",
                           on_yes="/admin/executeDeleteUser/"+username,
                           on_no="/admin/users")
                           
@app.route('/admin/executeDeleteUser/<username>')
def executeDeleteUser(username):
   get_user_dao().delete_user(username)
   return redirect('/admin/users')
   
@app.route('/invalidLogin') # LOOK AT MESSAGE FLASHING FUNCTION INSTEAD OF REDIRECT ~  ALLOWS TO ASYNC TELL USER THEIR STUFF IS INVALID
def invalidLogin():
   return "Invalid"
   
@app.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
      user = get_user_dao().get_user_by_username(request.form["username"]) # returns user object from DAO
      if user is None or user.password != request.form["password"]: 
         return redirect('/invalidLogin')
      else:
         session['username'] = request.form["username"]
        # return redirect('/debugSession'):
         return render_template('users.html', users=get_user_dao().get_users()) # just redirecting here for now 
   else:
      return render_template('login.html')
      
      
@app.route('/admin/newUser')
def new_user_interface():
   return render_template('new_user.html')

@app.route('/admin/editUser/<username>/<full_name>', methods=['GET'])
def modify_user(username, full_name):
   user = get_user_dao().get_user_by_username(username) # returns user object from DAO
   if user is None:  # if user not found or password wrong
      return redirect('/admin/users')
   else:
      return render_template('editUser.html', user=user)

@app.route('/admin/commitEdit/', methods=['POST'])
def commit_edit():
   user = get_user_dao().get_user_by_username(username)
   if user is None:  # if user not found or password wrong
      return redirect('/admin/users')
   else:
      get_user_dao().modify_user(request.form["username"], request.form["new_password"], request.form["new_full_name"])
      return redirect('/admin/users')    
      
@app.route('/admin/commitNewUser', methods=['POST'])
def commit_new():
   user = get_user_dao().get_user_by_username(request.form["username"]) # returns user object from DAO
   if user is None:  # if user not found or password wrong
      get_user_dao().create_user(request.form["username"], request.form["password"], request.form["full_name"])
   return redirect('/admin/users')      
      
   
@app.route('/storeStuff')
def storeStuff():
   session['something'] = 22
   session['other thing'] = 'bob'
   return ""
    
@app.route('/debugSession')
def debugSession():
   result = ""
   for key, value in session.items():
      result += key+"->"+str(value)+"<br />"
   return result


