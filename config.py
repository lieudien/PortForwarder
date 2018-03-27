#!/usr/bin/python3
try:
    from tkinter import *
except ImportError:
    print("tkinter is not available in this system. Please install tkinter package.")
from tkinter import messagebox

master = Tk()

width = 625
height = 300
lo_ports = [2200, 8000, 7000]
des_ports = [22, 80, 7000]

entries = []
LOCAL_SERVICE_PORTS = {}
PORT_HOSTS = {}
WORKER_THREADS = 0

master.title("Configuration")
master.geometry("{}x{}".format(width,height))

separator = "-" * 100

Label(master, text="PORT MAPPING", font='Helvetica 12 bold').grid(row=0, column=0, columnspan=3, sticky=W)
Label(master, text=separator).grid(row=1, column=0, columnspan=3, sticky=W)

cur = 2
for i in range(3):
    j = 0
    entries.append([])

    Label(master, text="Local Port").grid(row=cur, column=0)
    entries[i].append(Entry(master))
    entries[i][j].grid(row=cur+1, column=0)
    entries[i][j].insert(0, lo_ports[i])

    Label(master, text="Destination Port").grid(row=cur, column=1)
    entries[i].append(Entry(master))
    entries[i][j+1].grid(row=cur+1, column=1)
    entries[i][j+1].insert(0, des_ports[i])

    Label(master, text="IP").grid(row=cur, column=2)
    entries[i].append(Entry(master, width=30))
    entries[i][j+2].grid(row=cur+1, column=2)

    ++i
    cur = cur + 2

cur = cur + 1
Label(master, text="THREADS CONFIGURATION", font='Helvetica 12 bold').grid(row=cur, column=0, columnspan=3, sticky=W)
Label(master, text=separator).grid(row=cur+1, column=0, columnspan=3, sticky=W)

Label(master, text="Number of worker threads").grid(row=cur+3)
num_threads = Entry(master)
num_threads.grid(row=cur+4)
num_threads.insert(0, 4)

def get_input():
    checked = 0
    threads = num_threads.get()
    if (threads == ''):
        checked = 1
        messagebox.showinfo("Error", "Number of worker threads cannot be 0")

    WORKER_THREADS = threads

    for i in range(len(entries[0])):
        for j in range(len(entries[0])):
            if (len(entries[i][j].get()) == 0):
                checked = 1
                messagebox.showinfo("Error", "[{},{}] cannot be emptied".format(i,j))
                break
            else:
                LOCAL_SERVICE_PORTS[entries[i][1].get()] = entries[i][0].get()
                PORT_HOSTS[entries[i][1].get()] = entries[i][2].get()
    print (LOCAL_SERVICE_PORTS)
    print(PORT_HOSTS)
    if (checked == 0):
        master.quit()

submit_button = Button(master, text="Submit", command=get_input)
submit_button.grid(row=cur+7, sticky=N+S+E)

quit_button = Button(master, text="Quit", command=master.quit)
quit_button.grid(row=cur+7, column=2, sticky=N+S+W)


master.mainloop()
