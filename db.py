import sqlite3

db = sqlite3.connect("bot.sqlite")
cursor = db.cursor()


def add_user(message):
    cursor.execute("SELECT id FROM user WHERE id=?",(message.chat.id,))
    user = cursor.fetchone()
    if not user:
        cursor.execute("INSERT INTO user VALUES(?,?,?,?)",(message.chat.id,"name","age","city",))
        db.commit()
    else:
        pass


def add_user_name(message):
    cursor.execute("UPDATE user SET name=? WHERE id=?",(message.text, message.chat.id,))
    db.commit()


def add_user_age(message):
    cursor.execute("UPDATE user SET age=? WHERE id=?",(message.text, message.chat.id,))
    db.commit()


def add_user_city(message):
    cursor.execute("UPDATE user SET city=? WHERE id=?",(message.text, message.chat.id,))
    db.commit()


def log(message):
    cursor.execute("INSERT INTO logs VALUES(?,?)",(message.chat.id,message.text,))
    db.commit()
