pyinstaller --paths=./src/lib --paths=./src/lib/assets --paths=data --windowed --noconsole --clean --onefile --icon=./src/assets/window_icon.ico --add-data "<PythonLocation>/Lib/site-packages/customtkinter;customtkinter" --name=renxel ./src/main.py

python3 ./compileZip.py