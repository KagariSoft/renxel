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

import requests
import lib.rpyExcel as rpyExcel
import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import webbrowser as wb

_version = "1.0.7"
_debug_version = "1.0.2"


class Window():
    def __init__(self, root):
        self.root = root
        self.root.title("Ren'Xel")

        self.rpyname = 'readonly'
        self.root.resizable(0, 0)
        self.root.configure(padx=10, pady=10)
        self.var = tk.IntVar()
        self.lang = ""
        self.langt = tk.StringVar()

        self.langinp = tk.Entry(self.root, text="English", width=30)
        self.langinp.bind("<Key>", self.lang_inp)

        generate = tk.Button(
            self.root, text="Generate Excel", command=self.OpenTab)
        self.generaterpy = tk.Button(
            self.root, text="Generate Rpy", state="disabled", command=self.OpenExcel)
        donate = tk.Button(self.root, text="Donate", command=self.Donate)
        close = tk.Button(self.root, text="Close", command=self.Close)

        text = tk.Label(self.root, text="Ren'Py Folder language name:")

        generate.grid(row=0, column=0)
        generate.config(font=("Helvetica", 11), width=23)
        self.generaterpy.config(font=("Helvetica", 11), width=23)
        self.generaterpy.grid(row=1, column=0)
        donate.config(font=("Helvetica", 11), width=23)
        donate.grid(row=2, column=0)

        close.config(font=("Helvetica", 11), width=23)
        close.grid(row=3, column=0)
        self.langinp.grid(row=1, column=2, padx=10, pady=10)
        text.grid(row=0, column=2)

    def lang_inp(self, e):

        if len(self.langinp.get()) > 0:
            self.generaterpy.config(state="normal")
            self.lang = self.langinp.get()
        else:
            self.generaterpy.config(state="disabled")
            self.lang = ""

    def OpenTab(self):
        filename = filedialog.askopenfilename(
            initialdir="/",
            title="Select tab file",
            filetypes=[("TAB file", "*.tab")]
        )
        if filename:
            rpyExcel.RenpyToExcel(self.root,
                                  messagebox, file=filename).tab_to_csv()

    def OpenExcel(self):
        filename = filedialog.askopenfilename(
            initialdir="/",
            title="Select xlsx file",
            filetypes=[("Excel file", "*.xlsx")]
        )
        if filename:
            rpyExcel.RenPyTLGenerator(
                messagebox, excel=filename, lang=self.langinp.get()).generator()

    def Donate(self):
        wb.open_new("https://ko-fi.com/kagarisoft")

    def Close(self):
        self.root.destroy()


def CheckVersion(root):
    try:
        result = requests.get(
            "https://api.github.com/repos/KagariSoft/renxel/releases/latest")
        version = result.json()["tag_name"]
        if version > _version:
            msg = messagebox.askokcancel(message="Ren'Xel detected that there is a new version, do you want to update the app? This will open the Itch page.",
                                         title="New version available v{}".format(version))
            if msg:
                wb.open("https://kagarisoft.itch.io/renxel")
                root.destroy()

        else:
            print("No new version available")

    except Exception as e:
        print(e)


def __main__():
    if not os.path.exists("out"):
        os.makedirs("out")
        os.makedirs("out/xlsx")
        os.makedirs("out/rpy")
        os.makedirs("out/temp")

    CheckVersion(root)


__main__()
