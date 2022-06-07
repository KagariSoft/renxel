# Ren'Xel

## What is Ren'Xel?

Ren'Xel, is an app that generates an Excel file from renpy's `dialogue.tab` file using python technology,
it is also able to generate a `.rpy` translation file to import translations faster.

# How to use Ren'Xel

## From source code
### Install libraries

```bash
pip install -r requirements.txt
```

### Run Ren'Xel

```bash
python3 renxel.py
```
### How to build
    
```bash
$ ./build.sh
```
or
```bash
$ pyinstaller --paths=lib --windowed --noconsole --clean --onefile --name="renxel" renxel.py
```
# Getting Started

First you must generate a `dialogue.tab` file from renpy.

![](./screenshots/01.png)

Then from Ren'Xel you must use the `Generate Excel` button to generate a `dialogue.xlsx` file, which can be sent to the translators for translation.

To generate the `.rpy` file you must use the `Generate .rpy` button, but first, you must type the name of the language you are going to translate to, the folder name is in `game/tl/<Folder>`.


# How to add on your project
cut the file in `out/rpy/*.rpy` and paste it in your tl folder.
```tree
game/
├── tl/
    ├── [folder]/
        ├── [file].rpy
```
## What i need delete in tl folder?

You need delete only the script will contains dialogues and screens text.

example: `screen.rpy`, `scripts.rpy`, `options.rpy`

> **Note:** If you generated `dialogue.tab` by extracting only the dialogs, do not delete screen.rpy, options.rpy ![](./screenshots/02.png)



# Important notes:

* You may not get the script.rpy or screen.rpy files generated again if you regenerate the translation, don't panic. This is because they are now in a single file.

* Dialogue.tab does not take into account native renpy screens(`common.rpy`), so only translatable strings that exist inside the ./game or .game/* folder will be generated.

* Yo need generate a Ren'Py translation first, then you can use this script to generate file.

* No delete the `out` folder or the folders inside `out` folder.

* It is recommended to use this app only with finished projects, the app will not update already translated strings.
