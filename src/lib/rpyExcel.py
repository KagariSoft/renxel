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
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, data OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import json
import csv
import glob
import os
import shutil
import pandas as pd
import time
from pandas import DataFrame


class RenpyToExcel():
    def __init__(self, file):
        self.fileName = file
        self.data = []
        self.csv_temp = ""

    def tab_to_csv(self):
        if glob.glob(self.fileName):
            with open(self.fileName, 'r', encoding="UTF-8", newline='') as tab:
                rows = tab.readlines()[1:]
                lines = csv.reader(rows, delimiter="\t")
                for line in lines:
                    if line[1] == "":
                        t = (line[0], "None", line[2], " ")
                        self.data.append(t)
                    elif line[0] == "":
                        t = ("None", line[1], line[2], " ")
                        self.data.append(t)
                    else:
                        t = (line[0], line[1], line[2], " ")
                        self.data.append(t)

                while self.data:
                    time.sleep(1)
                    
                    return self.generate_excel()
                    
        else:
            return TypeError("No dialogue.tab file found in the current folder")


    def generate_excel(self):
        directory = os.getcwd()
        df = DataFrame(self.data, columns=[
                       'id', 'Character', 'Dialogue', 'Translation'])

        df.to_excel(directory+"/data/xlsx/dialogue.xlsx", index=False)

        time.sleep(1)
        self.data = []  # clear the cache
        
        return ("xlsx file generated in {}/data/xlsx, do you want to open the location? This file is the one you should send to the translator or use it to translate.".format(directory), directory+"/data/xlsx")


class RenPyTLGenerator():

    def __init__(self, excel="", gameFolder="" ,Outfilename="renxel", lang="",tl="off"):
        self.lang = lang
        self.tl = tl
        self.Outfilename = Outfilename
        self.gameFolder = gameFolder
        self.data = []
        self.csv = []
        self.excel = excel

    def generator(self):
        if self.lang != "":
            rows = pd.read_excel(self.excel, usecols=[
                'id', 'Character', 'Dialogue', 'Translation'])
            cv = rows.to_csv(index=False, index_label=False)

            with open("data/temp/dialogue.csv", "w", encoding="UTF-8") as c:
                c.write(cv)

            self.read_temporal_tab()
        else:
            return TypeError("You are not provider the language")

    def read_temporal_tab(self):

        with open("data/temp/dialogue.csv", 'r', encoding="UTF-8") as tab:
            rows = tab.readlines()[2:]
            lines = csv.reader(rows, delimiter=",")

            for l in lines:
                if len(l) > 0:
                    if l[0] == '':
                        t = ("type:screen", l[1], l[2], l[3])
                        self.data.append(t)
                    else:
                        t = (l[0], l[1], l[2], l[3])
                        self.data.append(t)

            while self.data:
                time.sleep(1)
                return self.write_translates()
               
    
    def copytree(self, src, dst, symlinks=False, ignore=None):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, symlinks, ignore)
            else:
                shutil.copy2(s, d)

    def write_translates(self):
        directory = os.getcwd()




        template_folder = directory+"\\data\\template\\{}".format(self.lang)
        tl_folder = "{}/game/tl/{}".format(self.gameFolder,self.lang)

        if not os.path.exists(tl_folder):
            os.makedirs(tl_folder)
        
        time.sleep(3)

        self.copytree(template_folder, tl_folder)

        time.sleep(3)

        with open('{}/game/tl/{}/{}.rpy'.format(self.gameFolder,self.lang,self.Outfilename), 'w', encoding="UTF-8") as tab:
            for i in self.data:

                if i[0] == "type:screen":
                    tab.write(u"translate {} {}:\n".format(
                        self.lang, "strings"))

                    tab.write(u'    old "{}"\n'.format(i[2]))
                    tab.write(u'    new "{}"\n'.format(i[3].strip()))
                else:
                    tab.write(u"translate {} {}:\n".format(
                        self.lang, i[0]))

                    if i[1] == "None":
                        tab.write(u'    # "{}"\n'.format(i[2]))
                        tab.write(u'    "{}"\n'.format(i[3].strip()))
                    else:
                        tab.write(u'    # {} "{}"\n'.format(i[1], i[2]))
                        tab.write(u'    {} "{}"\n'.format(i[1], i[3].strip()))

                tab.write(u"\n")

            self.data = []  # clear the cache

        return None
