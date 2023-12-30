import sqlite3 as sql
from flask import g

# sql.register_adapter(bool, int)
# sql.register_converter("BOOLEAN", lambda v: bool(int(v)))

DATABASE = 'wiz_flask.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sql.connect(DATABASE)
        db.row_factory = sql.Row
    return db


def close_db():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    cur = db.cursor()

    cur.execute('''
CREATE TABLE IF NOT EXISTS "bulbs" (
    "IP"	TEXT PRIMARY KEY,
    "NAME"	TEXT,
    "STATE"	INTEGER,
    "SCENE_ID"	INTEGER,
    "SCENE"	TEXT
)
    ''')
    cur.close()
    db.commit()


def add_bulb(ip):
    db = get_db()
    cur = db.cursor()
    cur.execute("select * from bulbs where IP=?", (ip,))
    bulb = cur.fetchone()
    cur.close()
    if not bulb:
        cur = db.cursor()
        cur.execute("insert into bulbs(IP, NAME) values (?, ?)", (ip, ip))
        cur.close()
        db.commit()


def get_all_bulbs():
    db = get_db()
    cur = db.cursor()
    cur.execute("select * from bulbs order by NAME")
    bulbs = cur.fetchall()
    cur.close()
    return bulbs


def get_online_bulbs():
    db = get_db()
    cur = db.cursor()
    cur.execute("select * from bulbs where STATE >= 0 order by NAME")
    bulbs = cur.fetchall()
    cur.close()
    return bulbs


def get_bulb(ip):
    db = get_db()
    cur = db.cursor()
    cur.execute("select * from bulbs where IP=?", (ip,))
    bulb = cur.fetchone()
    cur.close()
    return bulb


def edit_bulb(ip, name):
    db = get_db()
    cur = db.cursor()
    cur.execute("update bulbs set NAME=? where IP=?", (name, ip))
    cur.close()
    db.commit()


def update_bulb_state(ip, state, scene_id, scene):
    db = get_db()
    cur = db.cursor()
    cur.execute("update bulbs set STATE=?, SCENE_ID=?, SCENE=? where IP=?", (state, scene_id, scene, ip))
    cur.close()
    db.commit()


def update_bulb_down(ip):
    db = get_db()
    cur = db.cursor()
    cur.execute("update bulbs set STATE=? where IP=?", (-1, ip))
    cur.close()
    db.commit()


def delete_bulb(ip):
    db = get_db()
    cur = db.cursor()
    cur.execute("delete from bulbs where IP=?", (ip,))
    cur.close()
    db.commit()
