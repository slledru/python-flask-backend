import sys
import psycopg2
import json
from io import StringIO

from flask import Flask, url_for, request, Response
from flask_jwt import JWT, jwt_required, current_identity
import os.path
from dotenv import load_dotenv

from db_modules.books import db_list_books, db_get_book
from db_modules.token import check_token, create_token
from db_modules.user import create_user

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

app =  Flask(__name__)
app.debug = True

DSN = 'dbname=bookshelf_dev'

print(sys.argv)

if len(sys.argv) > 3:
    DSN = sys.argv[3]
    print(DSN)

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
    return db_list_books(DSN)

@app.route('/books/<id>', methods=['GET'])
def get_book(id):
    return db_get_book(DSN, id)

@app.route('/token', methods=['GET'])
def get_token():
    return check_token(DSN)

@app.route('/token', methods=['POST'])
def post_token():
    return create_token(DSN)

@app.route('/users', methods=['POST'])
def post_user():
    return create_user(DSN)

if __name__ == '__main__':
    app.run(debug=True)

# @app.route("/messages", methods=['GET'])
# def list():
#     print("Opening connection using dsn:", DSN)
#     conn = psycopg2.connect(DSN)
#     print("Encoding for this connection is", conn.encoding)
#
#     curs = conn.cursor()
#     print("Extracting the rows ...")
#     curs.execute("SELECT * FROM messages order by id desc")
#     io = StringIO()
#     data = list()
#     for row in curs.fetchall():
#         data.insert(0, dict(id=row[0], name=row[1], message=row[2]))
#     json.dump(data, io)
#     curs.close()
#     conn.close()
#     return io.getvalue()
#
# @app.route("/messages/<id>", methods=['GET'])
# def getById(id):
#     return id
#
# @app.route("/messages/<id>", methods=['PATCH'])
# def patchById(id):
#     io = StringIO()
#     json.dump(request.get_json(), io)
#     return 'patch ' + id + ' ' + io.getvalue()

# conn = psycopg2.connect(DSN)
# curs = conn.cursor()
# curs.execute("""
#     insert into messages (name, message)
#     values (%s, %s);
#     """,
#     ("Test 4", "Test 4 Message"))
# conn.commit()
# curs.close()
# conn.close()
