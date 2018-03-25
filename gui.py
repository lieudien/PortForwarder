#!/usr/bin/python3

try:
    from tkinter import *
except ImportError:
    print("tkinter is not available. Command: dnf install tkinter")

def show_entry_fields():
    print("Nothing")

master = tk()

master.title("Configuration")

Label(master, text="Port").grid(row=0)
e1 = Entry(master, width=10).grid(row=0, column=1)
Label(master, text="Address").grid(row=0, column=2)
e2 = Entry(master).grid(row=0, column=3)
Label(master, text="Port").grid(row=1)
e3 = Entry(master, width=10).grid(row=1, column=1)
Label(master, text="Address").grid(row=1, column=2)
e4 = Entry(master).grid(row=1, column=3)

Button(master, text="Submit", command=show_entry_fields).grid(row=3, column=1, sticky=W, pady=5)
Button(master, text="Quit", command=master.quit).grid(row=3, column=0, sticky=W, pady=5)

mainloop()
