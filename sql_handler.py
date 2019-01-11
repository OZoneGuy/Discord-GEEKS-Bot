import sqlite3
import sheets_interface

_db = sqlite3.connect('mydb.db')

_cursor = _db.cursor()

_cursor.execute("CREATE TABLE IF NOT EXISTS jokes (_id INTEGER PRIMARY KEY AUTOINCREMENT, post_id TEXT, title TEXT, body TEXT, author TEXT)")

#TODO: Add registered field
_cursor.execute("CREATE TABLE IF NOT EXISTS form_responses (timeStamp TEXT, discord_name TEXT, name_and_program TEXT, alumni INTEGER, interests TEXT, email TEXT, PRIMARY KEY(email, discord_name))")


def insert_joke(post_id, title, body, author):
    _cursor.execute('SELECT * FROM jokes WHERE post_id = "' + str(post_id) + '"')
    v = _cursor.fetchall()
    if len(v) is 0:
        _cursor.execute('INSERT INTO jokes(post_id, title, body, author) VALUES(?,?,?,?)', (str(post_id), str(title), str(body), str(author)))
        _db.commit()
        print('inserted joke')
        return
    print("joke already exists")


def get_random_joke():
    _cursor.execute('SELECT * FROM jokes ORDER BY RANDOM() LIMIT 1')
    joke = _cursor.fetchone()
    if joke is None:
        return ['', '', '']
    return [joke[2], joke[3], joke[4], joke[1]]


def insert_form_response(time, user_name, name_prog, alumni, interests, email):
    search = 'SELECT * FROM form_responses WHERE email = "{}" OR discord_name = "{}"'.format(email, user_name)
    _cursor.execute(search)
    length = len(_cursor.fetchall())
    if length == 0:
        print('hello')
        alum = 1 if alumni else 0
        print('Recording response {}'.format(user_name))
        sql = 'INSERT INTO form_responses (timeStamp, discord_name, name_and_program, alumni, interests, email) VALUES("{}", "{}", "{}", {}, "{}", "{}")'.format(time, user_name, name_prog.replace('"', ''), alum, interests, email)
        #print(sql)
        _cursor.execute(sql)
        _db.commit()
        return
    print('Member {} already recorded'.format(user_name))


def is_registered(user_name):
    print(user_name)
    _cursor.execute('SELECT * FROM form_responses WHERE discord_name LIKE \'{}%\''.format(user_name))
    if len(_cursor.fetchall()) > 0:
        return True
    else:
        sheets_interface.main
        _cursor.execute('SELECT * FROM form_responses WHERE discord_name LIKE \'{}%\''.format(user_name))
        if len(_cursor.fetchall()) > 0:
            return True
        else:
            return False
