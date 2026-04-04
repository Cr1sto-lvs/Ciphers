import string

class Vigenere:
    # Конструктор для задания алфавита
    def __init__(self, ALFABET, text, key):
        self.ALFABET = ALFABET
        self.text = text
        self.key = key

    # Функция привода ключа к длине текста для зашифровки или расшифровки
    @staticmethod #Декоратор, обозначающий функцию как статическую, нужно для  корректной работы кода без передачи класса как третьего аргумента
    def key_to_enc(key, len_enc = 0):
        i = 0
        key_to_longtxt = ""
        # Проверка условия, что длина ключа меньше чем сам текст для шифрования
        if len(key) > len_enc:
            key_to_longtxt = key[:len_enc]
        else:
            # Если условие не выполняется, то мы повторяем символы ключа, пока ключ не будет длины текста для шифровки или расшифровки
            while len(key_to_longtxt) < len_enc:
                key_to_longtxt += key[i]
                i = (i + 1) % len(key)
        return key_to_longtxt

    # Функция шифрования текста(self - указатель с конструктора, the_text_to_enc - текст для шифровки, key - ключ)
    def encryption(self):
        the_txt_to_enc = self.text.replace(' ', '')
        key = self.key
        len_enc = len(the_txt_to_enc)
        key_to_longtxt = Vigenere.key_to_enc(key, len_enc)
        # Создаём переменную, содержащая в себе алфавит для шифра
        ALFABET = self.ALFABET
        enc_txt = ""
        # Перебираем индексы слова для зашифровки
        for i in range(len_enc):
            # Проверка, есть ли символ для зашифровки в заданном алфавите
            if the_txt_to_enc[i] in ALFABET:
                # Если он есть, мы действуем по формуле cj= mj + kj \mod{n}, где cj - шифрованный символ, mj - исходный символ, kj - символ ключа с заданным индексом, n - длина алфавита
                enc_txt += ALFABET[(ALFABET.index(the_txt_to_enc[i]) + ALFABET.index(key_to_longtxt[i])) % len(ALFABET)]
            else:
                # Если его нет, то пропускаем
                enc_txt += the_txt_to_enc[i]
        return enc_txt

    # Функция расшифровки текста(self - указатель с конструктора, enc_txt - текст для расшифровки, key - ключ)
    def decrypion(self):
        len_enc = len(self.text)
        enc_txt = self.text.replace(' ', '')
        key = self.key
        key_to_longtxt = Vigenere.key_to_enc(key, len_enc)
        ALFABET = self.ALFABET
        decryrt_txt = ""
        for i in range(len_enc):
            if enc_txt[i] in ALFABET:
                # Как и в функции шировки, используем специальный алгоритм: mj = cj - kj \mod {n}
                decryrt_txt += ALFABET[(ALFABET.index(enc_txt[i]) - ALFABET.index(key_to_longtxt[i])) % len(ALFABET)]
            else:
                decryrt_txt += enc_txt[i]
        return decryrt_txt

user_text = input("Enter the text to encrypt: ").upper()
key = input("Enter the key: ").upper()
vibor = input('Enter what you wont to do: encrypt - 1 or decrypt - 2: ')
# Задание алфавита, в будущем можно вводить с клавиатуры
a = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
Vigenere = Vigenere(a, user_text, key)
if vibor == '1':
    # Создание зашифрованного текста
    enc_txt = Vigenere.encryption()
    print(f'Encrypted text: {enc_txt}')
elif vibor == '2':
    # Создание расшифрованного текста
    dec_txt = Vigenere.decryption()
    print(f'Decryption text: {dec_txt}')
else:
    print('This action cannot be performed')