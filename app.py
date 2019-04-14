from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps

app = Flask(__name__)

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'waleflask'
app.config['MYSQL_DB'] = 'movie_rec'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)



@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('user_email')
        psw = request.form.get('user_password')
        print(email, psw)
        return render_template('register.html')
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('user_email')
        psw = request.form.get('user_password')
        print(email, psw)
        return render_template('login.html')
    return render_template('login.html')



if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # app.run()
