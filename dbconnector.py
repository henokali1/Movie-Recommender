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

# All MSO's
# def get_all_msos():
#     cnx = mysql.connector.connect(user='root', password='@tmsqe!1321', host='127.0.0.1', database='MSO')
#     cur = cnx.cursor(dictionary=True)
#     cur.execute("SELECT * FROM tsd_mso_form ORDER BY id DESC")
#     r = cur.fetchall()
#     cnx.commit()
#     cur.close()
#     cnx.close()
#     return r

# Returns MSO's by the given email
# def all_msos_by_user(user):
#     cnx = mysql.connector.connect(user='root', password='@tmsqe!1321', host='127.0.0.1', database='MSO')
#     cur = cnx.cursor(dictionary=True)
#     query = "SELECT * FROM tsd_mso_form WHERE posted_by=%s ORDER BY id DESC"
#     cur.execute(query, (user,))
#     r = cur.fetchall()
#     cur.close()
#     cnx.close()
#     return r

#print(delete_mso(7))