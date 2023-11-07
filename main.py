import sqlite3 as sq

with sq.connect("my_books.db") as con:
    cur = con.cursor()

    # cur.execute("DROP TABLE books")  # Удаляет таблицу
    cur.execute("""CREATE TABLE IF NOT EXISTS books (
    book_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name_book TEXT NOT NULL,
    description TEXT,
    year INTEGER
    )""")


