from flask import Response, request
import psycopg2
import json
from io import StringIO
from db_modules.jwt_util import decode_auth_token, encode_auth_token

def is_authorized(DSN):
    token = request.cookies.get('token')
    if (token != None):
        payload = decode_auth_token(token)
        print(payload)
    else:
        return None

def db_list_favorites(DSN):
    if (is_authorized(DSN) != None):
        print("Opening connection using dsn:", DSN)
        conn = psycopg2.connect(DSN)
        print("Encoding for this connection is", conn.encoding)
        user_id = request.data['user_id']
        print(request.data)
        curs = conn.cursor()
        print("Extracting the rows ...")
        sqlString = """
                    SELECT books.author as author,
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
                    where users.id = %s
                    """ % user_id
        curs.execute(sqlString)
        io = StringIO()
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
        json.dump(data, io)
        curs.close()
        conn.close()
        return io.getvalue()
    else:
        return Response(status=401)
