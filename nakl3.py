import fitz  # PyMuPDF
import PyPDF2
import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, scrolledtext
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import PhotoImage
import os
import sys

# Файл с сохранённым списком накладных
LIST_FILE = "order_list.txt"

# Загружаем порядок накладных из файла или берём стандартный
DEFAULT_ORDER = [
    "Доломановский", "Турнир", "Нефедовский", "Амулет", "Калькулятор",
    "Смоловар", "Мышца", "Железнодорожный", "Катхиавари", "Вековой",
    "Правдолюбец", "Бригам", "Лиас", "Зоопсихолог", "Архивист", "Сироп",
    "Ошва", "Аксоран", "Престиж", "Пачули", "Детерминатив", "Буржуй",
    "Балканы", "Упругий", "Пикфорд", "Вельвет", "Квант", "Плеяда",
    "Баларама", "Жирондист", "Разбуривание", "Ведомая", "Стачки",
    "Зальцо", "Скиннер", "Нигрол", "Кардан", "Водомер", "Зола",
    "Теплоёмкость", "Пошив", "Батайск МД", "Подход", "Свитуотер",
    "Гастелло", "Льдинка", "Осанна", "РДВС", "Вечерняя заря"
]

def load_order():
    # Загружает порядок накладных из файла, если он есть
    if os.path.exists(LIST_FILE):
        with open(LIST_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines() if line.strip()]
    return DEFAULT_ORDER

def save_order(new_order):
    # Сохраняет новый порядок накладных в файл
    with open(LIST_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(new_order))

def process_pdf(input_pdf):
    # Обрабатывает PDF, сортируя накладные в нужном порядке
    if not input_pdf:
        messagebox.showwarning("Ошибка", "Выберите PDF-файл!")
        return

    output_pdf = input_pdf.replace(".pdf", "_sorted.pdf")
    order = load_order()

    doc = fitz.open(input_pdf)
    page_mapping = {}

    for i in range(len(doc)):
        text = doc[i].get_text("text")
        for keyword in order:
            full_phrase_mm = f'АО "Тандер" ММ "{keyword}"'
            full_phrase_mn = f'АО "Тандер" м-н {keyword}'  # Без кавычек
            if (full_phrase_mm in text or full_phrase_mn in text) and keyword not in page_mapping:
                page_mapping[keyword] = i

    pages = [page_mapping[k] for k in order if k in page_mapping]

    if not pages:
        messagebox.showwarning("Ошибка", "Не найдено ни одной накладной!")
        return

    reader = PyPDF2.PdfReader(input_pdf)
    writer = PyPDF2.PdfWriter()
    for page_num in pages:
        writer.add_page(reader.pages[page_num])

    with open(output_pdf, "wb") as f:
        writer.write(f)

    messagebox.showinfo("Готово!", f"Файл сохранён как:\n{output_pdf}")

def select_file():
    # Открывает диалог выбора PDF
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    entry_var.set(file_path)

def drop(event):
    # Обрабатывает Drag & Drop
    file_path = event.data.strip("{}")
    entry_var.set(file_path)

def edit_order():
    # Открывает окно для редактирования списка накладных
    def save_and_close():
        # Сохраняет новый список и закрывает окно
        new_list = text_area.get("1.0", tk.END).strip().split("\n")
        save_order(new_list)
        order_window.destroy()
        messagebox.showinfo("Сохранено", "Новый порядок накладных сохранён.")

    order_window = Toplevel(root)
    order_window.title("Редактировать список")
    order_window.geometry("280x260")  # Сделал компактнее
    order_window.resizable(False, False)

    # Текстовое поле с прокруткой
    text_area = scrolledtext.ScrolledText(order_window, wrap=tk.WORD, width=40, height=12)
    text_area.pack(pady=10, padx=10)  # Равномерные отступы

    # Загружаем текущий список
    text_area.insert(tk.END, "\n".join(load_order()))

    # Кнопка сохранить
    btn_save = tk.Button(order_window, text="Сохранить", command=save_and_close, width=20)
    btn_save.pack(pady=5)  # Отступ снизу

# Создание GUI
root = TkinterDnD.Tk()
root.title("Сортировка накладных")
root.geometry("280x160")  # Уменьшил размер окна
root.resizable(False, False)

entry_var = tk.StringVar()

# Поле выбора файла
entry = tk.Entry(root, textvariable=entry_var, width=40)
entry.pack(pady=10)

entry.drop_target_register(DND_FILES)
entry.dnd_bind("<<Drop>>", drop)

# Кнопки
btn_width = 20  # Одинаковая ширина кнопок
btn_padding = 5  # Отступы между кнопками

btn_select = tk.Button(root, text="Выбрать PDF", command=select_file, width=btn_width)
btn_select.pack(pady=btn_padding)

btn_process = tk.Button(root, text="Сортировать", command=lambda: process_pdf(entry_var.get()), width=btn_width)
btn_process.pack(pady=btn_padding)

btn_edit = tk.Button(root, text="Редактировать список", command=edit_order, width=btn_width)
btn_edit.pack(pady=btn_padding)

# Загрузка иконки
def resource_path(relative_path):
    # Получает путь к файлу, который корректно работает и в .exe, и в обычном режиме
    if getattr(sys, 'frozen', False):  # Если запущено как .exe
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")  # Обычный запуск из Python
    return os.path.join(base_path, relative_path)

# Загружаем иконку с правильным путём
icon_path = resource_path("free-icon-water-bottle-1676499.png")
icon = PhotoImage(file=icon_path)  # Устанавливаем иконку
root.iconphoto(True, icon)

# Запуск GUI
root.mainloop()