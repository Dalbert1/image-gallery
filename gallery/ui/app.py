import os
import base64
from flask import Flask, flash, session, render_template, redirect, url_for, request, send_file
from gallery.tools.postgres_user_dao import PostgresUserDAO
from gallery.tools.user import User
from gallery.tools.db import connect
from gallery.tools.secrets import get_secret_flask_session
from gallery.tools.s3 import list_files, upload_file, download_file, put_object
from werkzeug.utils import secure_filename
from functools import wraps




import logging
import boto3
from botocore.exceptions import ClientError

app = Flask(__name__)
app.secret_key = get_secret_flask_session()

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
BUCKET = "edu.au.cc.m6.python-image-gallery"

#app.config['UPLOAD_FOLDER']

connect()

# Retrieve the list of existing buckets
s3 = boto3.client('s3')
response = s3.list_buckets()

# Output the bucket names
print('Existing buckets:')
for bucket in response['Buckets']:
   print(f'  {bucket["Name"]}')
   
   
def allowed_file(filename):
   return '.' in filename and \
         filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS   
   
   

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
def upload():
  # if request.method == 'POST':
    #  print(request.files)
     #    print(request.files['photo'])
   print(request.files)
   image = request.files['file']  
   image_string = base64.b64encode(image.read())
   print(request)
   print(os.path)
   print(image)
   filename = secure_filename(image.filename)
   #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

   put_object(BUCKET, image.filename, image)
   # f#ilename = secure_filename(image_string)
   #print(image_string)
  # upload_file(image_string, BUCKET)
   #print('File pushed to s3')
   #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
   return redirect(url_for('root_page'))
      
      
"""
# check if the post request has the file part
if 'file' not in request.files:
flash('No file part')
return redirect(request.url)
file = request.files['photo']
# if user does not select file, browser also
# submit an empty part without filename
if file.filename == '':
flash('No selected file')
return redirect(request.url)
if file and allowed_file(file.filename):
image = request.files['photo']  
image_string = base64.b64encode(image.read())
# f#ilename = secure_filename(image_string)
print(image_string)
upload_file(image_string, BUCKET)
print('File pushed to s3')
#file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
return redirect(url_for('/'))
else:
return '''
<!doctype html>
<title>Upload new File</title>
<h1>Upload new File</h1>
<form method=post enctype=multipart/form-data>
<input type=file name=file>
<input type=submit value=Upload>
</form>
'''
"""







   
   
   

@app.route('/')
@requires_auth
def root_page():
   return render_template('home.html', user=get_user_dao().get_user_by_username(session['username']))
   
@app.route('/logout')
@requires_auth
def logout():
   session['username'] = None
   return redirect('/login')
   
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
      
   







# performs file downloads
@app.route("/download/<filename>", methods=['GET'])
def download(filename):
   if request.method == 'GET':
      output = download_file(filename, BUCKET)
      return send_file(output, as_attachment=True)


# page for user to upload their new file
@app.route('/<username>/upload', methods=['GET'])
@requires_auth
def new_image(username):
   return render_template('new_image.html', user=get_user_dao().get_user_by_username(session['username']))


#displays all images for given user
@app.route('/<username>/all_images', methods=['GET'])
@requires_auth
def user_images(username):
   contents = list_files("edu.au.cc.m6.python-image-gallery")
   return render_template('all_user_images.html', contents=contents)
     
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



