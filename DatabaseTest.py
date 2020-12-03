import mysql.connector
from mysql.connector import Error
from tkinter import *

def create_connection():
    global connection
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd=password.get(),
            database = "breathofthemild"
        )
        output_msg = "Connection to MySQL DB successful"
    except Error as e:
        print(f"The error '{e}' occurred")
        root.destroy()

    password.destroy()
    password_label.destroy()
    password_button.destroy()

    menu_options = ["Insert", "Update", "Delete", "Display"]
    selected = StringVar(root)
    selected.set(menu_options[0])
    menu = OptionMenu(root, selected, *menu_options, command=done)
    menu.grid(row=0, column=0, pady=10)

    # location_fields = execute_read_query(connection, "SHOW COLUMNS FROM location")
    # for i in range(len(location_fields)):
    #     entry = Label(root, text=str(location_fields[i][0]))
    #     entry.grid(row=0, column=i)
    #
    # locations_table = execute_read_query(connection, "Select * from location")
    # table_contents = []
    # for i in range(len(locations_table)):
    #     for j in range(len(locations_table[i])):
    #         entry = Label(root, text=str(locations_table[i][j]))
    #         entry.grid(row=i+1, column=j)
    #         table_contents.append(entry)



def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

def done(selected):
    print("Yay!")

global connection
root = Tk()
root.title("Test Database")
root.geometry("500x500")

password = Entry(root)
password.grid(row=0, column=1, pady=10)
password.config(show='*')

password_label = Label(root, text="Enter MySQL Password: ")
password_label.grid(row=0, column=0)

password_button = Button(root, text="Submit Password", command=create_connection)
password_button.grid(row=2, column=0, columnspan=2)


root.mainloop()

print(connection)
