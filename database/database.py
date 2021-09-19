import sqlite3

database = sqlite3.connect("db.sqlite")
cursor = database.cursor()


def create_users_table():
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER NOT NULL UNIQUE,
        user_name VARCHAR(255),
        true_answer INTEGER DEFAULT 0,
        false_answer INTEGER DEFAULT 0
    )""")


def create_tables():
    print("Создание таблиц.")
    create_users_table()
    database.commit()
