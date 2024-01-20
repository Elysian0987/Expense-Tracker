import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import datetime
from tkcalendar import DateEntry
import tkinter.ttk as ttk
from tkinter import messagebox as mb
import mysql.connector



def login():
    global table, date, payee, desc, amnt, MoP
    # Retrieve username and password from entry widgets
    username = entry_username.get()
    password = entry_password.get()

    db = mysql.connector.connect(
                host="localhost",
                user="root",  # replace with your MySQL username
                password="tanman135", 
                database = "database1"   # replace with your MySQL password
    )
    # Validate against the database
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    if user:
        mb.showinfo("Login Successful", "Welcome, " + username + "!")    
        result = mb.askyesno("Question", "Do you want to proceed?")
        if result:
            root_login.destroy()
            open_tracker(username, datetime.datetime.now().date(), payee)
            
        # Add logic to open the expense tracker window or perform other actions after login
        
    else:
        mb.showerror("Login Failed", "Invalid username or password")

    cursor.close()
    db.close()
def open_tracker(username, date, payee):
    global table
    db = mysql.connector.connect(
            host="localhost",
            user="root",  # replace with your MySQL username
            password="tanman135",  # replace with your MySQL password
            database="database1"
        )
    cursor = db.cursor()

    # Functions
    def list_all_expenses():
        global db, table

        table.delete(*table.get_children())

        all_data = cursor.execute('SELECT * FROM users')
        data = cursor.fetchall()

        for values in data:
            table.insert('', END, values=values)

    def view_expense_details(date, payee):
        global table
        global desc, amnt, MoP

        if not table.selection():
            mb.showerror('No expense selected', 'Please select an expense from the table to view its details')

        current_selected_expense = table.item(table.focus())
        values = current_selected_expense['values']

        expenditure_date = datetime.date(int(values[1].year), int(values[1].month), int(values[1].day))

        date.set_date(expenditure_date)
        payee.set(values[2])
        desc.set(values[3])
        amnt.set(values[4])
        MoP.set(values[5])

    def clear_fields():
        global desc, payee, amnt, MoP, date, table

        today_date = datetime.datetime.now().date()

        desc.set('')
        payee.set('')
        amnt.set(0.0)
        MoP.set('Cash')
        date.set_date(today_date)
        table.selection_remove(*table.selection())

    def remove_expense(username):
        if not table.selection():
            mb.showerror('No record selected!', 'Please select a record to delete!')
            return

        current_selected_expense = table.item(table.focus())
        values_selected = current_selected_expense['values']

        surety = mb.askyesno('Are you sure?', f'Are you sure that you want to delete the record of {values_selected[2]}')

        if surety:
            cursor.execute('DELETE FROM users WHERE username=%s', (username))
            db.commit()

            list_all_expenses()
            mb.showinfo('Record deleted successfully!', 'The record you wanted to delete has been deleted successfully')

    def remove_all_expenses():
        surety = mb.askyesno('Are you sure?', 'Are you sure that you want to delete all the expense items from the database%s',
                            icon='warning')

        if surety:
            table.delete(*table.get_children())

            cursor.execute('DELETE FROM users')
            db.commit()

            clear_fields()
            list_all_expenses()
            mb.showinfo('All Expenses deleted', 'All the expenses were successfully deleted')
        else:
            mb.showinfo('Ok then', 'The task was aborted and no expense was deleted!')

    def add_another_expense(username, date, payee):
        global desc, amnt, MoP
        global cursor, table

        if not date.get() or not payee.get() or not desc.get() or not amnt.get() or not MoP.get():
            mb.showerror('Fields empty!', "Please fill all the missing fields before pressing the add button!")
        else:
            cursor.execute(
                '''INSERT INTO users (date, Payee, Description, Amount, ModeOfPayment) 
                SELECT %s, %s, %s, %s, %s, %s
                FROM users
                WHERE username = %s''',
                (date.get(), payee.get(), desc.get(), amnt.get(), MoP.get(), username)
            )
            db.commit()

            clear_fields()
            list_all_expenses()
            mb.showinfo('Expense added', 'The expense whose details you just entered has been added to the database')

    def edit_expense():
        global table

        def edit_existing_expense(username):
            global date, amnt, desc, payee, MoP
            global cursor, table

            current_selected_expense = table.item(table.focus())
            contents = current_selected_expense['values']

            cursor.execute(
                'UPDATE users SET Date = %d-%m-%Y, Payee = %s, Description = %s, Amount = %d, ModeOfPayment = %s WHERE username = %s, Date = %d-%m-%Y',
                (date.get(), payee.get(), desc.get(), amnt.get(), MoP.get(), username, date))
            db.commit()

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

    def expense_to_words_before_adding(username):
        global date, desc, amnt, payee, MoP

        if not date or not desc or not amnt or not payee or not MoP:
            mb.showerror('Incomplete data', 'The data is incomplete, meaning fill all the fields first!')

        message = f'Your expense can be read like: \n"You paid {amnt.get()} to {payee.get()} for {desc.get()} on {date.get()} via {MoP.get()}"'

        add_question = mb.askyesno('Read your record like: ', f'{message}\n\nShould I add it to the database%s')

        if add_question:
            add_another_expense(username)
        else:
            mb.showinfo('Ok', 'Please take your time to add this record')

    # Backgrounds and Fonts
    dataentery_frame_bg = '#fab885'
    buttons_frame_bg = '#f27457'
    hlb_btn_bg = 'White'

    lbl_font = ('Georgia', 13)
    entry_font = 'Times 13 bold'
    btn_font = ('Gill Sans MT', 13)

    # Initializing the GUI window
    root = Tk()
    root.title('Expense Tracker')
    root.geometry('1100x680+0+0')

    Label(root, text='EXPENSE TRACKER', fg="White", highlightcolor='black', bd=2, relief=RIDGE,
        font=('Noto Sans CJK TC', 15, 'bold'), bg='#fab885').pack(side=TOP, fill=X)

    # StringVar and DoubleVar variables
    desc = StringVar(value='')
    amnt = DoubleVar(value=0.0)
    payee = StringVar(value='')
    MoP = StringVar(value='Cash')

    # Frames
    data_entry_frame = Frame(root, bg=dataentery_frame_bg)
    data_entry_frame.place(x=0, y=30, relheight=0.95, relwidth=0.25)

    buttons_frame = Frame(root, bg=buttons_frame_bg)
    buttons_frame.place(relx=0.25, rely=0.05, relwidth=0.75, relheight=0.21)

    tree_frame = Frame(root)
    tree_frame.place(relx=0.25, rely=0.26, relwidth=0.75, relheight=0.74)

    # Data Entry Frame
    Label(data_entry_frame, text='Date (M/DD/YY) :', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=50)
    date = DateEntry(data_entry_frame, date=datetime.datetime.now().date(), font=entry_font)
    date.place(x=160, y=50)

    Label(data_entry_frame, text='Payee\t :', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=230)
    Entry(data_entry_frame, font=entry_font, width=31, textvariable=payee).place(x=10, y=260)

    Label(data_entry_frame, text='Description :', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=100)
    Entry(data_entry_frame, font=entry_font, width=31, textvariable=desc).place(x=10, y=130)

    Label(data_entry_frame, text='Amount\t :', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=180)
    Entry(data_entry_frame, font=entry_font, width=14, textvariable=amnt).place(x=160, y=180)

    Label(data_entry_frame, text='Mode of Payment:', font=lbl_font, bg=dataentery_frame_bg).place(x=10, y=310)
    dd1 = OptionMenu(data_entry_frame, MoP, *['Cash', 'Cheque', 'Credit Card', 'Debit Card', 'Paytm', 'Google Pay', 'Razorpay'])
    dd1.config(width=10, font=entry_font)
    dd1.place(x=160, y=305)
    

    Button(data_entry_frame, text='Add expense', command=lambda : add_another_expense(username, date, payee), font=btn_font, width=30, bg='Green').place(x=10, y=395)

    Button(data_entry_frame, text='Convert to words before adding', font=btn_font, width=30, bg=hlb_btn_bg).place(x=10, y=450)

    # Buttons' Frame
    Button(buttons_frame, text='Delete Expense', font=btn_font, width=25, bg='Red', command=remove_expense).place(x=30, y=5)

    Button(buttons_frame, text='Clear Fields in DataEntry Frame', font=btn_font, width=25, bg='Yellow',
        command=clear_fields).place(x=335, y=5)

    Button(buttons_frame, text='Delete All Expenses', font=btn_font, width=25, bg='Red', command=remove_all_expenses).place(x=640, y=5)

    Button(buttons_frame, text='View Selected Expense\'s Details', font=btn_font, width=25, bg=hlb_btn_bg,
        command=view_expense_details).place(x=30, y=65)

    Button(buttons_frame, text='Edit Selected Expense', command=edit_expense, font=btn_font, width=25, bg=hlb_btn_bg).place(x=335, y=65)

    Button(buttons_frame, text='Convert Expense to a sentence', font=btn_font, width=25, bg=hlb_btn_bg,
        command=selected_expense_to_words).place(x=640, y=65)

    # Treeview Frame
    table = ttk.Treeview(tree_frame, selectmode=BROWSE,
                        columns=('Date', 'Payee', 'Description', 'Amount', 'Mode of Payment'))

    X_Scroller = Scrollbar(table, orient=HORIZONTAL, command=table)
    Y_Scroller = Scrollbar(table, orient=VERTICAL, command=table.yview)
    X_Scroller.pack(side=BOTTOM, fill=X)
    Y_Scroller.pack(side=RIGHT, fill=Y)


    table.config(yscrollcommand=Y_Scroller.set, xscrollcommand=X_Scroller.set)

    table.heading('Date', text='Date', anchor=CENTER)
    table.heading('Payee', text='Payee', anchor=CENTER)
    table.heading('Description', text='Description', anchor=CENTER)
    table.heading('Amount', text='Amount', anchor=CENTER)
    table.heading('Mode of Payment', text='Mode of Payment', anchor=CENTER)


    table.column('#0', width=0, stretch=NO)
    table.column('#1', width=50, stretch=NO)
    table.column('#2', width=95, stretch=NO) # Date column
    table.column('#3', width=150, stretch=NO) # Payee column
    table.column('#4', width=325, stretch=NO) # Title column
    table.column('#5', width=135, stretch=NO) # Amount column # Mode of Payment column


    table.place(relx=0, y=0, relheight=1, relwidth=1)


    list_all_expenses()


    # Finalizing the GUI window
    root.update()
    root.mainloop()

def register():
    # Retrieve username and password from entry widgets
    username = entry_register_username.get()
    password = entry_register_password.get()

    # Insert user into the database
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    db.commit()

    mb.showinfo("Registration Successful", "Registration successful for user: " + username)

# Create the main Tkinter window
root_login = tk.Tk()
root_login.title("Expense Tracker Login")
root_login.geometry("473x300")

# Create a Canvas widget
canvas = tk.Canvas(root_login, width=475, height=300)
canvas.pack()

# Load the background image
background_image = ImageTk.PhotoImage(Image.open(r"C:\Users\Ashish\OneDrive\Documents\OIP.jpeg"))
canvas.create_image(0, 0, anchor=NW, image=background_image)

# Create and place widgets on top of the background for login
label_username = tk.Label(root_login, text="Username:", bg="white")
label_password = tk.Label(root_login, text="Password:", bg="white")

entry_username = tk.Entry(root_login)
entry_password = tk.Entry(root_login, show="*")

button_login = tk.Button(root_login, text="Login", command=login)

# Grid layout using the Canvas widget
label_username_window = canvas.create_window(10, 10, anchor=NW, window=label_username)
label_password_window = canvas.create_window(10, 40, anchor=NW, window=label_password)
entry_username_window = canvas.create_window(120, 10, anchor=NW, window=entry_username)
entry_password_window = canvas.create_window(120, 40, anchor=NW, window=entry_password)
button_login_window = canvas.create_window(120, 80, anchor=NW, window=button_login)

# Create and place widgets on top of the background for registration
label_register_username = tk.Label(root_login, text="Username:", bg="white")
label_register_password = tk.Label(root_login, text="Set Password:", bg="white")

entry_register_username = tk.Entry(root_login)
entry_register_password = tk.Entry(root_login, show="*")

button_register = tk.Button(root_login, text="Register", command=register)

# Grid layout using the Canvas widget
label_register_username_window = canvas.create_window(10, 120, anchor=NW, window=label_register_username)
label_register_password_window = canvas.create_window(10, 150, anchor=NW, window=label_register_password)
entry_register_username_window = canvas.create_window(120, 120, anchor=NW, window=entry_register_username)
entry_register_password_window = canvas.create_window(120, 150, anchor=NW, window=entry_register_password)
button_register_window = canvas.create_window(120, 190, anchor=NW, window=button_register)

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tanman135",
    database="database1"
)

# Create a cursor object
mycursor = db.cursor()

# Create a users table (if it doesn't exist)
mycursor.execute('''
                 CREATE TABLE IF NOT EXISTS users (
                    username VARCHAR(255) PRIMARY KEY, 
                    password VARCHAR(255),
                    date DATE , 
                    Payee VARCHAR(255),
                    Description TEXT,
                    Amount FLOAT,
                    ModeOfPayment VARCHAR(255)
                )
                ''')

# Commit changes
db.commit()

# Use the created or existing database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tanman135",
    database="database1"
)

# Start the Tkinter event loop
root_login.mainloop()
