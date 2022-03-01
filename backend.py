import sqlite3
import requests
from bs4 import BeautifulSoup
import re

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
    print(title)
    print(author)
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

def add_to_db(num):
    """
    takes in a num, and will webscrape books from *num* pages of a library catalog
    """
    titles = []
    authors = []
    for x in range(0,num):
        r = requests.get(f"https://tacoma.bibliocommons.com/v2/search?custom_edit=false&query=audience%3A%22adult%22%20pubyear%3A%5B2021%20TO%202022%5D&searchType=bl&suppress=true&f_FORMAT=BK&page={x}")
        c = r.content
        soup = BeautifulSoup(c, "html.parser")
        
        all_title = soup.findAll("span", {"class":"title-content"})
        all_author = soup.findAll("a", {"class":"author-link"})

        for book,author in zip(all_title,all_author):
            titles.append(book.text)
            authors.append(author.text)
            
        
        connect()
        for y in range(1,len(titles)):
            insert(titles[y], authors[y], "-", y)

def next_isbn():
    isbns = []
    con = sqlite3.connect("books.db")
    cursor = con.cursor()
    cursor.execute("SELECT isbn FROM book")
    rock = cursor.fetchall()
    for isbn in rock:
        isbns.append(isbn[0])
    isbns.sort()
    return isbns[-1] + 1



