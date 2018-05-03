import jwt
import os
from flask_bcrypt import Bcrypt
from flask import Flask, Response
import json

app = Flask(__name__)

def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, os.getenv('JWT_KEY'), algorithm='HS256')
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def encode_auth_token(email):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            # 'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            # 'iat': datetime.datetime.utcnow(),
            'sub': email
        }
        return jwt.encode(
            payload,
            os.getenv('JWT_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        print('exception', e)
        return e

def get_hashed_password(password):
    bcrypt = Bcrypt(app)
    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    return pw_hash

def match_hashed_password(pw_hash, password):
    bcrypt = Bcrypt(app)
    return bcrypt.check_password_hash(pw_hash.encode('utf-8'), password)

def build_response(data, email):
    response = Response(
        response = json.dumps(data),
        status = 200,
        mimetype = 'application/json'
    )
    if (email != None):
        cookie = encode_auth_token(email)
        response.set_cookie("token", cookie)
    return response
