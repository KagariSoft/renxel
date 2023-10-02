pyinstaller --paths=./src/lib --paths=./src/lib/assets --paths=data --windowed --noconsole --clean --onefile --icon=./src/assets/window_icon.ico --add-data "/home/<user>/.local/lib/python3.10/site-packages/customtkinter:customtkinter" --name=renxel ./src/main.py

python3 ./compileZip.py