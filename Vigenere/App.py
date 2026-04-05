import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QFont, QPalette, QColor
from PyQt6.QtCore import Qt
from Vigen import Vigenere
from dec import Kasiski

# Импортируем необходимые функции шифрования/дешифрации/взлома
# (эти функции вы замените своими готовыми реализацией)
# from cipher_vigenere import encrypt, decrypt, crack_cipher

class VigenereApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    
    def init_ui(self):
        # Настройка внешнего вида
        self.setWindowTitle("Шифр Виженера")
        self.resize(800, 600)
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#FAFAFA"))
        self.setPalette(palette)
        
        # Определяем текущую тему ОС и применяем подходящую палитру
        self.apply_color_scheme()

        layout = QVBoxLayout(self)
        
        # Верхняя панель выбора языка (единый выбор для текста и ключа)
        language_group = QGroupBox("Язык (текст и ключ)")
        lang_layout = QVBoxLayout(language_group)
        self.lang_english_radio = QRadioButton("English")
        self.lang_russian_radio = QRadioButton("Русский")
        self.lang_english_radio.setChecked(True)  # Английский по умолчанию
        
        lang_layout.addWidget(self.lang_english_radio)
        lang_layout.addWidget(self.lang_russian_radio)
        layout.addWidget(language_group)
        
        # Блок загрузки файла и очистки
        file_buttons_widget = QWidget()
        file_buttons_layout = QHBoxLayout(file_buttons_widget)
        open_file_button = QPushButton("Открыть файл")
        clear_button = QPushButton("Очистить")
        file_buttons_layout.addWidget(open_file_button)
        file_buttons_layout.addWidget(clear_button)
        layout.addWidget(file_buttons_widget)
        
        # Поле ввода исходного текста
        source_label = QLabel("Исходный текст / Зашифрованный текст для взлома")
        self.source_text_edit = QPlainTextEdit()
        layout.addWidget(source_label)
        layout.addWidget(self.source_text_edit)
        
        # Поле ввода ключа
        key_label = QLabel("Ключ (для шифрования/расшифровки)")
        self.key_line_edit = QLineEdit()
        clear_key_button = QPushButton("Очистить")
        key_widget = QWidget()
        key_layout = QHBoxLayout(key_widget)
        key_layout.addWidget(self.key_line_edit)
        key_layout.addWidget(clear_key_button)
        layout.addWidget(key_label)
        layout.addWidget(key_widget)
        
        # Группа кнопок операций
        buttons_widget = QWidget()
        buttons_layout = QHBoxLayout(buttons_widget)
        encrypt_button = QPushButton("Зашифровать")
        decrypt_button = QPushButton("Расшифровать (с ключом)")
        crack_button = QPushButton("ВЗЛОМАТЬ (без ключа)")
        buttons_layout.addWidget(encrypt_button)
        buttons_layout.addWidget(decrypt_button)
        buttons_layout.addWidget(crack_button)
        layout.addWidget(buttons_widget)
        
        # Поле вывода результата
        result_label = QLabel("Результат")
        self.result_text_edit = QPlainTextEdit()
        layout.addWidget(result_label)
        layout.addWidget(self.result_text_edit)
        
        # Назначаем стили элементам
        font = QFont("Arial", 10)
        self.setFont(font)
        
        # Цвета кнопок
        open_file_button.setStyleSheet("background-color: #ADD8E6;")
        clear_button.setStyleSheet("background-color: #FF6347;")
        encrypt_button.setStyleSheet("background-color: #90EE90;")
        decrypt_button.setStyleSheet("background-color: #ADD8E6;")
        crack_button.setStyleSheet("background-color: #FFA500;")
        
        # Соединяем кнопки с действиями
        open_file_button.clicked.connect(self.open_file)
        clear_button.clicked.connect(self.clear_all)
        clear_key_button.clicked.connect(self.clear_key)
        encrypt_button.clicked.connect(self.perform_encrypt)
        decrypt_button.clicked.connect(self.perform_decrypt)
        crack_button.clicked.connect(self.perform_crack)

    def apply_color_scheme(self):
        '''Определяет текущую тему ОС и назначает подходящую палитру.'''
        # Определяем текущую тему ОС
        dark_mode = (self.style().standardPalette().color(QPalette.ColorRole.Window).lightness() < 128)
        
        # Создаём палитры для светлого и тёмного режимов
        light_palette = QPalette()
        light_palette.setColor(QPalette.ColorRole.Window, QColor("#FAFAFA"))  # Светлый фон
        light_palette.setColor(QPalette.ColorRole.WindowText, QColor("black"))  # Чёрный текст
        light_palette.setColor(QPalette.ColorRole.Base, QColor("#FFFFFF"))  # Белый фон текста
        light_palette.setColor(QPalette.ColorRole.Text, QColor("black"))  # Чёрный текст
        light_palette.setColor(QPalette.ColorRole.Button, QColor("#ADD8E6"))  # Голубая кнопка
        light_palette.setColor(QPalette.ColorRole.ButtonText, QColor("white"))  # Белый текст на кнопке
        
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.ColorRole.Window, QColor("#333333"))  # Тёмный фон
        dark_palette.setColor(QPalette.ColorRole.WindowText, QColor("white"))  # Белый текст
        dark_palette.setColor(QPalette.ColorRole.Base, QColor("#444444"))  # Тёмный фон текста
        dark_palette.setColor(QPalette.ColorRole.Text, QColor("white"))  # Белый текст
        dark_palette.setColor(QPalette.ColorRole.Button, QColor("#555555"))  # Серые кнопки
        dark_palette.setColor(QPalette.ColorRole.ButtonText, QColor("white"))  # Белый текст на кнопке
        
        # Применяем подходящую палитру
        if dark_mode:
            self.setPalette(dark_palette)
        else:
            self.setPalette(light_palette)
    
    def button_style(self, color_name):
        """
        Возвращает стиль кнопки в зависимости от выбранной темы.
        """
        if self.palette().color(QPalette.ColorRole.Window).lightness() < 128:
            # Темная тема
            background_color = "#555555"
            text_color = "white"
        else:
            # Светлая тема
            background_color = "#ADD8E6"
            text_color = "white"
        
        colors = {
            "light_blue": "#ADD8E6",
            "red": "#FF6347",
            "green": "#90EE90",
            "blue": "#ADD8E6",
            "orange": "#FFA500"
        }
        
        return f"background-color: {colors[color_name]}; color: {text_color};"
    
    def open_file(self):
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getOpenFileName(self,"Загрузить файл","","Text Files (*.txt);;All Files (*)")
        if filename:
            with open(filename, encoding="utf-8") as file:
                content = file.read()
                self.source_text_edit.setPlainText(content)
    
    def clear_all(self):
        self.source_text_edit.clear()
        self.result_text_edit.clear()
    
    def clear_key(self):
        self.key_line_edit.clear()
    
    def detect_language(self):
        """
        Вспомогательная функция для определения выбранного языка.
        Возвращает "RU" или "EN".
        """
        if self.lang_english_radio.isChecked():  # Первый радиоэлемент (Английский)
            return "EN"
        else:
            return "RU"
    
    # def vizhiner_text_processing(self):
    #     text = self.source_text_edit.toPlainText()
    #     key = self.key_line_edit.text()
        
    #     # Определяем единый язык для текста и ключа
    #     lang = self.detect_language()
    #     return Vigenere(lang, text, key)

    def perform_encrypt(self):
        text = self.source_text_edit.toPlainText()
        key = self.key_line_edit.text()
        
        # Определяем единый язык для текста и ключа
        lang = self.detect_language()
        Vigenere_cipher = Vigenere(lang, text, key)
        # Передаём язык в функцию шифрования
        encrypted_text = Vigenere_cipher.encryption()
        self.result_text_edit.setPlainText(encrypted_text)
    
    def perform_decrypt(self):
        text = self.source_text_edit.toPlainText()
        key = self.key_line_edit.text()
        
        # Определяем единый язык для текста и ключа
        lang = self.detect_language()
        Vigenere_cipher = Vigenere(lang, text, key)
        # Передаём язык в функцию расшифровки
        decrypted_text = Vigenere_cipher.decryption()
        self.result_text_edit.setPlainText(decrypted_text)
    
    def perform_crack(self):
        text = self.source_text_edit.toPlainText()
        analyzer = Kasiski(text)
        # Определяем единый язык для текста и ключа
        lang = self.detect_language()
        
        # Взлом производится только по языку текста
        recovered_key = analyzer.recover_key()

        self.result_text_edit.setPlainText(f"Восстановленный ключ: {recovered_key}\nРезультат расшифровки: {self.perform_decrypt()}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VigenereApp()
    window.show()
    sys.exit(app.exec())