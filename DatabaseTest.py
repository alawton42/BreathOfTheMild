import tkinter as tk
import login
import DatabaseEdit
import DatabaseSelection


class MainFrame(tk.Frame):

    def __init__(self):

        self.root = tk.Tk()
        self.root.geometry("700x500")
        self.root.title("Breath of the Mild")

        upperFrame = tk.Frame(self.root, background="#999999")
        upperFrame.place(relwidth=1, relheight=0.3)


        self._connection = None
        self._current_table = None
        tk.Frame.__init__(self, bg="#666666", width=500, height=500)
        container = tk.Frame(self)
        container.place(relwidth=.98, relheight=.98, relx=.01, rely=.01)
        #         container.pack(expand=True)

        self.frames = {}
        for F in (Index, login.loginFrame, DUMMY, DatabaseEdit.DatabaseEditFrame, DatabaseSelection.DatabaseSelectionFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)

            self.frames[page_name] = frame
            frame.place(relwidth=1, relheight=1)
        #             frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("Index")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if page_name != "DatabaseEditFrame":
            self.root.geometry("700x500")
        if page_name == "DatabaseEditFrame":
            self.root.geometry("1200x700")
            frame.create_table()
        if page_name == "DatabaseSelectionFrame":
            frame.create_buttons()
        if (page_name == "DUMMY"):
            frame.check_connection()
        frame.tkraise()

    def set_connection(self, connection):
        self._connection = connection
        print(self._connection)

    def get_connection(self):
        return self._connection

    def set_current_table(self, table_name):
        self._current_table = table_name

    def get_current_table(self):
        return self._current_table

    def get_root(self):
        return self.root


class Index(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, width=500, height=500)
        self.controller = controller
        label = tk.Label(self, text="BREATH OF THE MILD")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Admin Login",
                           command=lambda: controller.show_frame("loginFrame"))
        button.pack()


class DUMMY(tk.Frame):
    # example: this is where password screen takes you
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self._CONNECT = self.controller.get_connection()

        label = tk.Label(self, text="DUMMY")
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Back Home",
                           command=lambda: controller.show_frame("Index"))
        button.pack()

    def check_connection(self):
        print(self._CONNECT)
        print(self.controller.get_connection())



# mainFrame.pack(pady=200)
# mainFrame.place(relx=.5, rely=.8)
if __name__ == "__main__":
    mainFrame = MainFrame()
    mainFrame.place(relwidth=1, relheight=.7, relx=0, rely=.3)
    mainFrame.get_root().mainloop()