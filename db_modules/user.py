from flask import Response, request
from db_modules.jwt_util import encode_auth_token, get_hashed_password
import psycopg2
import json
from io import StringIO

def create_user(DSN):
    print(request.data)
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
    conn = psycopg2.connect(DSN)
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
        print(e)
        dictionary = {}
        dictionary['status'] = 404
        pass
    conn.commit()
    curs.close()
    conn.close()
    if (dictionary['status'] == 200):
        Response.set_cookie('token', encode_auth_token(email))
        return Response(dictionary, status=200, mimetype='application/json')
    else:
        io = StringIO()
        json.dump(dictionary, io)
        return io.getvalue()
