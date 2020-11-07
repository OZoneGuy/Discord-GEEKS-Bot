import sqlite3
import sheets_interface

_db = sqlite3.connect('data/mydb.db')

_cursor = _db.cursor()

_cursor.execute("CREATE TABLE IF NOT EXISTS form_responses (timeStamp TEXT, "
                "discord_name TEXT, name_and_program TEXT, alumni INTEGER, "
                "interests TEXT, email TEXT, "
                "PRIMARY KEY(email, discord_name))")


def insert_form_response(time, user_name, name_prog, alumni, interests, email):
    search = 'SELECT * FROM form_responses WHERE email = "{}" OR discord_name = "{}"'.format(email, user_name)
    _cursor.execute(search)
    length = len(_cursor.fetchall())
    if length == 0:
        alum = 1 if alumni else 0
        print('Recording response {}'.format(user_name))
        sql = 'INSERT INTO form_responses (timeStamp, discord_name, name_and_program, alumni, interests, email) VALUES("{}", "{}", "{}", {}, "{}", "{}")'.format(time, user_name, name_prog.replace('"', ''), alum, interests, email)
        _cursor.execute(sql)
        _db.commit()
        return


def is_registered(user_name, user_disc):
    update()
    _cursor.execute("SELECT * FROM form_responses "
                    "WHERE discord_name LIKE '{}%' "
                    "OR discord_name LIKE '%{}'".format(user_name, user_disc))
    if len(_cursor.fetchall()) > 0:
        return True
    else:
        return False


def update():
    sheets_interface.main()
