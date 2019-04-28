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
    cur.execute("SELECT * FROM movies WHERE id < 40 ORDER BY id")
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


# Get user psw by email
def user_psw(email):
    cnx = mysql.connector.connect(user='root', password='waleflask', host='127.0.0.1', database='movie_rec')
    cur = cnx.cursor()

    cur.execute("SELECT password FROM USERS WHERE email = %s", [email])
    r = cur.fetchone()
    cur.close()
    cnx.close()
    return r[0].encode('utf8')
