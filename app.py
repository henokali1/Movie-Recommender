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
app.config['DEBUG'] = True


# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# Register Form Class
# class RegisterForm(Form):
#     email = StringField('Email', [validators.Length(min=1, max=50)])
#     password = PasswordField('Password', [
#         validators.DataRequired(),
#         validators.EqualTo('confirm', message='Passwords do not match')
#     ])
#     confirm = PasswordField('Confirm Password')


# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    print(form)
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        print(email, password)
        # Create cursor
        cur = mysql.connection.cursor()

        # Execute query
        cur.execute("INSERT INTO USERS(email, password) VALUES(%s, %s)", (email, password))

        # Commit to DB
        mysql.connection.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
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

# Most Watched
@app.route('/most_watched')
def most_watched():
    return render_template('most_watched.html')


# New Movie
@app.route('/new_movie', methods=['GET', 'POST'])
def new_movie():
	if request.method == 'POST':
		title = request.form.get('movie_title')
		genre = request.form.get('genre')
		release_year = request.form.get('release_year')
		rating = request.form.get('rating')
		description = request.form.get('description')
		trailer_url = request.form.get('trailer_url')
		print('title: {}\n genre: {}\n release_year: {}\n rating: {}\n description: {}\n trailer_url: {}'.format(
			title, genre, release_year, rating, description, trailer_url))
		return render_template('new_movie.html')


	return render_template('new_movie.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # app.run()
