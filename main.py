import sqlite3 as sq

with sq.connect("my_books.db") as con:
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS books (
    name_book TEXT,
    description TEXT,
    year INTEGER
    )""")


