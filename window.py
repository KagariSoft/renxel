# Copyright (c) KagariSoft.

# Same has Ren'Py:
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import tkinter as tk
from tkinter import messagebox
import os
import lib.rpyExcel as rpyExcel


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

        self.excel = rpyExcel.RenpyToExcel(root, messagebox)

        self.langinp = tk.Entry(self.root, text="English", width=30)
        self.langinp.bind("<Key>", self.lang_inp)

        generate = tk.Button(
            self.root, text="Generate Excel", command=self.excel.get_data_from_tab)
        self.generaterpy = tk.Button(
            self.root, text="Generate Rpy", state="disabled", command=self.ButtonRPy)
        close = tk.Button(self.root, text="Close", command=self.Close)

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

        rpyExcel.RenPyTLGenerator(
            messagebox, lang=self.langinp.get()).generator()

    def lang_inp(self, e):

        if len(self.langinp.get()) > 0:
            self.generaterpy.config(state="normal")
            self.lang = self.langinp.get()
        else:
            self.generaterpy.config(state="disabled")
            self.lang = ""

    def Close(self):
        self.root.destroy()
        # self.langinp.config(text=self.lang)


def __main__():
    if not os.path.exists("out"):
        os.makedirs("out")
        os.makedirs("out/xlsx")
        os.makedirs("out/rpy")
        os.makedirs("out/temp")
    root = tk.Tk()
    Window(root)
    root.mainloop()


__main__()
