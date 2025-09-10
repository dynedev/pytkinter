"""
================================================================================
Project Name   : SQlite3 Tkinter Base Sqlite3 with exe Builders Linux And Windows
File Name      : app.py
Author         : Brian Boothe
Email          : deveng@logicdyne.net
Date Created   : 2025-9-7
Last Modified  : 2025-9-10
Version        : 1.0.0
License        : Proprietary
Python Version : 3.x

Description:
------------
SQlite3 Tkinter Base Sqlite3 with exe Builders Linux And Windows
================================================================================
"""


import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

# -----------------------------
# Database Functions
# -----------------------------
def init_db():
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS contacts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        phone TEXT NOT NULL)''')
    conn.commit()
    conn.close()

def insert_contact(name, phone):
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts (name, phone) VALUES (?, ?)", (name, phone))
    conn.commit()
    conn.close()

def fetch_contacts():
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contacts")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_contact(contact_id, name, phone):
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE contacts SET name=?, phone=? WHERE id=?", (name, phone, contact_id))
    conn.commit()
    conn.close()

def delete_contact(contact_id):
    conn = sqlite3.connect("mydatabase.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE id=?", (contact_id,))
    conn.commit()
    conn.close()

# -----------------------------
# GUI Functions
# -----------------------------
def load_contacts():
    for row in tree.get_children():
        tree.delete(row)
    for contact in fetch_contacts():
        tree.insert("", tk.END, values=contact)

def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    if name and phone:
        insert_contact(name, phone)
        load_contacts()
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please fill out both fields.")

def edit_contact():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select Error", "No contact selected.")
        return
    contact_id = tree.item(selected)["values"][0]
    name = name_entry.get()
    phone = phone_entry.get()
    if name and phone:
        update_contact(contact_id, name, phone)
        load_contacts()
    else:
        messagebox.showwarning("Input Error", "Please fill out both fields.")

def remove_contact():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Select Error", "No contact selected.")
        return
    contact_id = tree.item(selected)["values"][0]
    delete_contact(contact_id)
    load_contacts()

def select_contact(event):
    selected = tree.selection()
    if selected:
        item = tree.item(selected)
        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        name_entry.insert(0, item["values"][1])
        phone_entry.insert(0, item["values"][2])

# -----------------------------
# Main App
# -----------------------------
init_db()

root = tk.Tk()
root.title("Tkinter SQLite3 Contact Manager")
root.geometry("500x400")

frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Name").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(frame)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Phone").grid(row=1, column=0, padx=5, pady=5)
phone_entry = tk.Entry(frame)
phone_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Button(frame, text="Add", command=add_contact).grid(row=2, column=0, pady=10)
tk.Button(frame, text="Update", command=edit_contact).grid(row=2, column=1, pady=10)
tk.Button(frame, text="Delete", command=remove_contact).grid(row=2, column=2, pady=10)

columns = ("ID", "Name", "Phone")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

tree.bind("<<TreeviewSelect>>", select_contact)

load_contacts()
root.mainloop()

