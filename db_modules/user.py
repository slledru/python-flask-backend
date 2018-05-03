from flask import Response, request
from utilities.jwt_util import get_hashed_password, build_response
from utilities.db_util import get_database_connection
from utilities.web_util import build_response
import psycopg2
import json
from io import StringIO

def db_create_user():
    if (request.data == b''):
        return Response(status=401)
    dataDict = json.loads(request.data)
    email = dataDict['email']
    password = dataDict['password']
    first_name = dataDict['firstName']
    last_name = dataDict['lastName']
    if (email == None):
        abort(401)
    if (password == None):
        abort(401)
    if (first_name == None):
        abort(401)
    if (last_name == None):
        abort(401)
    hashed_password = get_hashed_password(password)
    dictionary = {}
    conn = get_database_connection()
    curs = conn.cursor()
    try:
        curs.execute("""
            insert into users (first_name, last_name, email, hashed_password)
            values (%s, %s, %s, %s);
            """,
            (first_name, last_name, email, hashed_password))
        dictionary['status'] = 200
        dictionary['firstName'] = first_name
        dictionary['lastName'] = last_name
        dictionary['email'] = email
        dictionary['hashedPassword'] = hashed_password
    except psycopg2.Error as e:
        print('err', e)
        dictionary = {}
        dictionary['status'] = 400
        pass
    conn.commit()
    curs.close()
    conn.close()
        return build_response(dictionary, email)
