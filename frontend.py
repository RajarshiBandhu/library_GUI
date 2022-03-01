from tkinter import *
from click import command
from matplotlib.pyplot import title
from backend import *

#If you want some books to put in, use add_to_db (uncomment it) to add books to the database. 
#The paramater is the number of books, each increase of 1 will aproximately add 5 books

#add_to_db(5)
def delete_entry():
    """
    Empties entry values
    """
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)

def view_command():
    """
    displays all rows in database on list1
    """
    list1.delete(0, END)#Deletes all rows in list1 from the *0* row, to *END* row
    for row in view():
        list1.insert(END, f"{row[0]} {row[1]} by {row[2]}, year:{row[3]}, isbn:{row[4]}")#inserts *string*, at the *END* of list1

def search_command():
    """
    inserts row(s) returned from search() into list1
    """
    rows = search(title = e1.get(), author = e2.get(), year = e3.get(), isbn = e4.get())
    list1.delete(0, END)
    print(rows)
    if rows == 0:
        return 0
    for row in rows:
        list1.insert(END, f"{row[0]} {row[1]} by {row[2]}, year:{row[3]}, isbn:{row[4]}")
    delete_entry()


def insert_command():
    """
    Inserts row into database, using the entry boxes
    """
    if not e1.get() or not e2.get() or not e3.get():
        list1.delete(0,END)
        list1.insert(0, "Fill in title, author, year, isbn")
    else:
        insert(e1.get(), e2.get(), e3.get(), next_isbn())
        delete_entry()
        view_command()

def delete_command():
    """
    deletes a selected row
    """
    con = sqlite3.connect("books.db")
    cursor = con.cursor()
    for i in list1.curselection():#returns position of selected row
        chunk = list1.get(i).split(" ")
        cursor.execute("SELECT * FROM book WHERE id=?", (chunk[0]))
        row = cursor.fetchall()
        delete(row[0][0])
        view_command()

def update_command():
    """
    Updates a selected row
    """
    con = sqlite3.connect("books.db")
    cursor = con.cursor()
    for i in list1.curselection():
        chunk = list1.get(i).split(" ")
        cursor.execute("SELECT * FROM book WHERE id=?", (chunk[0]))
        row = cursor.fetchall()
        if not e1.get() or not e2.get() or not e3.get() or not e4.get():
            list1.delete(0,END)
            list1.insert(0, "Fill in title, author, year, isbn")
        else:
            update(row[0][0], e1.get(), e2.get(), e3.get(), next_isbn())
            view_command()


window = Tk()#lets you create a instance of the class and use the functions


l1 = Label(window, text="Title")#defines a label, which is in *windows*, and has a name of *Title*
l1.grid(row=0, column=0)#.grid will display *l1*, at row 0, column 0

l2 = Label(window, text="Author")
l2.grid(row=0, column=2)

l3 = Label(window, text="Year")
l3.grid(row=1, column=0)

l4 = Label(window, text="ISBN")
l4.grid(row=1, column=2)

title_text = StringVar() #creates a empty variable, it is used in the entry as the variable were you type
e1 = Entry(window, textvariable=title_text)#defines a entry, with the variable being *title_text*
e1.grid(row=0,column=1)

author_text = StringVar() 
e2 = Entry(window, textvariable=author_text)
e2.grid(row=0,column=3)

year_text = StringVar() 
e3 = Entry(window, textvariable=year_text)
e3.grid(row=1,column=1)

isbn_text = StringVar() 
e4 = Entry(window, textvariable=isbn_text)
e4.grid(row=1,column=3)

list1 = Listbox(window, height=6, width=35)#display lines of text, made so you can highlight it easily. 
list1.grid(row=2,column=0, rowspan=6, columnspan=2)


sb1 = Scrollbar(window)#defines a scrollbar
sb1.grid(row=2,column=2, rowspan=6)

list1.configure(yscrollcommand=sb1.set)#lets you commnicate with a vertical scroll bar
sb1.configure(command=list1.yview)#makes it so when you scroll, it scrolls on the y axis for list1

b1 = Button(window, text="View All", width=12, command=view_command)#Defines a button
b1.grid(row=2, column=3)

b2 = Button(window, text="Search Entry", width=12, command=search_command)
b2.grid(row=3, column=3)

b3 = Button(window, text="Add Entry", width=12, command=insert_command)
b3.grid(row=4, column=3)

b4 = Button(window, text="Update", width=12, command=update_command)
b4.grid(row=5, column=3)

b5 = Button(window, text="Delete", width=12, command=delete_command)
b5.grid(row=6, column=3)

b6 = Button(window, text="Close", width=12, command=window.destroy)
b6.grid(row=7, column=3)


window.mainloop()#starts a event loops that executes your application



