from flask import Response, request
from db_modules.jwt_util import decode_auth_token, encode_auth_token, get_hashed_password, match_hashed_password
import psycopg2
import json
from io import StringIO

def check_token(DSN):
    token = request.cookies.get('token')
    if (token != None):
        payload = decode_auth_token(token)
        print(payload)
        return Response("true", status=200, mimetype='application/json')
    else:
        return Response("false", status=200, mimetype='application/json')

def create_token(DSN):
    print(request.data)
    if (request.data == b''):
        return Response(status=401)
    dataDict = json.loads(request.data)
    email = dataDict['email']
    password = dataDict['password']
    if (email == None):
        abort(401)
    if (password == None):
        abort(401)
    dictionary = find_user_by_email(DSN, email, password)
    print(dictionary)
    io = StringIO()
    json.dump(dictionary, io)
    return io.getvalue()
    # if (dictionary['status'] == 200):
    #     return Response("true", status=200, mimetype='application/json')
    # else:
    #     return Response(status=dictionary['status'])

def find_user_by_email(DSN, email, password):
    print(email)
    dictionary = {}
    conn = psycopg2.connect(DSN)
    curs = conn.cursor()
    try:
        curs.execute("SELECT * FROM users where email='%s'" % email)
        if (curs.rowcount == 1):
            dictionary['status'] = 200
            for row in curs.fetchall():
                dictionary['first_name'] = row[1]
                dictionary['last_name'] = row[2]
                dictionary['email'] = row[3]
                dictionary['hashed_password'] = row[4]
                print(row[4], dictionary['hashed_password'].encode('utf-8'))
            if (not match_hashed_password(dictionary['hashed_password'], password)):
                dictionary = {}
                dictionary['status'] = 401
                dictionary['message'] = 'Unable to authenticate user'
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
