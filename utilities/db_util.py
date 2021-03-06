import psycopg2
import urllib.parse as urlparse
import os

def get_database_connection():
    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port

    con = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
                )
    return con

def find_user_by_email(email):
    dictionary = {}
    conn = get_database_connection()
    curs = conn.cursor()
    try:
        curs.execute("SELECT * FROM users where email='%s'" % email)
        if (curs.rowcount == 1):
            dictionary['status'] = 200
            for row in curs.fetchall():
                dictionary['id'] = row[0]
                dictionary['firstName'] = row[1]
                dictionary['lastName'] = row[2]
                dictionary['email'] = row[3]
                dictionary['hashed_password'] = row[4]
        elif (curs.rowcount == 0):
            dictionary['status'] = 404
            dictionary['message'] = 'Unable to authenticate user'
        else:
            dictionary['status'] = 401
            dictionary['message'] = 'Unable to authenticate user'
    except psycopg2.Error as e:
        dictionary['status'] = 404
        dictionary['message'] = 'Unable to authenticate user'
        pass
    conn.commit()
    curs.close()
    conn.close
    return dictionary
