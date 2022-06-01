from logging import PlaceHolder
import tkinter as tk
from tkinter import messagebox
import glob

from click import command
import main


class Window():
    def __init__(self, root):
        self.root = root
        self.root.title("RenPy to Excel")
        self.rpyname = 'readonly'
        self.root.resizable(0, 0)
        self.root.configure(padx=10, pady=10)
        self.var = tk.IntVar()
        self.lang = ""
        self.langt = tk.StringVar()

        self.excel = main.RenpyToExcel(root, messagebox)

        self.langinp = tk.Entry(self.root, text="English", width=30)
        self.langinp.bind("<Key>", self.lang_inp)

        generate = tk.Button(
            self.root, text="Generate Excel", command=self.excel.get_data_from_tab)
        self.generaterpy = tk.Button(
            self.root, text="Generate Rpy", state="disabled", command=self.ButtonRPy)
        close = tk.Button(self.root, text="Close")
        text = tk.Label(self.root, text="Renpy Folder language name:")

        generate.grid(row=0, column=0)
        generate.config(font=("Helvetica", 11), width=23)
        self.generaterpy.config(font=("Helvetica", 11), width=23)
        self.generaterpy.grid(row=1, column=0)
        close.config(font=("Helvetica", 11), width=23)
        close.grid(row=2, column=0)
        self.langinp.grid(row=1, column=2, padx=10, pady=10)
        text.grid(row=0, column=2)

    def ButtonRPy(self):

        main.RenPyTLGenerator(
            messagebox, lang=self.langinp.get()).generator()

    def lang_inp(self, e):

        if len(self.langinp.get()) > 0:
            self.generaterpy.config(state="normal")
            self.lang = self.langinp.get()
        else:
            self.generaterpy.config(state="disabled")
            self.lang = ""
        # self.langinp.config(text=self.lang)


def __main__():
    root = tk.Tk()
    Window(root)
    root.mainloop()


__main__()
