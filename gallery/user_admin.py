from flask import Flask, render_template, redirect, url_for, request

from tools.db import *

app = Flask(__name__)

@app.route('/')
def load_admin():
        return redirect(url_for('admin_interface'))

@app.route('/admin')
def admin_interface():
        connect()
        user_data = listAllNoPass().fetchall()
        return render_template('admin.html', user_data=user_data)

@app.route('/admin/newUser')
def new_user_interface():
        return render_template('new_user.html')

@app.route('/admin/modifyUser/<username>/<full_name>')
def modify_user(username, full_name):
        return render_template('modifyUser.html', username=username, full_name=full_name)

@app.route('/admin/commitEdit', methods=['POST'])
def commit_edit():
        connect()
        userToEdit = [request.form['username'], request.form['new_pass'], request.form['new_name']]
        editUser(userToEdit)
        return render_template('modifyUser.html', username=userToEdit[0], full_name=userToEdit[2])

@app.route('/admin/commitDelete', methods=['POST'])
def commit_delete():
        connect()
        deleteUser(request.form['username'])
        return redirect(url_for('admin_interface'))

@app.route('/admin/commitNewUser', methods=['POST'])
def commit_new_user():
        new_account = [request.form['username'], request.form['new_pass'], request.form['new_fullname']]
        connect()
        if(checkExists(new_account[0]) == False):
                insertUser(new_account)
        return redirect(url_for('admin_interface'))
