import mysql.connector
import hashlib
import tkinter as tk
from tkinter import messagebox

# Database Connection
def connect_db():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",  
            password="root", 
            database="user_auth"
        )
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return None

# Hash Password Function
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Signup Function
def signup():
    username = entry_username.get()
    password = entry_password.get()
    
    if not username or not password:
        messagebox.showerror("Input Error", "Username and Password cannot be empty!")
        return
    
    conn = connect_db()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    try:
        cursor.execute("select count(*) from users")
        count = cursor.fetchone()[0]
        cursor.execute("INSERT INTO users (id, username, password) VALUES (%s, %s, %s)", (count+1, username, hash_password(password)))
        conn.commit()
        messagebox.showinfo("Success", "Signup Successful!")
        entry_username.delete(0, tk.END) 
        entry_password.delete(0, tk.END)
    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "Username already exists!")
    
    cursor.close()
    conn.close()

# Login Function
def login():
    username = entry_username.get()
    password = entry_password.get()
    
    if not username or not password:
        messagebox.showerror("Input Error", "Please enter Username and Password!")
        return
    
    conn = connect_db()
    if not conn:
        return
    
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, hash_password(password)))
    user = cursor.fetchone()
    
    if user:
        messagebox.showinfo("Login Success", f"Welcome, {username}!")
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password!")
    
    cursor.close()
    conn.close()

# UI Design
root = tk.Tk()
root.title("Login & Signup System")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

frame = tk.Frame(root, bg="white", padx=20, pady=20)
frame.pack(expand=True)

label_title = tk.Label(frame, text="User Authentication", font=("Arial", 14, "bold"), bg="white")
label_title.grid(row=0, column=0, columnspan=2, pady=10)

label_username = tk.Label(frame, text="Username:", font=("Arial", 12), bg="white")
label_username.grid(row=1, column=0, padx=5, pady=5)

entry_username = tk.Entry(frame, font=("Arial", 12))
entry_username.grid(row=1, column=1, padx=5, pady=5)

label_password = tk.Label(frame, text="Password:", font=("Arial", 12), bg="white")
label_password.grid(row=2, column=0, padx=5, pady=5)

entry_password = tk.Entry(frame, font=("Arial", 12), show="*")
entry_password.grid(row=2, column=1, padx=5, pady=5)

btn_signup = tk.Button(frame, text="Signup", font=("Arial", 12), bg="#28a745", fg="white", command=signup)
btn_signup.grid(row=3, column=0, padx=5, pady=10, sticky="ew")

btn_login = tk.Button(frame, text="Login", font=("Arial", 12), bg="#007bff", fg="white", command=login)
btn_login.grid(row=3, column=1, padx=5, pady=10, sticky="ew")

root.mainloop()
