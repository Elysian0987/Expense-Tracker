import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector

import datetime
from tkcalendar import DateEntry
import tkinter.messagebox as mb
import tkinter.ttk as ttk


expense_db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="s@mrudh1",
    database="mydatabase1"
)

cursor = expense_db.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ExpenseTracker (
        ID INT AUTO_INCREMENT PRIMARY KEY,
        Date DATE,
        Payee VARCHAR(255),
        Description TEXT,
        Amount FLOAT,
        ModeOfPayment VARCHAR(255)
    )
''')
expense_db.commit()  


def list_all_expenses():
    global cursor, table

    table.delete(*table.get_children())

    try:
        cursor.execute('SELECT * FROM ExpenseTracker')
        data = cursor.fetchall()

        for values in data:
            table.insert('', END, values=values)

    except Exception as e:
        print(f"Error fetching data: {e}")

def view_expense_details():
    global table
    global date, payee, desc, amnt, MoP


    if not table.selection():
        mb.showerror('No expense selected', 'Please select an expense from the table to view its details')


    current_selected_expense = table.item(table.focus())
    values = current_selected_expense['values']


    expenditure_date = datetime.date(int(values[1][:4]), int(values[1][5:7]), int(values[1][8:]))


    date.set_date(expenditure_date) ; payee.set(values[2]) ; desc.set(values[3]) ; amnt.set(values[4]) ; MoP.set(values[5])




def clear_fields():
    global desc, payee, amnt, MoP, date, table


    today_date = datetime.datetime.now().date()


    desc.set('') ; payee.set('') ; amnt.set(0.0) ; MoP.set('Cash'), date.set_date(today_date)
    table.selection_remove(*table.selection())




def remove_expense():
    if not table.selection():
        mb.showerror('No record selected!', 'Please select a record to delete!')
        return


    current_selected_expense = table.item(table.focus())
    values_selected = current_selected_expense['values']


    surety = mb.askyesno('Are you sure?', f'Are you sure that you want to delete the record of {values_selected[2]}')


    if surety:
        cursor.execute('DELETE FROM ExpenseTracker WHERE ID=%d' % values_selected[0])
        connector.commit()


        list_all_expenses()
        mb.showinfo('Record deleted successfully!', 'The record you wanted to delete has been deleted successfully')




def remove_all_expenses():
    surety = mb.askyesno('Are you sure?', 'Are you sure that you want to delete all the expense items from the database?', icon='warning')


    if surety:
        table.delete(*table.get_children())


        cursor.execute('DELETE FROM ExpenseTracker')
        connector.commit()


        clear_fields()
        list_all_expenses()
        mb.showinfo('All Expenses deleted', 'All the expenses were successfully deleted')
    else:
        mb.showinfo('Ok then', 'The task was aborted and no expense was deleted!')




def add_another_expense():
    global date, payee, desc, amnt, MoP
    global connector


    if not date.get() or not payee.get() or not desc.get() or not amnt.get() or not MoP.get():
        mb.showerror('Fields empty!', "Please fill all the missing fields before pressing the add button!")
    else:
        cursor.execute(
        'INSERT INTO ExpenseTracker (Date, Payee, Description, Amount, ModeOfPayment) VALUES (?, ?, ?, ?, ?)',
        (date.get_date(), payee.get(), desc.get(), amnt.get(), MoP.get())
        )
        connector.commit()


        clear_fields()
        list_all_expenses()
        mb.showinfo('Expense added', 'The expense whose details you just entered has been added to the database')




def edit_expense():
    global table


    def edit_existing_expense():
        global date, amnt, desc, payee, MoP
        global connector, table


        current_selected_expense = table.item(table.focus())
        contents = current_selected_expense['values']


        cursor.execute('UPDATE ExpenseTracker SET Date = ?, Payee = ?, Description = ?, Amount = ?, ModeOfPayment = ? WHERE ID = ?',
                          (date.get_date(), payee.get(), desc.get(), amnt.get(), MoP.get(), contents[0]))
        connector.commit()


        clear_fields()
        list_all_expenses()


        mb.showinfo('Data edited', 'We have updated the data and stored in the database as you wanted')
        edit_btn.destroy()
        return


    if not table.selection():
        mb.showerror('No expense selected!', 'You have not selected any expense in the table for us to edit; please do that!')
        return


    view_expense_details()


    edit_btn = Button(data_entry_frame, text='Edit expense', font=btn_font, width=30,
                      bg=hlb_btn_bg, command=edit_existing_expense)
    edit_btn.place(x=10, y=395)




def selected_expense_to_words():
    global table


    if not table.selection():
        mb.showerror('No expense selected!', 'Please select an expense from the table for us to read')
        return


    current_selected_expense = table.item(table.focus())
    values = current_selected_expense['values']


    message = f'Your expense can be read like: \n"You paid {values[4]} to {values[2]} for {values[3]} on {values[1]} via {values[5]}"'


    mb.showinfo('Here\'s how to read your expense', message)




def expense_to_words_before_adding():
    global date, desc, amnt, payee, MoP


    if not date or not desc or not amnt or not payee or not MoP:
        mb.showerror('Incomplete data', 'The data is incomplete, meaning fill all the fields first!')


    message = f'Your expense can be read like: \n"You paid {amnt.get()} to {payee.get()} for {desc.get()} on {date.get_date()} via {MoP.get()}"'


    add_question = mb.askyesno('Read your record like: ', f'{message}\n\nShould I add it to the database?')


    if add_question:
        add_another_expense()
    else:
        mb.showinfo('Ok', 'Please take your time to add this record')










dataentery_frame_bg = '#ddd4fc'
buttons_frame_bg = '#e9d7e1'
hlb_btn_bg = 'Linen'


lbl_font = ('Georgia', 13)
entry_font = 'Times 13 bold'
btn_font = ('Gill Sans MT', 13)


root = Tk()
root.title('Expense Tracker')
root.geometry('1100x680+0+0')




Label(root, text='EXPENSE TRACKER',fg="white", highlightcolor='black', bd=2, relief=RIDGE, font=('Noto Sans CJK TC', 15, 'bold'), bg='#914e75').pack(side=TOP, fill=X)


desc = StringVar()
amnt = DoubleVar()
payee = StringVar()
MoP = StringVar(value='Cash')


data_entry_frame = Frame(root, bg=dataentery_frame_bg)
data_entry_frame.place(x=0, y=30, relheight=0.95, relwidth=0.25)


buttons_frame = Frame(root, bg=buttons_frame_bg)
buttons_frame.place(relx=0.25, rely=0.05, relwidth=0.75, relheight=0.21)


tree_frame = Frame(root)
tree_frame.place(relx=0.25, rely=0.26, relwidth=0.75, relheight=0.74)


Label(data_entry_frame, text='Date (M/DD/YY) :', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=50)
date = DateEntry(data_entry_frame, date=datetime.datetime.now().date(), font=entry_font)
date.place(x=160, y=50)


Label(data_entry_frame, text='Payee\t :', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=230)
Entry(data_entry_frame, font=entry_font, width=31, text=payee).place(x=10, y=260)


Label(data_entry_frame, text='Description :', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=100)
Entry(data_entry_frame, font=entry_font, width=31, text=desc).place(x=10, y=130)


Label(data_entry_frame, text='Amount\t :', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=180)
Entry(data_entry_frame, font=entry_font, width=14, text=amnt).place(x=160, y=180)


Label(data_entry_frame, text='Mode of Payment:', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=310)
dd1 = OptionMenu(data_entry_frame, MoP, *['Cash', 'Cheque', 'Credit Card', 'Debit Card', 'Paytm', 'Google Pay', 'Razorpay'])
dd1.place(x=160, y=305) ; dd1.configure(width=10, font=entry_font)


Button(data_entry_frame, text='Add expense', command=add_another_expense, font=btn_font, width=30,
       bg='#50C878').place(x=10, y=395)
Button(data_entry_frame, text='Convert to words before adding', font=btn_font, width=30, bg=hlb_btn_bg).place(x=10,y=450)


Button(buttons_frame, text='Delete Expense', font=btn_font, width=25, bg='#89674a', command=remove_expense).place(x=30, y=5)


Button(buttons_frame, text='Clear Fields in DataEntry Frame', font=btn_font, width=25, bg='lightYellow',
       command=clear_fields).place(x=335, y=5)


Button(buttons_frame, text='Delete All Expenses', font=btn_font, width=25, bg='#9f5529', command=remove_all_expenses).place(x=640, y=5)


Button(buttons_frame, text='View Selected Expense\'s Details', font=btn_font, width=25, bg=hlb_btn_bg,
       command=view_expense_details).place(x=30, y=65)


Button(buttons_frame, text='Edit Selected Expense', command=edit_expense, font=btn_font, width=25, bg=hlb_btn_bg).place(x=335,y=65)


Button(buttons_frame, text='Convert Expense to a sentence', font=btn_font, width=25, bg=hlb_btn_bg,
       command=selected_expense_to_words).place(x=640, y=65)


table = ttk.Treeview(tree_frame, selectmode=BROWSE, columns=('ID', 'Date', 'Payee', 'Description', 'Amount', 'Mode of Payment'))


X_Scroller = Scrollbar(table, orient=HORIZONTAL, command=table.xview)
Y_Scroller = Scrollbar(table, orient=VERTICAL, command=table.yview)
X_Scroller.pack(side=BOTTOM, fill=X)
Y_Scroller.pack(side=RIGHT, fill=Y)


table.config(yscrollcommand=Y_Scroller.set, xscrollcommand=X_Scroller.set)


table.heading('ID', text='S No.', anchor=CENTER)
table.heading('Date', text='Date', anchor=CENTER)
table.heading('Payee', text='Payee', anchor=CENTER)
table.heading('Description', text='Description', anchor=CENTER)
table.heading('Amount', text='Amount', anchor=CENTER)
table.heading('Mode of Payment', text='Mode of Payment', anchor=CENTER)


table.column('#0', width=0, stretch=NO)
table.column('#1', width=50, stretch=NO)
table.column('#2', width=95, stretch=NO) 
table.column('#3', width=150, stretch=NO) 
table.column('#4', width=325, stretch=NO) 
table.column('#5', width=135, stretch=NO) 
table.column('#6', width=125, stretch=NO) 


table.place(relx=0, y=0, relheight=1, relwidth=1)


list_all_expenses()


root.update()

def open_expense_tracker():
    expense_tracker_window = tk.Toplevel(root)
    expense_tracker_window.title("Expense Tracker")
    expense_tracker_window.geometry("1100x680+0+0")

    background_image_expense = Image.open(r"C:\Users\samru\Downloads\OIP.jpeg")
    background_image_expense = ImageTk.PhotoImage(background_image_expense)
    

    list_all_expenses()  


class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker Login")

        self.label_username = tk.Label(root, text="Username:")
        self.label_password = tk.Label(root, text="Password:")

        self.entry_username = tk.Entry(root)
        self.entry_password = tk.Entry(root, show="*")

        self.button_login = tk.Button(root, text="Login", command=self.login)

        self.label_username.grid(row=0, column=0, padx=10, pady=5)
        self.label_password.grid(row=1, column=0, padx=10, pady=5)
        self.entry_username.grid(row=0, column=1, padx=10, pady=5)
        self.entry_password.grid(row=1, column=1, padx=10, pady=5)
        self.button_login.grid(row=2, column=1, pady=10)

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="s@mrudh1",
            database="mydatabase1"  
        )

        #mycursor = self.db.cursor()

        #mycursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase1")

        #self.db.commit()

        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="s@mrudh1",
            database="mydatabase1"
        )

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
root.mainloop()