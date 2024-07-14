import tkinter as tk
from tkinter import messagebox
import sqlite3

def create_table():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                  (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

def sign_up():
    def submit():
        username = username_entry.get()
        password = password_entry.get()
        
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Account created successfully!")

        signup_window.destroy()

    signup_window = tk.Toplevel(root)
    signup_window.title("Sign Up")

    username_label = tk.Label(signup_window, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(signup_window)
    username_entry.pack()

    password_label = tk.Label(signup_window, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(signup_window, show="*")
    password_entry.pack()

    submit_button = tk.Button(signup_window, text="Submit", command=submit)
    submit_button.pack()

def login():
    def submit():
        username = username_entry.get()
        password = password_entry.get()

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Success", "Login successful!")
        else:
            messagebox.showerror("Error", "Invalid username or password!")

    login_window = tk.Toplevel(root)
    login_window.title("Login")

    username_label = tk.Label(login_window, text="Username:")
    username_label.pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    password_label = tk.Label(login_window, text="Password:")
    password_label.pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    submit_button = tk.Button(login_window, text="Submit", command=submit)
    submit_button.pack()

root = tk.Tk()
root.title("Login System")

create_table()

login_button = tk.Button(root, text="Login", command=login)
login_button.pack()

signup_button = tk.Button(root, text="Sign Up", command=sign_up)
signup_button.pack()

root.mainloop()
