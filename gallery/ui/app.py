from base64 import b64encode
from flask import Flask, flash, session, render_template, redirect, url_for, request #, #send_file
from gallery.tools.postgres_user_dao import PostgresUserDAO
from gallery.tools.user import User
from gallery.tools.db import connect, insertImage, deleteImage
from gallery.tools.secrets import get_secret_flask_session
from gallery.tools.s3 import get_object, put_object
from werkzeug.utils import secure_filename
from functools import wraps




#import logging
#import boto3
#from botocore.exceptions import ClientError

app = Flask(__name__)
app.secret_key = get_secret_flask_session()
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
BUCKET = "edu.au.cc.m6.python-image-gallery"

#app.config['UPLOAD_FOLDER']

connect()

def get_user_dao():
   return PostgresUserDAO()
   
def check_admin():
   if 'username' in session:
      is_admin = get_user_dao().get_admin_user_by_username(session['username'])
      return is_admin
   else: 
      return None
   
def check_auth():
   return 'username' in session and get_user_dao().get_user_by_username(session['username'])
  
def requires_admin(view):
   @wraps(view)
   def decorated(**kwargs):
      if not check_admin():
         return "Restricted to administrator"
      return view(**kwargs)
   return decorated

def requires_auth(view):
   @wraps(view)
   def decorated(**kwargs):
      if not check_auth():
         return redirect('/login')
      return view(**kwargs)
   return decorated
   

#performs the file uploads
@app.route("/upload", methods=['GET', 'POST'])
@requires_auth
def upload():
   if request.method == 'POST':
      image = request.files['file']
      path = session['username'] + '/' + image.filename
      put_object(BUCKET, path, image)
      user = session['username']
      insertImage(user, path)
      return redirect(url_for('root_page'))
      
      
# page for user to upload their new file
@app.route('/<username>/upload', methods=['GET'])
@requires_auth
def new_image(username):
   return render_template('new_image.html', user=get_user_dao().get_user_by_username(session['username']))

#displays all images for given user
@app.route('/<username>/all_images', methods=['GET', 'POST'])
@requires_auth
def user_images(username):
   user_images = get_user_dao().get_images_by_username(username)
   s3_imports = []
   for img_name in user_images:
      image_object = get_object(BUCKET, img_name)
      b64_img = b64encode(image_object).decode("utf-8")
      s3_imports.append(b64_img)
   return render_template('all_user_images.html', contents=s3_imports, user=get_user_dao().get_user_by_username(username))



# WORKING       
@app.route('/')
@requires_auth
def root_page():
   return render_template('home.html', user=get_user_dao().get_user_by_username(session['username']))

# WORKING    
@app.route('/logout')
@requires_auth
def logout():
   session['username'] = None
   return redirect('/login')

# WORKING 
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
         
# WORKING         
@app.route('/admin/users')
@requires_admin 
def users():
   return render_template('users.html', users=get_user_dao().get_users())

# WORKING
@app.route('/admin/deleteUser/<username>')
@requires_admin 
def deleteUser():
   return render_template("confirm.html", 
                           title ="Confirm Delete", 
                           message="Are you sure you want to delete this user?",
                           on_yes="/admin/executeDeleteUser/"+username,
                           on_no="/admin/users")
                       
# WORKING
@app.route('/admin/executeDeleteUser/<username>')
@requires_admin 
def executeDeleteUser(username):
   get_user_dao().delete_user(username)
   return redirect('/admin/users')

# WORKING
@app.route('/invalidLogin') # LOOK AT MESSAGE FLASHING FUNCTION INSTEAD OF REDIRECT ~  ALLOWS TO ASYNC TELL USER THEIR STUFF IS INVALID
def invalidLogin():
   return "Invalid"
   
# WORKING
@app.route('/admin/editUser/<username>/<full_name>', methods=['GET'])
@requires_admin 
def modify_user(username, full_name):
   user = get_user_dao().get_user_by_username(username) # returns user object from DAO
   if user is None:  # if user not found or password wrong
      return redirect('/admin/users')
   else:
      return render_template('editUser.html', user=user)

# (?)
@app.route('/admin/commitEdit', methods=['POST'])
@requires_admin 
def commit_edit():
   if request.method == 'POST':
      get_user_dao().modify_user(request.form["username"], request.form["new_password"], request.form["new_full_name"])
      return render_template('users.html', users=get_user_dao().get_users())
   else:
      return render_template('users.html', users=get_user_dao().get_users())
   
# WORKING
@app.route('/admin/newUser')
@requires_admin 
def new_user_interface():
   return render_template('new_user.html')

#WORKING
@app.route('/admin/commitNewUser', methods=['POST'])
@requires_admin 
def commit_new():
   user = get_user_dao().get_user_by_username(request.form["username"]) # returns user object from DAO
   if user is None:  # if user not found or password wrong
      get_user_dao().create_user(request.form["username"], request.form["password"], request.form["full_name"])
   return redirect('/admin/users')      
      
   
# reset session var
@app.route('/reset')
def storeStuff():
   session['username'] = ""
   session['other thing'] = 'bob'
   return ""
    
# debug
@app.route('/debugSession')
def debugSession():
   result = ""
   for key, value in session.items():
      result += key+"->"+str(value)+"<br />"
   return result



