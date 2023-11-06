import sqlite3 as sq

con = sq.connect("my_books.db")
cur = con.cursor()

cur.execute("""
""")


con.close()