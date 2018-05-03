from flask import Response, Flask
from utilities.jwt_util import encode_auth_token

def build_response(data, email):
    if (data['status'] == 200):
        response = Response(
            response = json.dumps(data),
            status = 200,
            mimetype = 'application/json'
        )
        if (email != None):
            cookie = encode_auth_token(email)
            response.set_cookie("token", cookie)
        return response
    else:
        return build_error_response(data)

def build_array_response(data):
    response = Response(
        response = json.dumps(data),
        status = 200,
        mimetype = 'application/json'
    )
    return response

def build_error_response(data):
    response = Response(
        response = data['message'],
        status = data['status'],
        mimetype = 'text/plain'
    )
