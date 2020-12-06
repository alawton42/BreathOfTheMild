import mysql.connector
import tkinter as tk
from mysql.connector import Error
from tkinter import *
from functools import partial


class DatabaseEditFrame(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.current_table = None
        self.table = []
        self.insert_components = []
        self.field_names = []
        self.extra_buttons = []
        self.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
        self.error = Label(self, text="")

    def execute_read_query(self, connection, query):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"The error '{e}' occurred")
            self.error.config(text=f"The error '{e}' occurred")

    def execute_query(self, connection, query):
        cursor = connection.cursor()
        result = None
        try:
            cursor.execute(query)
        except Error as e:
            if e != 'No result set to fetch from.':
                self.error.config(text=f"The error '{e}' occurred")

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

            self.current_table = self.controller.get_current_table()

            fields_list = self.execute_read_query(self.controller.get_connection(), "SHOW COLUMNS IN " + self.current_table)
            for i, field in enumerate(fields_list):
                field_label = Label(self, text=field[0])
                field_label.grid(row=0, column=i + 1)
                self.field_names.append(field[0])

            table_contents = self.execute_read_query(self.controller.get_connection(), "SELECT * FROM " + self.current_table)
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

            # blank_space = Label(self, text="   ")
            # blank_space.grid(row=last_row_of_table + 2, column=2)

            update_button = Button(self, text="Update Table", command=self.update_table)
            update_button.grid(row=last_row_of_table + 3, column=1)
            functions_button = Button(self, text="Display Functions", command=lambda: self.controller.show_frame("Index"))
            functions_button.grid(row=last_row_of_table + 3, column=3)
            self.extra_buttons = [update_button, functions_button]
            self.error.grid(row=last_row_of_table + 2, column=0, columnspan=5)

    def delete_row(self, primary_key, primary_key_value):
        self.error.config(text="")
        print(primary_key)
        self.execute_read_query(self.controller.get_connection(), "DELETE FROM " + self.current_table + " WHERE " + primary_key + " = " + str(primary_key_value))
        print(self.execute_read_query(self.controller.get_connection(), "SELECT * FROM " + self.current_table))
        self.create_table()

    def insert_row(self, field_values):
        self.error.config(text="")
        values = ""
        for val in field_values:
            values += "'" + val.get() + "', "
        values = values[:-2]

        self.execute_read_query(self.controller.get_connection(),
                                "INSERT INTO " + self.current_table + " VALUES (" + values + ")")
        self.create_table()

    def update_table(self):
        self.error.config(text="")
        table_name = self.current_table
        query = ""
        for i, row in enumerate(self.table):
            if table_name == "Location":
                query = f"UPDATE Location " \
                        f"SET {self.field_names[0]} = {int(self.table[i][1].get())}, " \
                        f"{self.field_names[1]} = \"{self.table[i][2].get()}\", " \
                        f"{self.field_names[2]} = {int(self.table[i][3].get())} "\
                        f"WHERE {self.field_names[0]} = {self.table[i][1].get()}"
            elif table_name == "DwellsIn":
                query = f"UPDATE DwellsIn " \
                        f"SET {self.field_names[0]} = {int(self.table[i][1].get())}, " \
                        f"{self.field_names[1]} = {int(self.table[i][2].get())} "\
                        f"WHERE {self.field_names[0]} = {self.table[i][1].get()}"
            elif table_name == "Item":
                query = f"UPDATE Item " \
                        f"SET {self.field_names[0]} = {int(self.table[i][1].get())}, " \
                        f"{self.field_names[1]} = {self.table[i][2].get()}, " \
                        f"{self.field_names[2]} = \"{self.table[i][3].get()}\", " \
                        f"{self.field_names[3]} = \"{self.table[i][4].get()}\", " \
                        f"{self.field_names[4]} = \"{self.table[i][5].get()}\", " \
                        f"{self.field_names[5]} = {self.table[i][6].get()}, " \
                        f"{self.field_names[6]} = {self.table[i][7].get()}, " \
                        f"{self.field_names[7]} = \"{self.table[i][8].get()}\" "\
                        f"WHERE {self.field_names[0]} = {self.table[i][1].get()}"
            elif table_name == "Mob":
                query = f"UPDATE Mob " \
                        f"SET {self.field_names[0]} = {int(self.table[i][1].get())}, " \
                        f"{self.field_names[1]} = \"{self.table[i][2].get()}\", " \
                        f"{self.field_names[2]} = {self.table[i][3].get()}, " \
                        f"{self.field_names[3]} = {self.table[i][4].get()} "\
                        f"WHERE {self.field_names[0]} = {self.table[i][1].get()}"
            elif table_name == "NPC":
                query = f"UPDATE NPC " \
                        f"SET {self.field_names[0]} = {int(self.table[i][1].get())}, " \
                        f"{self.field_names[1]} = \"{self.table[i][2].get()}\", " \
                        f"{self.field_names[2]} = {self.table[i][3].get()} "\
                        f"WHERE {self.field_names[0]} = {self.table[i][1].get()}"
            elif table_name == "NPCDialogue":
                query = f"UPDATE NPCDialogue " \
                        f"SET {self.field_names[0]} = {int(self.table[i][1].get())}, " \
                        f"{self.field_names[1]} = \"{self.table[i][2].get()}\" "\
                        f"WHERE {self.field_names[0]} = {self.table[i][1].get()}"
            elif table_name == "NPCQuest":
                query = f"UPDATE NPCQuest " \
                        f"SET {self.field_names[0]} = {int(self.table[i][1].get())}, " \
                        f"{self.field_names[1]} = \"{self.table[i][2].get()}\" "\
                        f"WHERE {self.field_names[0]} = {self.table[i][1].get()}"
            elif table_name == "PlayerAccount":
                query = f"UPDATE PlayerAccount " \
                        f"SET {self.field_names[0]} = \"{self.table[i][1].get()}\", " \
                        f"{self.field_names[1]} = \"{self.table[i][2].get()}\", " \
                        f"{self.field_names[2]} = \"{self.table[i][3].get()}\" "\
                        f"WHERE {self.field_names[0]} = \"{self.table[i][1].get()}\""
            elif table_name == "PlayerCharacter":
                query = f"UPDATE PlayerCharacter " \
                        f"SET {self.field_names[0]} = \"{self.table[i][1].get()}\", " \
                        f"{self.field_names[1]} = {self.table[i][2].get()}, " \
                        f"{self.field_names[2]} = {self.table[i][3].get()}, " \
                        f"{self.field_names[3]} = \"{self.table[i][4].get()}\", " \
                        f"{self.field_names[4]} = {self.table[i][5].get()}, " \
                        f"{self.field_names[5]} = \"{self.table[i][6].get()}\", " \
                        f"{self.field_names[6]} = {self.table[i][7].get()} "\
                        f"WHERE {self.field_names[0]} = \"{self.table[i][1].get()}\""
            elif table_name == "Server":
                query = f"UPDATE Server " \
                        f"SET {self.field_names[0]} = {int(self.table[i][1].get())}, " \
                        f"{self.field_names[1]} = \"{self.table[i][2].get()}\", " \
                        f"{self.field_names[2]} = {self.table[i][3].get()} "\
                        f"WHERE {self.field_names[0]} = {self.table[i][1].get()}"
            elif table_name == "Shop":
                query = f"UPDATE Shop " \
                        f"SET {self.field_names[0]} = {int(self.table[i][1].get())}, " \
                        f"{self.field_names[1]} = \"{self.table[i][2].get()}\", " \
                        f"{self.field_names[2]} = \"{self.table[i][3].get()}\" "\
                        f"WHERE {self.field_names[0]} = {self.table[i][1].get()}"
            self.execute_query(self.controller.get_connection(), query)
            print(query)
        self.create_table()
