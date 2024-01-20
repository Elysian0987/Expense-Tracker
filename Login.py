import tkinter as tk
from tkinter import messagebox
import mysql.connector

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker Login")

        # Create and place widgets
        self.label_username = tk.Label(root, text="Username:")
        self.label_password = tk.Label(root, text="Password:")

        self.entry_username = tk.Entry(root)
        self.entry_password = tk.Entry(root, show="*")

        self.button_login = tk.Button(root, text="Login", command=self.login)

        # Grid layout
        self.label_username.grid(row=0, column=0, padx=10, pady=5)
        self.label_password.grid(row=1, column=0, padx=10, pady=5)
        self.entry_username.grid(row=0, column=1, padx=10, pady=5)
        self.entry_password.grid(row=1, column=1, padx=10, pady=5)
        self.button_login.grid(row=2, column=1, pady=10)

        # Connect to MySQL database
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="s@mrudh1",
            database="mydatabase1"  # Use the created database name here
        )

        # Create a cursor object
        #mycursor = self.db.cursor()

        # Create a database (if it doesn't exist)
        #mycursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase1")

        # Commit changes
        #self.db.commit()

        # Use the created or existing database
        self.db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="s@mrudh1",
            database="mydatabase1"
        )

    def login(self):
        # Retrieve username and password from entry widgets
        username = self.entry_username.get()
        password = self.entry_password.get()

        # Validate against the database
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Login Successful", "Welcome, " + username + "!")
            # Add logic to open the expense tracker window or perform other actions after login
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()