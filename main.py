import csv
import glob
import pandas as pd
import time
from pandas import DataFrame


class RenpyToExcel():
    def __init__(self, fileName="dialogue"):
        self.fileName = fileName
        self.data = []
        self.get_data_from_tab()
        while self.data:
            self.generate_excel()
            break

    def get_data_from_tab(self):
        with open('dialogue.tab', 'r') as tab:
            rows = tab.readlines()[1:]
            for line in csv.reader(rows, delimiter="\t"):
                if line[1] == '':
                    tupla = (line[0], "None", line[2], " ")
                else:
                    tupla = (line[0], line[1], line[2], " ")

                self.data.append(tupla)

    def generate_excel(self):
        df = DataFrame(self.data, columns=[
                       'id', 'Character', 'Dialogue', 'Translation'])
        fil = self.fileName + '.xlsx'
        df.to_excel("out/xlsx/{}".format(fil), index=False)

        print("------------------------------------------")
        print(">>> Excel generated.")
        print(">>> path: out/xlsx/{}".format(fil))
        print("------------------------------------------")


class RenPyTLGenerator():

    def __init__(self, lang, excel, Outfilename="dialogue"):
        self.lang = lang
        self.Outfilename = Outfilename
        self.data = []
        self.csv = []
        self.excel = excel
        self.generator()
        self.write_translates()

    def generator(self):
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
        print("------------------------------------------")
        print(">>> Translation generated.")
        print(">>> path: out/rpy/{}.rpy".format(self.Outfilename))
        print("------------------------------------------")

if glob.glob("dialogue.tab"):
    print("""
    1) Generate excel file for translators
    2) Generate a new tl (.rpy) file with the excel file
    3) Close
    """)

    CHOICES = input()
    if CHOICES == "1":
        print("Do you want to name the file? [y/n]")
        QUESTION = input()
        if QUESTION == "y":
            print("What is the file going to be called (without the .xlsx)?")
            name = input()
            RenpyToExcel(name)
        else:
            RenpyToExcel()
    elif CHOICES == '2':
        if glob.glob("out/xlsx/*.xlsx"):
            print("What is the language of the translation? (it has to be the name of the folder you generated with renpy)")
            lang = input()

            print("What is the name of the excel file (without the .xlsx)?")
            excel = input()

            print("Do you want to name the file? [y/n]")
            QUESTION = input()

            while lang and excel:
                if QUESTION == 'y':
                    print("What will the rpy file be called? (without the .rpy)")
                    filename = input()
                    RenPyTLGenerator(lang, excel, filename)
                else:
                    RenPyTLGenerator(lang, excel)
                break
        else:
            print("------------------------------------------")
            print(">>> Excel file not found, generate it first.")
            print("------------------------------------------")

    elif CHOICES == "3":
        pass
else:
    print("------------------------------------------")
    print(">>> File dialogue.tab was not found")
    print("------------------------------------------")
