from flask import Flask, Response, request
from db_modules.jwt_util import decode_auth_token, match_hashed_password, build_response
import psycopg2
import json
from io import StringIO

def check_token(DSN):
    token = request.cookies.get('token')
    if (token != None):
        payload = decode_auth_token(token)
        dictionary = find_user_by_email(DSN, payload)
        if (dictionary['status'] == 200):
            return Response("true", status=200, mimetype='application/json')
    return Response("false", status=200, mimetype='application/json')

def create_token(DSN):
    print(request)
    if (request.data == b''):
        return Response(status=401)
    dataDict = json.loads(request.data)
    email = dataDict['email']
    password = dataDict['password']
    if (email == None):
        abort(401)
    if (password == None):
        abort(401)
    dictionary = find_user_by_email(DSN, email)
    print(dictionary)
    if (dictionary['status'] == 200):
        if (not match_password(dictionary['hashed_password'], password)):
            dictionary = {}
            dictionary['status'] = 401
            dictionary['message'] = 'Unable to authenticate user'
            return Response(dictionary)
        else:
            return build_response(dictionary, email)
    else:
        return Response(dictionary)

def match_password(hashed_password, password):
    return match_hashed_password(hashed_password, password)

def find_user_by_email(DSN, email):
    dictionary = {}
    conn = psycopg2.connect(DSN)
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
