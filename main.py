
import csv
import glob
from re import S
import pandas as pd
import time
from pandas import DataFrame

import tkinter as tk


class RenpyToExcel():
    def __init__(self, root, messagebox, fileName="dialogue"):
        self.fileName = fileName
        self.data = []
        self.root = root
        self.messagebox = messagebox

    def get_data_from_tab(self):
        if glob.glob("dialogue.tab"):
            with open('dialogue.tab', 'r') as tab:
                rows = tab.readlines()[1:]
                for line in csv.reader(rows, delimiter="\t"):
                    if line[1] == '':
                        tupla = (line[0], "None", line[2], " ")
                    else:
                        tupla = (line[0], line[1], line[2], " ")

                    self.data.append(tupla)
                self.generate_excel()
        else:
            self.messagebox.showerror(
                "Error", "No dialogue.tab file found in the current folder")

    def generate_excel(self):
        df = DataFrame(self.data, columns=[
                       'id', 'Character', 'Dialogue', 'Translation'])
        fil = self.fileName + '.xlsx'
        df.to_excel("out/xlsx/{}".format(fil), index=False)

        self.messagebox.showinfo(
            "Info", "xlsx file generated in out/xlsx/{}".format(fil))


class RenPyTLGenerator():

    def __init__(self, messagebox, excel="dialogue", Outfilename="dialogue", lang=""):
        self.lang = lang
        self.Outfilename = Outfilename
        self.data = []
        self.csv = []
        self.messagebox = messagebox
        self.excel = excel

    def generator(self):

        if self.lang != "":
            if glob.glob("out/xlsx/*.xlsx"):

                fil = self.excel + '.xlsx'
                rows = pd.read_excel("out/xlsx/{}".format(fil), usecols=[
                    'id', 'Character', 'Dialogue', 'Translation'])
                cv = rows.to_csv(index=False, index_label=False)

                with open('out/temp/dialogue.tab', 'w') as f:
                    f.write(cv)

                time.sleep(1)
                with open('out/temp/dialogue.tab', 'r') as tab:
                    rows = tab.readlines()[1:]
                    for line in csv.reader(rows):

                        if line[1] == '':
                            tupla = (line[0], "None", line[2], line[3])
                        elif line[0] == '':
                            tupla = ("string", line[1], line[2], line[3])
                        else:
                            tupla = (line[0], line[1], line[2], line[3])

                        self.data.append(tupla)
                    self.write_translates()
            else:
                self.messagebox.showerror(
                    "Error", "No xlsx file found")
        else:
            self.messagebox.showerror(
                "Error", "You are not provider the language")

    def write_translates(self):
        if self.Outfilename != "dialogue":
            with open('out/rpy/dialogue.rpy', 'w') as tab:
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
        else:
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


# if glob.glob("dialogue.tab"):
#     print("""
#     1) Generate excel file for translators
#     2) Generate a new tl (.rpy) file with the excel file
#     3) Close
#     """)

#     CHOICES = input()
#     if CHOICES == "1":
#         RenpyToExcel()
#     elif CHOICES == '2':
#         if glob.glob("out/xlsx/*.xlsx"):
#             print("What is the language of the translation? (it has to be the name of the folder you generated with renpy)")
#             lang = input()

#             print("Do you want to name the file? [y/n]")
#             QUESTION = input()

#             while lang:
#                 if QUESTION == 'y':
#                     print("What will the rpy file be called? (without the .rpy)")
#                     filename = input()
#                     RenPyTLGenerator(lang, Outfilename=filename)
#                 else:
#                     RenPyTLGenerator(lang)
#                 break
#         else:
#             print("------------------------------------------")
#             print(">>> Excel file not found, generate it first.")
#             print("------------------------------------------")
#     elif CHOICES == "3":
#         pass
# else:
#     print("------------------------------------------")
#     print(">>> File dialogue.tab was not found")
#     print("------------------------------------------")
