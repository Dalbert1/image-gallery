from flask import Flask, render_template
from tools.db import *
app = Flask(__name__)

@app.route('/')
def admin_interface():
        connect()
        user_data = listUsers().fetchall()
        return render_template('admin.html', user_data=user_data)
