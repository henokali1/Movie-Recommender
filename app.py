from flask import Flask, render_template, flash, redirect, url_for, session, request, logging, Blueprint
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from flask_paginate import Pagination, get_page_parameter, get_page_args
from werkzeug.utils import secure_filename
from passlib.hash import sha256_crypt
from flask_mysqldb import MySQL
import knn_recommender as kr
from functools import wraps
import dbconnector as db
import time
import os

UPLOAD_FOLDER = '/root/project_files/Movie-Recommender/static/img/movie_imgs/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
mod = Blueprint('users', __name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'seckey!@#$%'
# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'waleflask'
app.config['MYSQL_DB'] = 'movie_rec'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
# init MYSQL
mysql = MySQL(app)
app.config['DEBUG'] = True


# Returns video id of a given YouTube URL
def get_video_id(yt_url):
    sp = yt_url.split('/')
    if sp[2] == 'youtu.be':
        return sp[-1]
    elif sp[2] == 'www.youtube.com':
        return sp[-1][8:]
    else:
        return -1


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_name(fn):
    return str(int(time.time()))+fn[-4:]

# Get curret user info
def current_user():
    return session['email'].encode('utf8')

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


@app.route('/movie/<string:id>/')
@is_logged_in
def movie_trailer(id):
    movie = db.get_movie_details(id)
    # video_id = get_video_id(movie['url'])
    return render_template('trailer.html', movie=movie, user = str(session['email']))

# Edit Movie Details
@app.route('/mv/<string:title>/', methods=['GET', 'POST'])
@is_logged_in
def movie_detail(title):
	# Update the MSO in the database
	sql = "UPDATE USERS  SET last_watched=%s  WHERE email=%s"
	data = (title, session['email']) 

	db.save(sql, data)
	r = kr.get_movie_rec(str(title))
	r_movs = []
	for i in r:
		r_movs.append({'title': i, 'rating': db.get_rating(i)})
	return render_template('movie_detail.html', title=title, movie_recommendation=r, r_movs=r_movs, user = str(session['email']))



# Edit Movie Details
@app.route('/edit/<string:id>/', methods=['GET', 'POST'])
@is_logged_in
def edit(id):
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
        
        # Update the MSO in the database
        sql = "UPDATE movies  SET title=%s, genre=%s, release_year=%s, rating=%s, description=%s, trailer_url=%s, thumbnail=%s  WHERE id=%s"
        data = (title, genre, release_year, rating, description, trailer_url, filename, int(id)) 

        db.save(sql, data)


    movie = db.get_movie_details(id)
    return render_template('edit.html', movie=movie, user=str(session['email']))

@app.route('/', methods=['GET', 'POST'])
@is_logged_in
def index():
    return redirect(url_for('all'))


# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('user_email')
        password = sha256_crypt.encrypt(str(request.form.get('user_password')))
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
        # Get Form Fields
        email = request.form.get('user_email')
        password_candidate = request.form.get('user_password')
        # Get user by email
        password = db.user_psw(email)

        if len(password) > 0:
            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['email'] = email

                lw = db.get_last_watched(session['email'])
                if lw == '':
                    return redirect(url_for('all'))
                else:
                    return redirect(url_for('rec'))

                
            else:
                error = 'Invalid login'
                return render_template('login.html', msg=error)
        else:
            error = 'User not found'
            return render_template('login.html', msg=error)
    return render_template('login.html')
    
# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    return redirect(url_for('login'))

# Sign In Sign Up
@app.route('/a', methods=['GET', 'POST'])
def a():
    if request.method == 'POST':
        # Get Form Fields
        email = request.form.get('user_email')
        password_candidate = request.form.get('user_password')
        # # Get user by email
        password = db.user_psw(email)

        if len(password) > 0:
            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['email'] = email

                return redirect(url_for('all'))
            else:
                error = 'Invalid login'
                return render_template('signin_signup.html', msg=error)
        else:
            error = 'User not found'
            return render_template('signin_signup.html', msg=error)
    return render_template('signin_signup.html')


# Most Watched
@app.route('/most_watched')
@is_logged_in
def most_watched():
    return render_template('most_watched.html')

# users = list(range(100))

def get_movies(offset=0, per_page=22):
	movies = db.get_all_movies()
	return movies[offset: offset + per_page]

def get_movies_m2(movies, offset=0, per_page=22):
	movies = movies
	return movies[offset: offset + per_page]

# All Movies
@app.route('/all')
@is_logged_in
def all():
    user = str(session['email'])
    all_movies = db.get_all_movies()
    
    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(all_movies)
    pagination_movies = get_movies(offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')
    return render_template('all.html', user=user, all_movies=pagination_movies, page=page, per_page=per_page, pagination=pagination,)


# New Movie
@app.route('/new_movie', methods=['GET', 'POST'])
@is_logged_in
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

        
        sql = "INSERT INTO movies(title, genre, release_year, rating, description, trailer_url, thumbnail) VALUES(%s, %s, %s, %s, %s, %s, %s)"
        data = (title, genre, release_year, rating, description, trailer_url, filename)
        # Save into db
        db.save(sql, data)
        
        return render_template('new_movie.html')


    return render_template('new_movie.html')

# Delete Movie through AJAX
@app.route('/delete/<string:id>/', methods=['GET', 'POST'])
@is_logged_in
def delete_movie(id):
    db.delete_movie(id)
    return redirect(url_for('all'))


@app.route('/rec/', methods=['GET', 'POST'])
@is_logged_in
def rec():
    lw = db.get_last_watched(session['email'])
    if lw == '':
        return 'No Data'
    else:
        r = kr.get_movie_rec_m2(lw)
        mvs = []
        for i in r:
            detail = db.get_movie_details_t(i)
            if detail == None:
                pass
            else:
                mvs.append(detail)

    user = str(session['email'])
    all_movies = mvs
    
    page, per_page, offset = get_page_args(page_parameter='page', per_page_parameter='per_page')
    total = len(all_movies)
    pagination_movies = get_movies_m2(mvs, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total, css_framework='bootstrap4')

    return render_template('rec.html', mvs=str(mvs), user=user, all_movies=pagination_movies, page=page, per_page=per_page, pagination=pagination,)


        #return str(mvs)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
    # app.run()
