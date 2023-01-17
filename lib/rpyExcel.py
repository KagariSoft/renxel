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

import csv
import glob
import os
import pandas as pd
import time
from pandas import DataFrame


class RenpyToExcel():
    def __init__(self, root, messagebox, file):
        self.fileName = file
        self.data = []
        self.root = root
        self.messagebox = messagebox
        self.csv_temp = ""

    def tab_to_csv(self):
        if glob.glob(self.fileName):
            with open(self.fileName, 'r', encoding="UTF-8", newline='') as tab:
                rows = tab.readlines()[1:]
                lines = csv.reader(rows, delimiter="\t")
                for line in lines:
                    if line[1] == '':
                        t = (line[0], "None", line[2], " ")
                        self.data.append(t)
                    else:
                        t = (line[0], line[1], line[2], " ")
                        self.data.append(t)

                while self.data:
                    time.sleep(1)
                    self.generate_excel()
                    break
        else:
            self.messagebox.showerror(
                "Error", "No dialogue.tab file found in the current folder")

    def generate_excel(self):
        directory = os.getcwd()

        df = DataFrame(self.data, columns=[
                       'id', 'Character', 'Dialogue', 'Translation'])

        df.to_excel(directory+"/out/xlsx/dialogue.xlsx", index=False)

        time.sleep(1)

        self.messagebox.showinfo(
            "Info", "xlsx file generated in {}/out/xlsx/dialogue.xlsx").format(directory)

        self.data = []  # clear the cache


class RenPyTLGenerator():

    def __init__(self, messagebox, excel="", Outfilename="script_translation", lang=""):
        self.lang = lang
        self.Outfilename = Outfilename
        self.data = []
        self.csv = []
        self.messagebox = messagebox
        self.excel = excel

    def generator(self):
        if self.lang != "":
            rows = pd.read_excel(self.excel, usecols=[
                'id', 'Character', 'Dialogue', 'Translation'])
            cv = rows.to_csv(index=False, index_label=False)

            with open('out/temp/dialogue.tab', 'w', encoding="UTF-8", newline='') as f:

                f.write(cv)

                time.sleep(1)

                # TODO: FAIL HERE

                self.read_temporal_tab()

        else:
            self.messagebox.showerror(
                "Error", "You are not provider the language")

    def read_temporal_tab(self):

        with open("out/temp/dialogue.tab", 'r', encoding="UTF-8", newline='') as tab:
            rows = tab.readlines()[1:]
            lines = csv.reader(rows, delimiter="\t")

            for line in lines:
                if line[1] == '':
                    tupla = (line[0], "None", line[2], line[3])
                    self.data.append(tupla)
                elif line[0] == '':
                    tupla = ("string", line[1], line[2], line[3])
                    self.data.append(tupla)
                else:
                    tupla = (line[0], line[1], line[2], line[3])
                    self.data.append(tupla)

            while self.data:
                time.sleep(1)
                self.write_translates()
                break

    def write_translates(self):
        with open('out/rpy/{}.rpy'.format(self.Outfilename), 'w') as tab:
            for i in self.data:

                if i[0] == "string":
                    tab.write(u"translate {} {}:\n".format(
                        self.lang, "strings"))

                    tab.write(u'    old "{}"\n'.format(i[2]))
                    tab.write(u'    new "{}"\n'.format(i[3]))
                else:
                    tab.write(u"translate {} {}:\n".format(
                        self.lang, i[0]))

                    if i[1] == "None":
                        tab.write(u'    # "{}"\n'.format(i[2]))
                        tab.write(u'    "{}"\n'.format(i[3]))
                    else:
                        tab.write(u'    # {} "{}"\n'.format(i[1], i[2]))
                        tab.write(u'    {} "{}"\n'.format(i[1], i[3]))

                tab.write(u"\n")
            self.messagebox.showinfo(
                "Info", "rpy file generated in out/rpy/{}.rpy".format(self.Outfilename))

            self.data = []  # clear the cache
