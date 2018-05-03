import sys
import psycopg2
import json
from io import StringIO

from flask import Flask
import os.path
from dotenv import load_dotenv

from db_modules.books import db_list_books, db_get_book, db_create_book, db_update_book, db_delete_book
from db_modules.token import check_token, create_token, clear_cookie
from db_modules.user import db_create_user
from db_modules.favorites import db_list_favorites

# try:
#     dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
#     load_dotenv(dotenv_path)
# except Error as e:
#     print('error', e)
#     pass

app =  Flask(__name__)

# serving index.html
@app.route("/", methods=['GET'])
def url_for_static():
    return app.send_static_file('index.html')

# serving other resources from static directory
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

@app.route('/books', methods=['GET'])
def list_books():
    return db_list_books()

@app.route('/books/<id>', methods=['GET'])
def get_book(id):
    return db_get_book(id)

@app.route('/books', methods=['POST'])
def post_book():
    return db_create_book()

@app.route('/books/<id>', methods=['PATCH'])
def patch_book(id):
    return db_update_book(id)

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    return db_delete_book(id)

@app.route('/token', methods=['GET'])
def get_token():
    return check_token()

@app.route('/token', methods=['POST'])
def post_token():
    return create_token()

@app.route('/token', methods=['DELETE'])
def delete_token():
    return clear_cookie()

@app.route('/users', methods=['POST'])
def post_user():
    return db_create_user()

@app.route('/favorites', methods=['GET'])
def get_favorites():
    return db_list_favorites()

if __name__ == '__main__':
    app.run()
