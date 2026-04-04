from collections import Counter

# Русский алфавит
RU_ALFABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
# Английский алфавит
ENG_ALFABET = "abcdefghijklmnopqrstuvwxyz"

# Частота встречи букв в текстах русского и английского языков
ruFreq = {'а': 8.01, 'б': 1.59, 'в': 4.54, 'г': 1.70, 'д': 2.98, 'е': 8.45, 'ё': 0.04, 'ж': 0.94, 'з': 1.65, 'и': 7.35,
          'й': 1.21, 'к': 3.49, 'л': 4.40, 'м': 3.21, 'н': 6.70, 'о': 10.97, 'п': 2.81, 'р': 4.73, 'с': 5.47,
          'т': 6.26, 'у': 2.62, 'ф': 0.26, 'х': 0.97, 'ц': 0.48, 'ч': 1.44, 'ш': 0.73, 'щ': 0.36, 'ъ': 0.04, 'ы': 1.90,
          'ь': 1.74, 'э': 0.32, 'ю': 0.64, 'я': 2.01}
enFreq = {'a': 8.17, 'b': 1.49, 'c': 2.78, 'd': 4.25, 'e': 12.70, 'f': 2.23, 'g': 2.02, 'h': 6.09, 'i': 6.97,
          'j': 0.15, 'k': 0.77, 'l': 4.03, 'm': 2.41, 'n': 6.75, 'o': 7.51, 'p': 1.93, 'q': 0.10, 'r': 5.99, 's': 6.33,
          't': 9.06, 'u': 2.76, 'v': 0.98, 'w': 2.36, 'x': 0.15, 'y': 1.97, 'z': 0.07}


class KAsiski:
    def split_text(message, N):
        # Разделение сообщения на N столбцов, далее это нам понадобиться для правильной рабоыт алгоритма дешифровки
        arr = []
        for i in range(N):
            arr.append(message[i:len(message):N])
        return arr


    def index_of_coincidence(message, alphabet):
        # Индекс совпадения для строки
        sum_ic = 0
        textLen = len(message)
        if textLen <= 1:
            return 0
        for letter in alphabet:
            count = message.count(letter)
            sum_ic += count * (count - 1)
        return sum_ic / (textLen * (textLen - 1))


    def find_key_length(message, alphabet, max_len=20):
        # Поиск длины ключа методом индекса совпадений
        message = KAsiski.format_text(message)
        best_len = 1
        best_ic = 0
        for L in range(1, min(max_len, len(message) // 2) + 1):
            columns = KAsiski.split_text(message, L)
            avg_ic = sum(KAsiski.index_of_coincidence(col, alphabet) for col in columns) / L
            if avg_ic > best_ic:
                best_ic = avg_ic
                best_len = L
        return best_len


    def decrypt_shift(text, shift, alphabet):
        # Расшифровка строки со сдвигом
        result = ""
        for ch in text:
            if ch in alphabet:
                idx = (alphabet.index(ch) - shift) % len(alphabet)
                result += alphabet[idx]
            else:
                result += ch
        return result


    def freq_squared(text, alphabet, freq):
        # Сравнивание частот
        counter = Counter(text)
        chi2 = 0
        for letter in alphabet:
            expected = freq.get(letter, 0) * len(text) / 100
            observed = counter.get(letter, 0)
            if expected > 0:
                chi2 += ((observed - expected) ** 2) / expected
        return chi2


    def find_shift(text, alphabet, freq):
        # Сдвиг для строки
        best_shift = 0
        best_chi2 = float('inf')
        for shift in range(len(alphabet)):
            decrypted = KAsiski.decrypt_shift(text, shift, alphabet)
            chi2 = KAsiski.freq_squared(decrypted, alphabet, freq)
            if chi2 < best_chi2:
                best_chi2 = chi2
                best_shift = shift
        return best_shift


    def crack_vigenere(ciphertext, alphabet, freq):
        # Взлом
        clean_text = KAsiski.format_text(ciphertext)
        if len(clean_text) < 20:
            return "", "Текст слишком короткий для взлома"

        # Длина ключа
        key_length = KAsiski.find_key_length(clean_text, alphabet)

        # Подбор сдвигов
        columns = KAsiski.split_text(clean_text, key_length)
        key = ""
        for column in columns:
            shift = KAsiski.find_shift(column, alphabet, freq)
            key += alphabet[shift]

        # Расшифровываем
        decrypted = KAsiski.decrypt_with_key(ciphertext, key, alphabet)
        return key, decrypted