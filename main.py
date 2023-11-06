import sqlite3 as sq

with sq.connect("my_books.db") as con:
    cur = con.cursor()

    cur.execute("""
    """)


