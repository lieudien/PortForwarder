#!/usr/bin/python3

try: 
    import tkinter as tk
except ImportError:
    print("tkinter is not available in this system. Please install tkinter package.")

class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_forms()

    def create_forms(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        self.quit.pack(side="bottom")

    def load_input(self):
        print("hi there, everyone")

root = tk.Tk()
app = Application(master=root)
app.mainloop()