import mysql.connector
from mysql.connector import Error




# Save new data into the db.
def save(sql, data):
    cnx = mysql.connector.connect(user='root', password='waleflask', host='127.0.0.1', database='movie_rec')
    cur = cnx.cursor()
    cur.execute(sql, data)
    cnx.commit()
    cur.close()
    cnx.close()

# All Movies
def get_all_movies():
    cnx = mysql.connector.connect(user='root', password='waleflask', host='127.0.0.1', database='movie_rec')
    cur = cnx.cursor(dictionary=True)
    # cur.execute("SELECT * FROM tsd_mso_form ORDER BY id DESC")
    # cur.execute("SELECT * FROM movies ORDER BY rating")
    cur.execute("SELECT * FROM movies")
    r = cur.fetchall()
    cnx.commit()
    cur.close()
    cnx.close()
    return r

# Movie Details
def get_movie_details(id):
	cnx = mysql.connector.connect(user='root', password='waleflask', host='127.0.0.1', database='movie_rec')
	cur = cnx.cursor(dictionary=True)
	cur.execute("SELECT * FROM movies WHERE id=" + str(id))
	r = cur.fetchall()
	cnx.commit()
	cur.close()
	cnx.close()
	return r[0]

# Movie Details by Title
def get_movie_details_t(title):
    cnx = mysql.connector.connect(user='root', password='waleflask', host='127.0.0.1', database='movie_rec')
    cur = cnx.cursor(dictionary=True)
    cur.execute("SELECT * FROM movies WHERE title = %s", [title])
    r = cur.fetchall()
    cnx.commit()
    cur.close()
    cnx.close()
    try:
        return r[0]
    except:
        pass


# Get user psw by email
def user_psw(email):
    cnx = mysql.connector.connect(user='root', password='waleflask', host='127.0.0.1', database='movie_rec')
    cur = cnx.cursor()

    cur.execute("SELECT password FROM USERS WHERE email = %s", [email])
    r = cur.fetchone()
    cur.close()
    cnx.close()
    return r[0].encode('utf8')

# Delete Movie by ID
def delete_movie(id):
    query = "DELETE FROM movies WHERE id = %s"
    # connect to the database server
    cnx = mysql.connector.connect(user='root', password='waleflask', host='127.0.0.1', database='movie_rec')
    cur = cnx.cursor()
 
    try:
        # execute the query
        cur.execute(query, (id,))
 
        # accept the change
        cnx.commit()
    except Error as error:
        print(error)
 
    finally:
        cur.close()
        cnx.close()

# Returns rating of a given movie title
def get_rating(title):
    cnx = mysql.connector.connect(user='root', password='waleflask', host='127.0.0.1', database='movie_rec')
    cur = cnx.cursor()

    cur.execute("SELECT rating FROM movies WHERE title = %s", [title])
    r = cur.fetchone()
    cur.close()
    cnx.close()
    print(title, r)
    return r[0]

# Returns last watched movie for a given user(email)
def get_last_watched(email):
    cnx = mysql.connector.connect(user='root', password='waleflask', host='127.0.0.1', database='movie_rec')
    cur = cnx.cursor()

    cur.execute("SELECT last_watched FROM USERS WHERE email=%s", [email])
    r = cur.fetchone()
    cur.close()
    cnx.close()
    print(r)
    return r[0]

