import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from pathlib import Path
import webbrowser as wb
import requests
import lib.rpyExcel as rpyExcel
import os
import configparser

ctk.set_appearance_mode("dark")


### Default variables
config = configparser.ConfigParser()
config.read('./data/settings.ini')

sections = config.sections()

FOLDER_ROOT = config['app']['rootFolder']


_VERSION = "1.0.10"
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"./assets")
GITHUB_URL = "https://api.github.com/repos/KagariSoft/renxel/releases/latest"
DONATE_URL = "https://ko-fi.com/kagarisoft"


class App(ctk.CTk):
    # 369x485
    width = 369
    height = 485
 

    button_width = 338
    button_height = 41
    update_button_state = "disabled"
    generate_button_state = "disabled"
    rpy_button_state = "disabled"

    language_list = [
        "Select language",
    ]

    language_selected = ""

    gameFolder_root = ""

    renxel_file = ""

    checkbox_confirm_message = "Generate translate folder"

    all_translatable_strings = "off"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.CheckVersion()
        self.title("Ren'Xel")

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x_cordinate = int((screen_width/2) - (self.width/2))
        y_cordinate = int((screen_height/2) - (self.height/2))

        self.geometry(f"{self.width}x{self.height}+{x_cordinate}+{y_cordinate}")
        self.resizable(False, False)
        self.iconbitmap('window_icon.ico')

        # Frames
        self.home_container = ctk.CTkFrame(self, fg_color="transparent")
        self.generator_container = ctk.CTkFrame(self,fg_color="transparent")
        

        # Default Show
        self.home_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Pages

        self.Home()

        self.Generator()

        # Global

        app_version = ctk.CTkLabel(self, text=_VERSION)
        app_version.pack(side=tk.BOTTOM)



    def Home(self):
        
        
        self.excel = ctk.CTkButton(
                self.home_container,
            text="Open base folder",
                width=self.button_width,
                height=self.button_height,
                command=lambda: self.setGameFolder()
        )

        self.rxcel = ctk.CTkButton(
                self.home_container,
                text="Import Ren'Xel generated",
                width=self.button_width,
                height=self.button_height,
                state="disabled",
                command=lambda: self.ImportExcel()
        )
        
        self.rpy = ctk.CTkButton(
                self.home_container,
                text="Generate Translation",
                width=self.button_width,
                height=self.button_height,
                state=self.rpy_button_state,
                command=lambda: {
                    self.home_container.pack_forget(),
                    self.generator_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                }
        )

        update_button = ctk.CTkButton(
                self.home_container,
                text="Update App",
                width=self.button_width,
                height=self.button_height,
                state=self.update_button_state,
                command=lambda: wb.open_new("https://kagarisoft.itch.io/renxel")
        )
        
        donate = ctk.CTkButton(
                self.home_container,
                text="Donate",
                width=self.button_width,
                height=self.button_height,
                command=lambda: wb.open_new(DONATE_URL)
        )
        
        close_app = ctk.CTkButton(
                self.home_container,
                text="Close App",
                width=self.button_width,
                height=self.button_height,
                command=lambda: self.destroy()
        )


        # Pack
        
        self.excel.pack(padx=20, pady=10)
        self.rxcel.pack(padx=20, pady=10)
        self.rpy.pack(padx=20, pady=10)
        update_button.pack(padx=20, pady=10)
        donate.pack(padx=20, pady=10)
        close_app.pack(padx=20,pady=3, side=tk.BOTTOM)
    
    def Generator(self):
        directory = os.getcwd()
        lng = ctk.CTkLabel(self.generator_container, text="Select Language for Translation")

        lang_templates_folders="{}\\data\\template".format(directory)

        for item in os.listdir(lang_templates_folders):
            self.language_list.append(item)
            
        language_select = ctk.CTkOptionMenu(self.generator_container,
                                       values=self.language_list,
                                       command=self.langmenu_callback
                        )
        
        language_select.set("Select language")  # set initial value

        read_more = ctk.CTkButton(
            master=self.generator_container, 
            text="Read More",
            fg_color="transparent",
            command=lambda: wb.open_new("https://github.com/KagariSoft/renxel/wiki/Info#language-folder")
        )

        
        self.generate = ctk.CTkButton(
                self.generator_container,
                text="Generate",
                width=self.button_width,
                height=self.button_height,
                state=self.generate_button_state,
                command=self.generateRpy
        )

        home_button = ctk.CTkButton(
                self.generator_container,
                text="Return",
                width=self.button_width,
                height=self.button_height,
                command=lambda: {
                    self.generator_container.pack_forget(),
                    self.home_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                }
        )

        lng.pack(padx=20,pady=3)

        language_select.pack(padx=20,pady=10, fill=tk.X)

     

        read_more.pack(padx=20, pady=2)

        self.generate.pack(padx=20,pady=3, side=tk.BOTTOM)

        home_button.pack(padx=20,pady=3, side=tk.BOTTOM)

 

    def setGameFolder(self):
        folder_selected = filedialog.askdirectory(initialdir=FOLDER_ROOT)
        if folder_selected:
            if os.path.basename(folder_selected) != "game":
                self.gameFolder_root = folder_selected
                self.excel.configure(text="Generate Excel",
                                     command=self.generateExcel)
                self.rxcel.configure(state="normal")
            else:
                messagebox.showinfo("error",
                                    "(%s) It cannot be used as root folder, the folder to be chosen must be the base folder, where the game folder is located." % (folder_selected))

    
    def ImportExcel(self):

        filename = filedialog.askopenfilename(
            initialdir="/",
            title="Select xlsx file",
            filetypes=[("Excel file", "*.xlsx")]
        )

        if filename:
            self.rpy_button_state = "normal"
            self.rpy.configure(state=self.rpy_button_state)
            self.renxel_file = filename
            messagebox.showinfo("Info", "The file location has been imported, now you can generate the translation.")
    
    def generateRpy(self):
        try:
            generator = rpyExcel.RenPyTLGenerator(self.renxel_file,self.gameFolder_root,lang=self.language_selected).generator()
            
            if generator == None:
                q = messagebox.askquestion("Info", "The .rpy file was generated, do you want to open the location?")
                
                if q == 'yes':
                    wb.open(f"{self.gameFolder_root}/game/tl/{self.language_selected}")

        except Exception as e:
            messagebox.showinfo("Exception", e)
            print("Exception",e)
    
            
    def generateExcel(self):

        file = "{}/dialogue.tab".format(self.gameFolder_root)
  
 
        try:
            generator = rpyExcel.RenpyToExcel(file).tab_to_csv()


            
            q = messagebox.askquestion("Info", generator[0])
            if q == 'yes':
                wb.open(generator[1])

        except Exception as e:
            messagebox.showinfo("Exception", e)
            print("Exception",e)
        

    def langmenu_callback(self,choice):

        if choice != "Select language":
            self.generate_button_state = "normal"
            self.generate.configure(state=self.generate_button_state)
            self.language_selected = choice
        
        else:
            self.generate_button_state = "disabled"
            self.generate.configure(state=self.generate_button_state)
            self.language_selected = ""

            
    def relative_to_assets(self, path: str) -> Path:
        return ASSETS_PATH / Path(path)

    def CheckVersion(self):
        try:
            result = requests.get(GITHUB_URL)
            version = result.json()["tag_name"]

            if version > _VERSION:
                self.update_button_state = "normal"

        except Exception as e:
            print(e)


if __name__ == "__main__":
    app = App()
    app.mainloop()
