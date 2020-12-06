import mysql.connector
import tkinter as tk
from mysql.connector import Error
from tkinter import *
from functools import partial
from _curses import COLOR_BLACK


class DatabaseEditFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.table = []
        self.insert_components = []
        self.field_names = []
        self.extra_buttons = []

        #         super(loginFrame, self).__init__()
        self.password = Entry(self)

        #         frame = tk.Frame(root, bg="black")
        self.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

        # self.password.grid(row=0, column=1, pady=10)
        # self.password.config(show='*')
        #
        # password_label = Label(self, text="Here!!!")
        # password_label.grid(row=0, column=0)
        #
        # password_button = Button(self, text="Submit Password")
        # password_button.grid(row=2, column=0, columnspan=2)

    #     def printer(self):
    #        print("{} {}".format(self.i, self.j))

    def execute_read_query(self, connection, query):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
        except Error as e:
            print(f"The error '{e}' occurred")

    def get_frame(self):
        return self.frame

    def create_table(self):
        for row in self.table:
            for row_component in row:
                row_component.destroy()
        for component in self.insert_components:
            component.destroy()
        for button in self.extra_buttons:
            button.destroy()

        if self.controller.get_connection() is not None:

            fields_list = self.execute_read_query(self.controller.get_connection(), "SHOW COLUMNS IN Location")
            for i, field in enumerate(fields_list):
                field_label = Label(self, text=field[0])
                field_label.grid(row=0, column=i + 1)
                self.field_names.append(field[0])

            table_contents = self.execute_read_query(self.controller.get_connection(), "SELECT * FROM Location")
            last_row_of_table = 0
            self.table = []
            for i, row in enumerate(table_contents):
                table_row = []
                button = Button(self, text="Delete row",
                                command=partial(self.delete_row, fields_list[0][0], table_contents[i][0]))
                button.grid(row=i + 1, column=0)
                table_row.append(button)
                last_row_of_table = i + 1
                for j, col in enumerate(row):
                    entry = Entry(self, width=15)
                    entry.insert(END, table_contents[i][j])
                    entry.grid(row=i + 1, column=j + 1)
                    table_row.append(entry)
                self.table.append(table_row)

            field_values = []
            for i, field in enumerate(fields_list):
                field_value = Entry(self, width=15)
                field_value.grid(row=last_row_of_table + 1, column=i + 1)
                field_values.append(field_value)
                self.insert_components.append(field_value)
            button = Button(self, text="Add row",
                            command=lambda: self.insert_row(field_values))
            button.grid(row=last_row_of_table + 1, column=0)
            self.insert_components.append(button)

            blank_space = Label(self, text="   ")
            blank_space.grid(row=last_row_of_table + 2, column=2)

            update_button = Button(self, text="Update Table", command=self.update_table)
            update_button.grid(row=last_row_of_table + 3, column=1)
            functions_button = Button(self, text="Display Functions", command=lambda: self.controller.show_frame("Index"))
            functions_button.grid(row=last_row_of_table + 3, column=3)
            self.extra_buttons = [update_button, functions_button]

    def delete_row(self, primary_key, primary_key_value):
        print(primary_key)
        self.execute_read_query(self.controller.get_connection(), "DELETE FROM Location WHERE " + primary_key + " = " + str(primary_key_value))
        print(self.execute_read_query(self.controller.get_connection(), "SELECT * FROM Location"))
        self.create_table()

    def insert_row(self, field_values):
        values = ""
        for val in field_values:
            values += "'" + val.get() + "', "
        values = values[:-2]

        self.execute_read_query(self.controller.get_connection(),
                                "INSERT INTO Location VALUES (" + values + ")")
        self.create_table()

    def update_table(self):
        table_name = "Location"
        for i, row in enumerate(self.table):
            if table_name == "Location":
                query = f"UPDATE Location " \
                        f"SET {self.field_names[0]} = {int(self.table[i][1].get())}, " \
                        f"{self.field_names[1]} = \"{self.table[i][2].get()}\", " \
                        f"{self.field_names[2]} = {int(self.table[i][3].get())} " \
                        f"WHERE {self.field_names[0]} = {self.table[i][1].get()}"
            self.execute_query(self.controller.get_connection(), query)
            print(query)

        self.create_table()
