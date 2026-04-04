from tkinter import *
from tkinter import filedialog as fd
from tkinter import messagebox
from dec import KAsiski, ENG_ALFABET, RU_ALFABET, enFreq, ruFreq
from Vigen import Vigenere

# Шрифты
FONT_MAIN = ("Segoe UI", 10)
FONT_TEXT = ("Consolas", 11)
FONT_BUTTON = ("Segoe UI", 9, "bold")


class VApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Шифр Виженера - Шифрование/Дешифрование/Взлом")
        self.root.geometry("750x520")
        self.root.configure(bg="#f0f0f0")

        # Переменные
        self.language = StringVar(value="eng")
        self.alphabet = ENG_ALFABET
        self.freq = enFreq

        # Настройка стилей
        self.setup_styles()

        # Создание интерфейса
        self.create_widgets()

        # Привязка горячих клавиш
        self.bind_hotkeys()

    def setup_styles(self):
        """Настройка цветовой схемы и стилей"""
        self.bg_color = "#f5f5f5"
        self.fg_color = "#2c3e50"
        self.button_bg = "#3498db"
        self.button_fg = "white"
        self.frame_bg = "#ffffff"
        self.root.configure(bg=self.bg_color)

    def bind_hotkeys(self):
        """Привязка Ctrl+C, Ctrl+V, Ctrl+A для всех текстовых полей"""
        for widget in [self.message_text, self.result_text, self.key_entry]:
            widget.bind('<Control-c>', self.copy)
            widget.bind('<Control-C>', self.copy)
            widget.bind('<Control-v>', self.paste)
            widget.bind('<Control-V>', self.paste)
            widget.bind('<Control-a>', self.select_all)
            widget.bind('<Control-A>', self.select_all)

    def copy(self, event):
        """Копирование выделенного текста"""
        try:
            event.widget.event_generate('<<Copy>>')
            return 'break'
        except:
            return None

    def paste(self, event):
        """Вставка текста из буфера обмена"""
        try:
            event.widget.event_generate('<<Paste>>')
            return 'break'
        except:
            return None

    def select_all(self, event):
        """Выделение всего текста в поле"""
        event.widget.tag_add(SEL, "1.0", END)
        event.widget.mark_set(INSERT, "1.0")
        event.widget.see(INSERT)
        return 'break'

    def create_widgets(self):
        # Рамка для выбора языка
        lang_frame = LabelFrame(self.root, text="Язык", padx=10, pady=5,
                                font=FONT_MAIN, bg=self.frame_bg, fg=self.fg_color)
        lang_frame.place(x=10, y=10, width=150, height=80)

        Radiobutton(lang_frame, text="English", value="eng", variable=self.language,
                    command=self.change_language, font=FONT_MAIN, bg=self.frame_bg).pack(anchor=W, pady=2)
        Radiobutton(lang_frame, text="Русский", value="ru", variable=self.language,
                    command=self.change_language, font=FONT_MAIN, bg=self.frame_bg).pack(anchor=W, pady=2)

        # Рамка для исходного текста
        input_frame = LabelFrame(self.root, text="Исходный текст / Зашифрованный текст для взлома",
                                 padx=10, pady=5, font=FONT_MAIN, bg=self.frame_bg, fg=self.fg_color)
        input_frame.place(x=170, y=10, width=570, height=150)

        self.message_text = Text(input_frame, width=65, height=6, wrap=WORD,
                                 font=FONT_TEXT, bg="white", fg="#2c3e50",
                                 relief=FLAT, bd=1)
        self.message_text.pack(side=LEFT, fill=BOTH, expand=True)

        scroll_input = Scrollbar(input_frame, command=self.message_text.yview)
        scroll_input.pack(side=RIGHT, fill=Y)
        self.message_text.config(yscrollcommand=scroll_input.set)

        # Кнопки для работы с файлом
        btn_frame = Frame(self.root, bg=self.bg_color)
        btn_frame.place(x=10, y=100, width=150, height=100)

        Button(btn_frame, text="📂 Открыть файл", command=self.open_file,
               font=FONT_BUTTON, bg=self.button_bg, fg=self.button_fg,
               relief=RAISED, bd=1, cursor="hand2").pack(pady=3, fill=X)
        Button(btn_frame, text="🗑 Очистить", command=self.clear_text,
               font=FONT_BUTTON, bg="#e74c3c", fg=self.button_fg,
               relief=RAISED, bd=1, cursor="hand2").pack(pady=3, fill=X)

        # Рамка для ключа
        key_frame = LabelFrame(self.root, text="Ключ (для шифрования/расшифровки)",
                               padx=10, pady=5, font=FONT_MAIN, bg=self.frame_bg, fg=self.fg_color)
        key_frame.place(x=10, y=210, width=730, height=60)

        self.key_entry = Entry(key_frame, width=60, font=FONT_TEXT,
                               bg="white", fg="#2c3e50", relief=FLAT, bd=1)
        self.key_entry.pack(side=LEFT, padx=5, fill=X, expand=True)
        Button(key_frame, text="✖ Очистить", command=self.clear_key,
               font=FONT_BUTTON, bg="#95a5a6", fg=self.button_fg,
               relief=RAISED, bd=1, cursor="hand2").pack(side=RIGHT, padx=5)

        # Рамка для кнопок операций
        operations_frame = Frame(self.root, bg=self.bg_color)
        operations_frame.place(x=10, y=280, width=730, height=45)

        Button(operations_frame, text="🔒 Зашифровать", command=self.do_encrypt,
               font=FONT_BUTTON, bg="#27ae60", fg=self.button_fg,
               relief=RAISED, bd=1, cursor="hand2").pack(side=LEFT, padx=5)
        Button(operations_frame, text="🔓 Расшифровать (с ключом)", command=self.do_decrypt_with_key,
               font=FONT_BUTTON, bg="#2980b9", fg=self.button_fg,
               relief=RAISED, bd=1, cursor="hand2").pack(side=LEFT, padx=5)
        Button(operations_frame, text="⚡ ВЗЛОМАТЬ (без ключа)", command=self.do_crack,
               font=FONT_BUTTON, bg="#e67e22", fg=self.button_fg,
               relief=RAISED, bd=1, cursor="hand2").pack(side=LEFT, padx=5)

        # Рамка для результата
        result_frame = LabelFrame(self.root, text="Результат",
                                  padx=10, pady=5, font=FONT_MAIN, bg=self.frame_bg, fg=self.fg_color)
        result_frame.place(x=10, y=335, width=730, height=170)

        self.result_text = Text(result_frame, width=65, height=8, wrap=WORD,
                                font=FONT_TEXT, bg="#fef9e7", fg="#2c3e50",
                                relief=FLAT, bd=1)
        self.result_text.pack(side=LEFT, fill=BOTH, expand=True)

        scroll_result = Scrollbar(result_frame, command=self.result_text.yview)
        scroll_result.pack(side=RIGHT, fill=Y)
        self.result_text.config(yscrollcommand=scroll_result.set)

        # Метка для отображения найденного ключа
        self.key_label = Label(self.root, text="", font=FONT_MAIN,
                               fg="#2980b9", bg=self.bg_color)
        self.key_label.place(x=10, y=510)

    def change_language(self):
        if self.language.get() == "eng":
            self.alphabet = ENG_ALFABET
            self.freq = enFreq
        else:
            self.alphabet = RU_ALFABET
            self.freq = ruFreq

    def get_text(self):
        return self.message_text.get(1.0, END).strip().lower()

    def set_result(self, text):
        self.result_text.delete(1.0, END)
        self.result_text.insert(1.0, text)

    def clear_text(self):
        self.message_text.delete(1.0, END)

    def clear_key(self):
        self.key_entry.delete(0, END)
        self.key_label.config(text="")

    def open_file(self):
        file_name = fd.askopenfilename()
        if file_name:
            with open(file_name, "r", encoding="utf-8") as f:
                self.message_text.insert(1.0, f.read())

    def do_encrypt(self):
        text = self.get_text()
        key = self.key_entry.get().strip().lower()

        if not text or not key:
            messagebox.showwarning("Ошибка", "Введите текст и ключ")
            return

        result = Vigenere.encryption(text, key, self.alphabet)
        self.set_result(result)

    def do_decrypt_with_key(self):
        text = self.get_text()
        key = self.key_entry.get().strip().lower()

        if not text or not key:
            messagebox.showwarning("Ошибка", "Введите текст и ключ")
            return

        result = Vigenere.decrypion(text, key, self.alphabet)
        self.set_result(result)

    def do_crack(self):
        text = self.get_text()

        if not text:
            messagebox.showwarning("Ошибка", "Введите текст для взлома")
            return

        key, decrypted = KAsiski.crack_vigenere(text, self.alphabet, self.freq)

        if not key:
            self.set_result(decrypted)
        else:
            self.set_result(decrypted)
            self.key_label.config(text=f"🔑 Найденный ключ: {key}")
            self.key_entry.delete(0, END)
            self.key_entry.insert(0, key)


if __name__ == '__main__':
    root = Tk()
    app = VApp(root)
    root.mainloop()