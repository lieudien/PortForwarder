#!/usr/bin/python3

try:
    from tkinter import *
except ImportError:
    print("tkinter is not available in this system. Please install tkinter package.")


LOCAL_SERVICE_PORTS = {}
PORT_HOSTS = {}
WORKER_THREADS = 0

class Application(Frame):

    width = 625
    height = 300
    lo_ports = [2200, 8000, 7000]
    des_ports = [22, 80, 7000]
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title("Configuration")
        self.master.geometry("{}x{}".format(self.width,self.height))
        self.create_forms()

    def create_forms(self):

        separator = '-'*50
        Label(self.master, text="PORT MAPPING", font='Helvetica 12 bold').grid(row=0, column=0, columnspan=2, sticky=W)
        Label(self.master, text=separator).grid(row=1, sticky=W)

        self.cur = 2
        for i in range(3):

            Label(self.master, text="Local Port").grid(row=self.cur, column=0)
            self.local_port = Entry(self.master)
            self.local_port.grid(row=self.cur+1, column=0)
            self.local_port.insert(0, self.lo_ports[i])

            Label(self.master, text="Destination Port").grid(row=self.cur, column=1)
            self.destination_port = Entry(self.master)
            self.destination_port.grid(row=self.cur+1, column=1)
            self.destination_port.insert(0, self.des_ports[i])

            Label(self.master, text="IP").grid(row=self.cur, column=2)
            self.ip = Entry(self.master, width=30)
            self.ip.grid(row=self.cur+1, column=2)

            ++i
            self.cur = self.cur + 2

        self.cur = self.cur + 1
        Label(self.master, text="THREADS CONFIGURATION", font='Helvetica 12 bold').grid(row=self.cur, column=0, columnspan=2, sticky=W)
        Label(self.master, text=separator).grid(row=self.cur+1, sticky=W)

        Label(self.master, text="Number of worker threads").grid(row=self.cur+3)
        self.num_threads = Entry(self.master)
        self.num_threads.grid(row=self.cur+4)
        self.num_threads.insert(0, 4)

        self.submit_button = Button(self.master, text="Submit", command=self.get_input)
        self.submit_button.grid(row=self.cur+7, sticky=N+S+E)

        self.quit_button = Button(self.master, text="Quit", command=self.master.quit)
        self.quit_button.grid(row=self.cur+7, column=2, sticky=N+S+W)


    def get_input(self):
        self.master.quit()

root = Tk()
app = Application(master=root)
app.mainloop()
