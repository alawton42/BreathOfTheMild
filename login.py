import mysql.connector
import tkinter as tk
from mysql.connector import Error
from tkinter import *
from _curses import COLOR_BLACK


class loginFrame(tk.Frame):
    global connection

    #     global password
    #     frame.bg = COLOR_BLACK
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #         super(loginFrame, self).__init__()
        self.password = Entry(self)

        #         frame = tk.Frame(root, bg="black")
        self.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

        self.password.grid(row=0, column=1, pady=10)
        self.password.config(show='*')

        password_label = Label(self, text="Enter MySQL Password: ")
        password_label.grid(row=0, column=0)

        password_button = Button(self, text="Submit Password", command=self.create_connection)
        password_button.grid(row=2, column=0, columnspan=2)

    #     def printer(self):
    #        print("{} {}".format(self.i, self.j))

    def create_connection(self):
        global connection
        connection = None
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                passwd=self.password.get(),
                database="breathofthemild"
            )
            output_msg = "Connection to MySQL DB successful"
            print(connection)
            self.controller.set_connection(connection)
            self.controller.show_frame("DatabaseEditFrame")
        except Error as e:
            print(f"The error '{e}' occurred")

    #         menu_options = ["Insert", "Update", "Delete", "Display"]
    #         selected = StringVar(frame)
    #         selected.set(menu_options[0])
    #         menu = OptionMenu(frame, selected, *menu_options, command=done)
    #         menu.grid(row=0, column=0, pady=10)

    def execute_read_query(connection, query):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

    def get_frame(self):
        return self.frame

    def done(selected):
        print("Yay!")

# x = loginFrame()
# x.printer()