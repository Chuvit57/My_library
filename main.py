import sqlite3 as sq
import os
import pprint

# Определение относительного пути к папке с книгами
books_folder = "books"


def create_db():
    with sq.connect("my_books.db") as con:
        cur = con.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS authors (
                        author_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        author_name TEXT NOT NULL
                        )""")

        # cur.execute("DROP TABLE books")  # Удаляет таблицу
        cur.execute("""CREATE TABLE IF NOT EXISTS books (
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_book TEXT NOT NULL,
        author_id INTEGER,
        theme TEXT NOT NULL,
        description TEXT,
        year INTEGER,
        language TEXT,
        link TEXT NOT NULL,
        FOREIGN KEY (author_id) REFERENCES authors(author_id)
        )""")


# Функция для добавления данных авторов в таблицу "authors"
def add_author():
    author_name = input("Введите имя автора: ")
    con = sq.connect("my_books.db")
    cur = con.cursor()
    cur.execute("INSERT INTO authors (author_name) VALUES (?)", (author_name,))
    con.commit()
    con.close()
    return author_name


def get_author_id(author_name):
    con = sq.connect("my_books.db")
    cur = con.cursor()
    cur.execute("SELECT author_id FROM authors WHERE author_name = ?", (author_name,))
    author_id = cur.fetchone()[0]
    con.close()
    return author_id


# Функция, чтобы получить абсолютный путь к книге
def get_book_path(name_book):
    project_folder = os.path.dirname(os.path.abspath(__file__))  # Получаем абсолютный путь к папке проекта
    book_path = os.path.join(project_folder, books_folder, name_book)  # Формируем абсолютный путь до файла книги
    return book_path


# Функция для добавления данных книг в таблицу "books"
def add_book(author_name):
    # author_name = input("Введите имя автора книги: ")
    name_book = input("Введите название книги: ")
    theme = input("Введите тематику книги(программ python): ")
    description = input("Введите описание книги: ")
    year = int(input("Введите год выпуска книги: "))
    language = input("Введите на каком языке написана книга 'ru/en': ")
    link = get_book_path(name_book)
    author_id = get_author_id(author_name)

    con = sq.connect("my_books.db")
    cur = con.cursor()
    cur.execute("INSERT INTO books (name_book, author_id, theme, description, year, language, link) VALUES (?, ?, ?, "
                "?, ?, ?, ?)",
                (name_book, author_id, theme, description, year, language, link))
    con.commit()
    con.close()
    return name_book




def data_output():  # Вывод данных
    with sq.connect("my_books.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM books")
        results = cur.fetchall()
        for row in results:
            pprint.pprint(row)


if __name__ == '__main__':
    # create_db()
    # author_name = add_author()
    # add_book(author_name)
    data_output()
    # insert_data()
