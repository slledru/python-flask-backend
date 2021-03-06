from flask import Response, request
import psycopg2
import json
from io import StringIO
from utilities.jwt_util import decode_auth_token, encode_auth_token
from utilities.db_util import find_user_by_email, get_database_connection
from utilities.web_util import build_response, build_array_response

def is_authorized():
    token = request.cookies.get('token')
    if (token != None):
        payload = decode_auth_token(token)
        return payload
    else:
        return None

def db_get_favorite_sql_string(user_id):
    sqlString = """SELECT books.author as author,
        books.cover_url as coverUrl,
        books.description as description,
        books.genre as genre,
        books.title as title,
        favorites.book_id as bookId,
        favorites.user_id as userId,
        favorites.id as id
        FROM favorites
        INNER JOIN books on books.id =  favorites.book_id
        INNER JOIN users on users.id = favorites.user_id
        where users.id = %s""" % user_id
    return sqlString

def db_list_favorites():
    payload = is_authorized()
    if (payload != None):
        dictionary = find_user_by_email(payload)
        if (dictionary['status'] == 200):
            conn = get_database_connection()
            print("Encoding for this connection is", conn.encoding)
            user_id = dictionary['id']
            curs = conn.cursor()
            print("Extracting the rows ...")
            sqlString = db_get_favorite_sql_string(user_id)
            curs.execute(sqlString)
            response = Response(json.dumps({}), status=200)
            if (curs.rowcount > 0):
                data = list()
                for row in curs.fetchall():
                    # print(row)
                    dictionary = {}
                    dictionary['author'] = row[0]
                    dictionary['coverUrl'] = row[1]
                    dictionary['description'] = row[2]
                    dictionary['genre'] = row[3]
                    dictionary['title'] = row[4]
                    dictionary['bookId'] = row[5]
                    dictionary['userId'] = row[6]
                    dictionary['id'] = row[7]
                    data.insert(0, dictionary)
                    # dict(id=row[0], title=row[1], author=row[2], genre=row[3]))
                    # data.insert(0, row)
                response = build_array_response(data)

            curs.close()
            conn.commit()
            conn.close()
            return response
        else:
            return build_response(dictionary, None)
    else:
        return Response(status=401)

def db_check_favorite():
    payload = is_authorized()
    if (payload != None):
        dictionary = find_user_by_email(payload)
        if (dictionary['status'] == 200):
            user_id = dictionary['id']
            book_id = request.args.get('bookId')
            conn = get_database_connection()
            print("Encoding for this connection is ", conn.encoding)
            curs = conn.cursor()
            try:
                curs.execute("select * from favorites where book_id={book_id} and user_id={user_id}".format(book_id=book_id, user_id=user_id))
                if (curs.rowcount > 0):
                    for row in curs.fetchall():
                        print('check: ', row)
                        dictionary = {}
                        dictionary['status'] = 200
                        dictionary['id'] = row[0]
                        dictionary['bookId'] = row[1]
                        dictionary['userId'] = row[2]
                    print('dictionary: ', dictionary)
                    response = build_response(dictionary, None)
                else:
                    response = Response("false", status=200)
            except psycopg2.Error as e:
                print('not foun: ', e)
                response = Response("false", status=200)
                pass

            curs.close()
            conn.commit()
            conn.close()
            return response
        else:
            return build_array_response(dictionary, None)
    else:
        return Response(status=401)

def db_add_favorite():
    if (request.data == b''):
        return Response(status=400)
    dataDict = json.loads(request.data)
    payload = is_authorized()
    if (payload != None):
        dictionary = find_user_by_email(payload)
        if (dictionary['status'] == 200):
            user_id = dictionary['id']
            book_id = dataDict['bookId']
            print('user_id: ', user_id)
            print('book_id: ', book_id)
            conn = get_database_connection()
            print("Encoding for this connection is", conn.encoding)
            curs = conn.cursor()
            response = Response("true", status=200)
            try:
                sqlString = "insert into favorites (book_id, user_id) values({book_id}, {user_id}) returning *".format(book_id=book_id, user_id=user_id)
                print('sqlString', sqlString)
                curs.execute(sqlString)
                if (curs.rowcount > 0):
                    for row in curs.fetchall():
                        print('insert: ', row)
                        dictionary = {}
                        dictionary['status'] = 200
                        dictionary['id'] = row[0]
                        dictionary['bookId'] = row[1]
                        dictionary['userId'] = row[2]
                    print('dictionary: ', dictionary)
                    response = build_response(dictionary, None)
                else:
                    print('error - unable to insert')
                    response = Response("false", status=200)
            except psycopg2.Error as e:
                print('error', e)
                response = Response("false", status=200)
                pass

            curs.close()
            conn.commit()
            conn.close()
            return response
        else:
            return build_response(dictionary, None)
    else:
        return Response(status=401)

def db_delete_favorite():
    if (request.data == b''):
        return Response(status=400)
    dataDict = json.loads(request.data)
    payload = is_authorized()
    if (payload != None):
        dictionary = find_user_by_email(payload)
        if (dictionary['status'] == 200):
            user_id = dictionary['id']
            book_id = dataDict['bookId']
            conn = get_database_connection()
            print("Encoding for this connection is", conn.encoding)
            curs = conn.cursor()
            response = Response("true", status=200)
            try:
                curs.execute("delete from favorites where book_id={book_id} and user_id={user_id} returning *".format(book_id=book_id, user_id=user_id))
                for row in curs.fetchall():
                    print('delete: ', row)
            except psycopg2.Error as e:
                print('delete error', e)
                response = Response("false", status=200)
                pass

            curs.close()
            conn.commit()
            conn.close()
            return response
        else:
            return build_response(dictionary, None)
    else:
        return Response(status=401)
