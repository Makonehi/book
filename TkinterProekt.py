import tkinter as tk
from tkinter import ttk
import sqlite3

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()
    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        self.add_img = tk.PhotoImage(file='./img/add.png')
        btn_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.add_img, command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'tel', 'email'), height=45, show='headings')
        self.tree.column('ID', width=30, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('tel', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('tel', text='Телефон')
        self.tree.heading('email', text='Email')

        self.tree.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='./img/update.png')
        button_update_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.update_img, command=self.open_update_dialog)
        button_update_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='./img/delete.png')


    def open_dialog(self):
        Child()

    def records(self, name, tel, email):
        self.db.insert_data(name, tel, email)
        self.view_records()

    def view_records(self):
        self.db.cursor.execute('SELECT * FROM db')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cursor.fetchall()]

    def open_update_dialog(self):
        Update()

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.cursor.execute('DELETE FROM db WHERE id=?', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()


    def update_records(self, name, tel, email):
        self.db.cursor.execute('''UPDATE db SET name=?, tel=?, email=? WHERE id=?''', (name, tel, email, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()



class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app
    def init_child(self):
        self.title('Добавить')
        self.geometry('400x220')
        self.resizable(False, False)

        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text='Телефон')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='Email')
        label_sum.place(x=50, y=110)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=110)

        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=220, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=300, y=170)



        self.btn_ok.bind('<Button-1>', lambda  event:
                         self.view.records(self.entry_name.get(),
                                           self.entry_email.get(),
                                           self.entry_tel.get()))




class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        # self.default_data()

    def init_edit(self):
        self.title('Редактировать контакт')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event:
                      self.view.update_records(self.entry_name.get(),
                                               self.entry_email.get(),
                                               self.entry_tel.get()))
        btn_edit.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_ok.destroy()
    # def default_data(self):
    #     self.db.cursor.execute('SELECT * FROM db WHERE id=?', self.view.tree.set(self.view.tree.selection()[0]))
    #     row = self.db.cursor.fetchall()
    #     self.entry_name.insert(0, row[0][1])
    #     self.entry_email.insert(0, row[0][2])
    #     self.entry_tel.insert(0, row[0][3])
class DB:
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS db(
                id INTEGER PRIMARY KEY,
                name TEXT,
                tel TEXT,
                email TEXT
            )'''
        )
        self.conn.commit()
    def insert_data(self, name, tel, email):
        self.cursor.execute('''INSERT INTO db (name, tel, email) VALUES ( ?, ?, ?)''',(name, tel, email))
        self.conn.commit()



if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Телефонная книга')
    root.geometry('665x450')
    root.resizable(False, False)
    root.mainloop()