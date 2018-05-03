from flask import Flask, Response, request
import psycopg2
import json
from utilities.db_util import get_database_connection
from utilities.web_util import build_response

def db_list_books():
    conn = get_database_connection()
    print("Encoding for this connection is", conn.encoding)

    curs = conn.cursor()
    print("Extracting the rows ...")
    curs.execute("SELECT * FROM books order by title")
    data = list()
    for row in curs.fetchall():
        # print(row)
        dictionary = {}
        dictionary['id'] = row[0]
        dictionary['title'] = row[1]
        dictionary['author'] = row[2]
        dictionary['genre'] = row[3]
        dictionary['description'] = row[4]
        dictionary['coverUrl'] = row[5]
        data.insert(0, dictionary)
        # dict(id=row[0], title=row[1], author=row[2], genre=row[3]))
        # data.insert(0, row)
    return build_response(data, None)

def db_get_book(id):
    conn = get_database_connection()
    print("Encoding for this connection is", conn.encoding)

    curs = conn.cursor()
    curs.execute("SELECT * FROM books where id='%s'" % id)
    dictionary = {}
    for row in curs.fetchall():
        print(row)
        dictionary['id'] = row[0]
        dictionary['title'] = row[1]
        dictionary['author'] = row[2]
        dictionary['genre'] = row[3]
        dictionary['description'] = row[4]
        dictionary['coverUrl'] = row[5]
    curs.close()
    conn.close()
    return build_response(dictionary, None)

def db_create_book():
    if (request.data == b''):
        return Response(status=401)
    dataDict = json.loads(request.data)
    if (dataDict['title'] == None):
        return Response(status=401, message='Title must not be blank')
    if (dataDict['author'] == None):
        return Response(status=401, message='Author must not be blank')
    if (dataDict['genre'] == None):
        return Response(status=401, message='Genre must not be blank')
    if (dataDict['description'] == None):
        return Response(status=401, message='Description must not be blank')
    if (dataDict['coverUrl'] == None):
        return Response(status=401, message='Cover URL must not be blank')
    conn = get_database_connection()
    curs = conn.cursor()
    try:
        curs.execute("""
            insert into books (title, author, genre, description, cover_url)
            values (%s, %s, %s, %s, %s);
            """,
            (title, author, genre, description, coverUrl))
        dictionary['status'] = 200
        dictionary['title'] = title
        dictionary['author'] = author
        dictionary['genre'] = genre
        dictionary['description'] = description
        dictionary['coverUrl'] = coverUrl
    except psycopg2.Error as e:
        print('err', e)
        dictionary = {}
        dictionary['status'] = 400
        pass
    conn.commit()
    curs.close()
    conn.close()
    return build_response(dictionary, None)

def db_update_book(id):
    if (request.data == b''):
        return Response(status=401)
    dataDict = json.loads(request.data)
    print("update", dataDict)
    sqlString = 'update books set '
    if (dataDict['title'] != None):
        sqlString += 'title="' + dataDict['title'] + '"'
    if (dataDict['author'] != None):
        if (len(sqlString) > 0):
            sqlString += ', '
        sqlString += 'author="' + dataDict['author'] + '"'
    if (dataDict['genre'] != None):
        if (len(sqlString) > 0):
            sqlString += ', '
        sqlString += 'genre="' + dataDict['genre'] + '"'
    if (dataDict['description'] != None):
        if (len(sqlString) > 0):
            sqlString += ', '
        sqlString += 'description="' + dataDict['description'] + '"'
    if (dataDict['coverUrl'] != None):
        if (len(sqlString) > 0):
            sqlString += ', '
        sqlString += 'cover_url="' + dataDict['coverUrl'] + '"'
    sqlString += ' where id = ' + id
    print(sqlString)
    conn = get_database_connection()
    curs = conn.cursor()
    try:
        curs.execute(sqlString)
        dictionary = {}
        for row in curs.fetchall():
            print(row)
            dictionary['id'] = row[0]
            dictionary['title'] = row[1]
            dictionary['author'] = row[2]
            dictionary['genre'] = row[3]
            dictionary['description'] = row[4]
            dictionary['coverUrl'] = row[5]
    except psycopg2.Error as e:
        print('err', e)
        dictionary = {}
        dictionary['status'] = 400
        pass
    conn.commit()
    curs.close()
    conn.close()
    return build_response(dictionary, None)

def db_delete_book(id):
    dictionary = {}
    conn = get_database_connection()
    curs = conn.cursor()
    try:
        curs.execute("DELETE FROM books where id='%s'" % id)
        dictionary['status'] = 200
    except psycopg2.Error as e:
        print('err', e)
        dictionary['status'] = 400
        pass
    conn.commit()
    curs.close()
    conn.close()
    return build_response(dictionary, None)
