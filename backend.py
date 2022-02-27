import sqlite3

def connect():
    """
    Checks if book table exists, if not, then it creates the table
    """
    con = sqlite3.connect("books.db")#it connects to the database, opening it
    cursor = con.cursor()#You use cursor to execute commands to the data base
    cursor.execute("CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY, title text, author text, year integer, isbn integer)")#if book isnt in db, create the table
    con.commit()#saves the changes
    con.close()#closes the db


def view():
    """
    it will return all the rows in book table
    """
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM book")
    rows = cur.fetchall()   #it retrievies all the rows in a query
    conn.close()
    return rows

def search(title="", author="", year="", isbn=""):
    """
    given title author year and isbn, returns rows with matching rows that contain any of them
    """
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM book WHERE title=? OR author=? OR year=? OR isbn=?", (title, author, year, isbn))
    row = cursor.fetchall()
    conn.close()
    if row == []:
        return 0
    return row

def insert(title, author, year, isbn):
    """
    Given a title, author, year, and isbn as paramaters, it will insert these into the book table
    """
    con = sqlite3.connect("books.db")
    cursor = con.cursor()
    if search(title, author) != 0:
        return 0
    cursor.execute("INSERT INTO book VALUES (NULL, ?, ?, ?, ?)", (title, author, year, isbn))
    con.commit()
    con.close()

def delete(id):
    """
    given an id, it will delete the row from book
    """
    con = sqlite3.connect("books.db")
    cursor = con.cursor()
    cursor.execute("DELETE FROM book WHERE id=?", (id,))
    con.commit()
    con.close()


def update(id, title, author, year, isbn):
    """
    given an id, title, author, year, and isbn, it will updates the row with the id given, with the title author year isbn given
    """
    con = sqlite3.connect("books.db")
    cursor = con.cursor()
    cursor.execute("UPDATE book SET title=?, author=?, year=?, isbn=? WHERE id=?", (title, author, year, isbn, id))
    con.commit()
    con.close()

connect()

