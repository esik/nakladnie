# nakladnie
Script for water order sort

Данный скрипт сортирует накладные из PDF в нужном порядке.

# Сборка на Windows
1. Потребуется pyinstaller `pip install pyinstaller`
2. Для сборки exe потребуется скачать tknd вручную и добавить содержимое в папку `C:\Users\username\AppData\Local\Programs\Python\Python39\tcl\tkdnd` [репозиторий](https://github.com/petasis/tkdnd/releases)
3. Сборка `pyinstaller --clean --onefile --windowed --name Nakladnie --icon=free-icon-water-bottle-1676499.ico --add-data "free-icon-water-bottle-1676499.png;." --add-data "C:\Users\username\AppData\Local\Programs\Python\Python39\tcl\tkdnd;tkdnd" nakl3.py`
