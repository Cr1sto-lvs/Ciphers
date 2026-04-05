import sys
import os
import platform
import subprocess
import ctypes
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
        # palette = QPalette()
        # palette.setColor(QPalette.ColorRole.Window, QColor("#FAFAFA"))
        # self.setPalette(palette)
        
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
        font = QFont("Times New Roman", 14)
        self.setFont(font)
        
        # Цвета кнопок (адаптивные)
        open_file_button.setStyleSheet(self.button_style("light_blue"))
        clear_button.setStyleSheet(self.button_style("red"))
        encrypt_button.setStyleSheet(self.button_style("green"))
        decrypt_button.setStyleSheet(self.button_style("blue"))
        crack_button.setStyleSheet(self.button_style("orange"))
        
        # Соединяем кнопки с действиями
        open_file_button.clicked.connect(self.open_file)
        clear_button.clicked.connect(self.clear_all)
        clear_key_button.clicked.connect(self.clear_key)
        encrypt_button.clicked.connect(self.perform_encrypt)
        decrypt_button.clicked.connect(self.perform_decrypt)
        crack_button.clicked.connect(self.perform_crack)

    def apply_color_scheme(self):
        """
        Применяет адаптивную цветовую схему, реагирующую на системную тему.
        """
        # Базовые стили для светлой и тёмной темы
        light_stylesheet = """
            QWidget {
                background-color: #FAFAFA;
                color: black;
            }
            QPushButton {
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton#light_blue {
                background-color: #ADD8E6;
                color: white;
            }
            QPushButton#red {
                background-color: #FF6347;
                color: white;
            }
            QPushButton#green {
                background-color: #90EE90;
                color: white;
            }
            QPushButton#blue {
                background-color: #ADD8E6;
                color: white;
            }
            QPushButton#orange {
                background-color: #FFA500;
                color: white;
            }
        """
        
        dark_stylesheet = """
            QWidget {
                background-color: #333333;
                color: white;
            }
            QPushButton {
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton#light_blue {
                background-color: #555555;
                color: white;
            }
            QPushButton#red {
                background-color: #AA4444;
                color: white;
            }
            QPushButton#green {
                background-color: #44AA44;
                color: white;
            }
            QPushButton#blue {
                background-color: #555555;
                color: white;
            }
            QPushButton#orange {
                background-color: #AA8844;
                color: white;
            }
        """
        
        # Определяем текущую тему ОС (более надежный способ)
        dark_mode = self.detect_system_theme()
        
        # Применяем подходящий стиль
        if dark_mode:
            self.setStyleSheet(dark_stylesheet)
        else:
            self.setStyleSheet(light_stylesheet)
    
    def detect_system_theme(self):
        """
        Надежное определение текущей темы ОС.
        Работает на Windows, macOS и Linux.
        """
        # Попытка определить тему через среду исполнения
        # Этот способ более стабилен и не требует внешних API
        try:
            # Проверяем наличие специальной переменной окружения
            # QT_QPA_PLATFORMTHEME=darkfusion указывает на тёмную тему
            qt_theme = os.environ.get("QT_QPA_PLATFORMTHEME", "")
            if "dark" in qt_theme.lower():
                return True
            
            # Проверяем наличие других индикаторов тёмной темы
            gtk_theme = os.environ.get("GTK_THEME", "")
            if "dark" in gtk_theme.lower():
                return True
            
            # Для macOS проверяем специальную переменную
            apple_theme = os.environ.get("APPLE_INTERFACE_STYLE", "")
            if apple_theme.lower() == "dark":
                return True
            
            # Для Windows проверяем реестр (если доступно)
            try:
                import winreg
                key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
                value, regtype = winreg.QueryValueEx(key, "AppsUseLightTheme")
                return value == 0  # 0 означает тёмную тему
            except ImportError:
                pass  # Модуль winreg отсутствует (не Windows)
            except Exception:
                pass  # Ошибка при чтении реестра
            
            # Если ничего не подошло, считаем светлую тему
            return False
        
        except Exception:
            # Если возникли проблемы, возвращаем светлую тему по умолчанию
            return False
    
    def button_style(self, color_name):
        """
        Возвращает стиль кнопки в зависимости от выбранной темы.
        """
        stylesheet_id = {
            "light_blue": "QPushButton#light_blue",
            "red": "QPushButton#red",
            "green": "QPushButton#green",
            "blue": "QPushButton#blue",
            "orange": "QPushButton#orange"
        }
        
        return f"{stylesheet_id[color_name]}"
    
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

        self.result_text_edit.setPlainText(f"Восстановленный ключ: {recovered_key}\nРезультат расшифровки: {Vigenere(lang, text, recovered_key).decryption()}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = VigenereApp()
    window.show()
    sys.exit(app.exec())