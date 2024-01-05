import sqlite3 as sq
from pprint import pprint


def create_db():
    with sq.connect("my_books.db") as con:
        cur = con.cursor()

        # cur.execute("DROP TABLE books")  # Удаляет таблицу
        cur.execute("""CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_book TEXT NOT NULL,
        description TEXT,
        year INTEGER
        )""")


def data_output():  # Вывод данных
    with sq.connect("my_books.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM books")
        # result = cur.fetchall()
        # pprint(result)
        # print(type(result))
        for result in cur:
            print(result)
        print(type(result))


def insert_data():
    name_book = input("Введите название книги: ")
    description = input("Введите описание книги: ")
    year = int(input("Введите год выпуска книги: "))

    with sq.connect("my_books.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO books(name_book, description, year) VALUES(?, ?, ?)",
                    (name_book, description, year))


if __name__ == '__main__':
    create_db()
    # data_output()
    # insert_data()
