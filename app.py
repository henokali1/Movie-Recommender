from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from werkzeug.utils import secure_filename
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
from functools import wraps
import dbconnector as db
import time
import os

UPLOAD_FOLDER = '/root/project_files/Movie-Recommender/static/img/movie_imgs/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'waleflask'
app.config['MYSQL_DB'] = 'movie_rec'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)
app.config['DEBUG'] = True


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_name(fn):
    return str(int(time.time()))+fn[-4:]


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


# All Movies
@app.route('/all')
def all():
    all_movies = db.get_all_movies()
    return render_template('all.html', all_movies=all_movies)


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

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = get_file_name(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))

        print('title: {}\n genre: {}\n release_year: {}\n rating: {}\n description: {}\n trailer_url: {}\n filename: {}'.format(
            title, genre, release_year, rating, description, trailer_url, filename))
        
        sql = "INSERT INTO movies(title, genre, release_year, rating, description, trailer_url, thumbnail) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        data = (title, genre, release_year, rating, description, trailer_url, filename)
        # Save into db
        db.save(sql, data)
        
        return render_template('new_movie.html')


    return render_template('new_movie.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # app.run()
