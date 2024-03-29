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
        title TEXT UNIQUE NOT NULL,
        author_id INTEGER,
        theme TEXT NOT NULL,
        description TEXT,
        year INTEGER,
        language TEXT,
        file_path TEXT NOT NULL,
        FOREIGN KEY (author_id) REFERENCES authors(author_id)
        )""")


# Функция для валидации ID книги
def validate_book_id(book_id):
    try:
        with sq.connect("my_books.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM books WHERE book_id = ?", (book_id,))
            book = cur.fetchone()
            if book:
                return True  # ID книги найден в базе данных
            else:
                return False  # ID книги не найден в базе данных
    except sq.Error as error:
        print("Ошибка при выполнении запроса в базе данных:", error)
        return False  # Ошибка при выполнении запроса


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
def get_book_path(title):
    project_folder = os.path.dirname(os.path.abspath(__file__))  # Получаем абсолютный путь к папке проекта
    book_path = os.path.join(project_folder, books_folder, title)  # Формируем абсолютный путь до файла книги
    return book_path


# Функция для добавления данных книг в таблицу "books"
def add_book(author_name):
    title = input("Введите название книги: ")
    theme = input("Введите тематику книги (например, 'программирование на Python'): ")
    description = input("Введите описание книги: ")
    year = int(input("Введите год выпуска книги: "))
    language = input("Введите язык книги ('ru' или 'en'): ")
    file_path = get_book_path(title)
    author_id = get_author_id(author_name)

    con = sq.connect("my_books.db")
    cur = con.cursor()

    try:
        cur.execute(
            "INSERT INTO books (title, author_id, theme, description, year, language, file_path) VALUES (?, ?, ?, ?, "
            "?, ?, ?)",
            (title, author_id, theme, description, year, language, file_path))
        con.commit()
        con.close()
        return title
    except sq.IntegrityError as e:
        print("Ошибка: Книга с таким названием и автором уже существует в базе данных.")
        con.close()
        return None
    except sq.Error as e:
        print("Ошибка при добавлении книги в базу данных:", e)
        con.close()
        return None


# Обновление записей а БД
def update_book(attempts=3):
    if attempts <= 0:
        print("Достигнуто максимальное количество попыток. Программа завершается.")
        return
    book_id = input("Введите ID книги: ")
    if validate_book_id(book_id):
        new_title = input("Введите новое название: ")
        new_author = input("Введите нового автора: ")
        new_description = input("Введите новое описание: ")
        try:
            with sq.connect("my_books.db") as con:
                cur = con.cursor()
                cur.execute("UPDATE books SET title = ?, author_id = ?, description = ? WHERE book_id = ?",
                            (new_title, new_author, new_description, book_id))
                con.commit()
                print("Информация о книге успешно обновлена в базе данных.")
        except sq.Error as error:
            print("Ошибка при обновлении информации о книге в базе данных:", error)
    else:
        print("Книга с указанным ID не найдена в базе данных.")
        update_book(attempts - 1)


# Удаление книги
def delete_book():
    book_id = input("Введите ID книги которую вы хотите удалить: ")
    if validate_book_id(book_id):
        try:
            with sq.connect("my_books.db") as con:
                cur = con.cursor()
                # Удаляем связанные данные из другой таблицы (authors)
                cur.execute("DELETE FROM authors WHERE author_id IN (SELECT author_id FROM books WHERE book_id = ?)",
                            (book_id,))
                cur.execute("DELETE FROM books WHERE book_id = ?", (book_id,))
                con.commit()
                print("Книга и связанные с ней данные успешно удалена из базы данных.")
        except sq.Error as error:
            print("Ошибка при удалении книги из базы данных:", error)
    else:
        print("Книга с указанным ID не найдена в базе данных.")


# Выбираем по теме
def select_by_topic():
    theme = input("Введите тему: ")
    with sq.connect("my_books.db") as con:
        cur = con.cursor()
        cur.execute("SELECT book_id, title  FROM books WHERE theme = ?", (theme,))
        results = cur.fetchall()
        for row in results:
            pprint.pprint(row)


def data_output():  # Вывод данных всех
    with sq.connect("my_books.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM books")
        results = cur.fetchall()
        for row in results:
            pprint.pprint(row)


def data_output_id_title():  # Вывод id и title
    with sq.connect("my_books.db") as con:
        cur = con.cursor()
        cur.execute("SELECT book_id, title  FROM books")
        results = cur.fetchall()

        for idx, row in enumerate(results, 1):
            print(f"{idx}. ID: {row[0]}, Название книги: {row[1]}")


def menu():
    print("Это программа 'Моя библиотека'")
    print("""
   ' Вывести все о книгах: 1',
   'Добавить книгу: 2',
   'Вывести название всех книг: 3',
   'Вывести все книги по теме: 4',
   'Обновить информацию о книге: 5',
   'Удалить книгу: 6'
    """)


def main():
    menu()
    option = int(input("Введите число: "))
    if option == 1:
        data_output()
    elif option == 2:
        author_name = add_author()
        add_book(author_name)
    elif option == 3:
        data_output_id_title()
    elif option == 4:
        select_by_topic()
    elif option == 5:
        update_book()
    elif option == 6:
        delete_book()
    else:
        print("Вы ввели неправильное число")


if __name__ == '__main__':
    main()
    # create_db()
    # author_name = add_author()
    # add_book(author_name)
    # data_output()
    # insert_data()
