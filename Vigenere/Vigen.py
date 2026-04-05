class Vigenere:

    RU_ALFABET= "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    EN_ALFABET= "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Конструктор для задания алфавита
    def __init__(self, language, text, key):
        self.text = text
        self.key = key
        self.language = language
        if self.language == "RU":
            self.ALFABET= self.RU_ALFABET
        elif self.language == "EN":
            self.ALFABET= self.EN_ALFABET

    # Функция привода ключа к длине текста для зашифровки или расшифровки
    @staticmethod
    def key_to_enc(text, key, alph):
        i = 0
        # alph = self.ALFABET
        # key = self.key
        key_to_longtxt = ""
        for sumbol in text:
            if sumbol not in alph:
                key_to_longtxt += sumbol
                continue
            key_to_longtxt += key[i]
            i = (i + 1) % len(key)
        return key_to_longtxt, len(key_to_longtxt)
    

    # Функция шифрования текста(self - указатель с конструктора, the_text_to_enc - текст для шифровки, key - ключ)
    def encryption(self):
        the_txt_to_enc = self.text.upper()
        key = self.key.upper()
        # Создаём переменную, содержащая в себе алфавит для шифра
        ALFABET = self.ALFABET
        key_to_longtxt, len_enc = self.key_to_enc(the_txt_to_enc, key, ALFABET)
        enc_txt = ""
        # Перебираем индексы слова для зашифровки
        print(key_to_longtxt)
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
    def decryption(self):
        enc_txt = self.text.upper()
        # enc_txt = Vigenere().clean_punc(enc_txt).replace(' ', '')
        key = self.key.upper()
        ALFABET = self.ALFABET
        key_to_longtxt, len_enc = self.key_to_enc(enc_txt, key, ALFABET)
        decryrt_txt = ""
        for i in range(len_enc):
            if enc_txt[i] in ALFABET:
                # Как и в функции шировки, используем специальный алгоритм: mj = cj - kj \mod {n}
                decryrt_txt += ALFABET[(ALFABET.index(enc_txt[i]) - ALFABET.index(key_to_longtxt[i])) % len(ALFABET)]
            else:
                decryrt_txt += enc_txt[i]
        return decryrt_txt

# user_text = input("Enter the text to encrypt: ").upper()
# key = input("Enter the key: ").upper()
# Lang = input('RU or EN: ')
# vibor = input('Enter what you wont to do: encrypt - 1 or decrypt - 2: ')
# # Задание алфавита, в будущем можно вводить с клавиатуры
# a = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
# ALFABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
# Vigenere = Vigenere(Lang, user_text, key)
# if vibor == '1':
#     # Создание зашифрованного текста
#     enc_txt = Vigenere.encryption()
#     print(f'Encrypted text: {enc_txt}')
# elif vibor == '2':
#     # Создание расшифрованного текста
#     dec_txt = Vigenere.decryption()
#     print(f'Decryption text: {dec_txt}')
# else:
#     print('This action cannot be performed')