import psycopg2
import json
from io import StringIO

def db_list_books(DSN):
    print("Opening connection using dsn:", DSN)
    conn = psycopg2.connect(DSN)
    print("Encoding for this connection is", conn.encoding)

    curs = conn.cursor()
    print("Extracting the rows ...")
    curs.execute("SELECT * FROM books order by title")
    io = StringIO()
    data = list()
    for row in curs.fetchall():
        print(row)
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
    json.dump(data, io)
    curs.close()
    conn.close()
    return io.getvalue()
