import sys
import psycopg2
import json
from io import StringIO

from flask import Flask, url_for, request, Response
import os.path

app =  Flask(__name__)

DSN = 'dbname=g_message_test'

print(sys.argv)

if len(sys.argv) > 3:
    DSN = sys.argv[3]
    print(DSN)

@app.route("/", methods=['GET'])
def url_for_static():
    return app.send_static_file('index.html')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)

@app.route("/messages", methods=['GET'])
def list():
    print("Opening connection using dsn:", DSN)
    conn = psycopg2.connect(DSN)
    print("Encoding for this connection is", conn.encoding)

    curs = conn.cursor()
    print("Extracting the rows ...")
    curs.execute("SELECT * FROM messages order by id desc")
    io = StringIO()
    data = list()
    for row in curs.fetchall():
        data.insert(0, dict(id=row[0], name=row[1], message=row[2]))
    json.dump(data, io)
    curs.close()
    conn.close()
    return io.getvalue()

@app.route("/messages/<id>", methods=['GET'])
def getById(id):
    return id

@app.route("/messages/<id>", methods=['PATCH'])
def patchById(id):
    io = StringIO()
    json.dump(request.get_json(), io)
    return 'patch ' + id + ' ' + io.getvalue()

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
