import sqlite3
import sheets_interface

_db = sqlite3.connect('data/mydb.db')

_cursor = _db.cursor()

_cursor.execute("CREATE TABLE IF NOT EXISTS jokes (_id INTEGER PRIMARY KEY AUTOINCREMENT, post_id TEXT, title TEXT, body TEXT, author TEXT)")

# TODO: Add registered field
_cursor.execute("CREATE TABLE IF NOT EXISTS form_responses (timeStamp TEXT, discord_name TEXT, name_and_program TEXT, alumni INTEGER, interests TEXT, email TEXT, PRIMARY KEY(email, discord_name))")

_cursor.execute("CREATE TABLE IF NOT EXISTS user_lvl_n_msgs (_user_id INTEGER PRIMARY KEY, message_cnt INTEGER, level INTEGER)")


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
    sheets_interface.main()
    _cursor.execute('SELECT * FROM form_responses WHERE discord_name LIKE \'{}%\''.format(user_name))
    if len(_cursor.fetchall()) > 0:
        return True
    else:
        return False


def add_message(user_id):
    _cursor.execute('SELECT message_cnt FROM user_lvl_n_msgs WHERE _user_id = {}'.format(user_id))
    data = _cursor.fetchall()
    if len(data) > 0:
        message_cnt = data[0][0]
        new_message_cnt = 1 + message_cnt
        print(new_message_cnt)
        _cursor.execute('UPDATE user_lvl_n_msgs SET message_cnt = {} WHERE _user_id = {}'.format(new_message_cnt, user_id))
        _db.commit()
    else:
        _cursor.execute('INSERT INTO user_lvl_n_msgs (_user_id, message_cnt, level) VALUES({}, {}, {})'.format(user_id, 1, 1))
        _db.commit()


# checks if user is eady for level up
def is_lvl_up(user_id):
    _cursor.execute('SELECT message_cnt, level FROM user_lvl_n_msgs WHERE _user_id = {}'.format(user_id))
    data = _cursor.fetchall()
    if len(data) < 0:
        print('error: user not in table user_lvl_n_msgs')
        return False
    if data[0][0] > messages_req_for_lvl(data[0][1]):
        return True
    return False


def messages_req_for_lvl(cur_lvl):
    return 2**(cur_lvl+1)
    pass


def get_messages(user_id):
    _cursor.execute('SELECT message_cnt FROM user_lvl_n_msgs WHERE _user_id = {}'.format(user_id))
    data = _cursor.fetchone()
    return data[0]


def get_level(user_id):
    _cursor.execute('SELECT level FROM user_lvl_n_msgs WHERE _user_id = {}'.format(user_id))
    data = _cursor.fetchone()
    return data[0]


# adds 1 to level
def lvl_up(user_id):
    _cursor.execute('SELECT level FROM user_lvl_n_msgs WHERE _user_id = {}'.format(user_id))
    lvl = _cursor.fetchone()
    new_lvl = 1 + lvl[0]
    _cursor.execute('UPDATE user_lvl_n_msgs SET level = {} WHERE _user_id = {}'.format(new_lvl, user_id))
    _db.commit()
    print(new_lvl)
