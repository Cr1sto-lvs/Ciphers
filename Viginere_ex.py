from itertools import permutations

symbol = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
          'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def cryption(string, key):
    #string
    #string_index
    #key_index
    #array_key
    #conclusion

    stream_string = []# stream symbols of string
    for i in string:
        stream_string.append(symbol.index(i))


    key_index = [] # index symbols of key
    for i in key:
        key_index.append(symbol.index(i))


    stream_key = [] # stream of key's
    for i in range(len(string)):
        stream_key.append(key_index[i%len(key_index)])


    array_conc = []
    for i in range(len(stream_string)):
        array_conc.append((stream_string[i] + stream_key[i])%len(symbol))


    array_s = []
    for i in array_conc:
        array_s.append(symbol[i])
    res = ''.join(array_s)


    return res

def incryption(conc, key):

    stream_conc = []
    for i in conc:
        stream_conc.append(symbol.index(i))


    key_index = []
    for i in key:
        key_index.append(symbol.index(i))


    stream_key = []
    for i in range(len(conc)):
        stream_key.append(key_index[i % len(key_index)])


    array_conc = []
    for i in range(len(stream_conc)):
        array_conc.append((stream_conc[i] - stream_key[i]) % len(symbol))


    array_s = []
    for i in array_conc:
        array_s.append(symbol[i])
    res = ''.join(array_s)


    return res


def nod(arr): # принимает список int(расстояний) и возвращает список делителей
    if not arr:
        return []
    array_dell = []
    minvalue = min(arr)
    for dell in range(minvalue, 1, -1):
        flag = True
        for i in arr: # значения списка на входе
            if i % dell != 0: # ну делится ли
                flag = False
                break
        if flag == True:
            array_dell.append(dell)

    return array_dell

def split_groups(text, l): # Возвращает список строк: groups[i] = символы с индексами i, i+L, i+2L,
    groups = [''] * l
    for idx, ch in enumerate(text):
        groups[idx % l] += ch
    return groups

def find_shift(group):
    if not group:
        return 0

    freq = {}
    for char in group:
        freq[char] = freq.get(char, 0) + 1 # второй аргумент - значение по умолчанию, если char еще нет

    max_char = max(freq.items(), key=lambda item: item[1])[0] # lambda item: item[1] берет второй элемент, то есть частоту
    shift = (ord(max_char) - ord('e')) % 26 # вычисляем сдвиг относительно самой встречаемой буквы в англйиском - 'e'
    return shift

def english_score(text): # скорее всего текст, где больше всего встречаются частые буквы
    t = text.lower()
    return (t.count('e') + t.count('t') + t.count('a') + t.count('o') + t.count('i') + t.count('n'))


def incryption_sasiski(string):
    count_s = {} # кол-во повторений символов 3-6 длины
    indexx_s = {} # списки индексов
    for i in range(3, 7):
        word_i = 0
        while word_i <= len(string)-i:
            array_index = []
            word = string[word_i:word_i+i]

            if word not in count_s: # проверка на вхождение слова в словаре
                countt = 1
                i2 = 0
                while i2 <= len(string) - i:
                 # счет слов в строке
                    if string[i2:i2+i] == word:
                        array_index.append(i2) # тут же добавляем индексы слов
                        countt+=1
                    i2+=1
                if countt > 1:
                    count_s[word] = countt
                    indexx_s[word] = array_index
            word_i += 1 # дальше по индексу


    diff_s = {} # словарь с расстояниями между индексами слов(ключей)
    for i in indexx_s:
        arr_dif = []
        for ind_i in range(len(indexx_s[i])-1):
            arr_dif.append(indexx_s[i][ind_i+1] - indexx_s[i][ind_i])
        if arr_dif:
            diff_s[i] = arr_dif

    array_frequancy_dell = [0]*100 # возможные длины ключа, где индексы - длины, а значения - повторения
    for key_d in diff_s:
        arr = nod(diff_s[key_d])
        if arr: # список не пуст
            for i in arr:
                if i < len(array_frequancy_dell):
                    array_frequancy_dell[i] += 1
                else:
                    print('Длина ключа больше сотни, что не подходит к условию программы, так что игнорим')

    # может быть, что максимальная частота длин не одна, тогда чекаем все
    max_v = max(array_frequancy_dell) # максимум встречается
    if max_v == 0:
        print("Общих делителей не найдено. Возможно, текст слишком короткий или ключ длиннее 99.")

    # ar_max_lenght_key = []
    # for i in range(100):
    #     if array_frequancy_dell[i] == max_v:
    #         ar_max_lenght_key.append(i) # длина ключа
    #         print(f'Возможная длина ключа: {i}')
    #
    # if not ar_max_lenght_key:
    #     print("Нет кандидатов для анализа.")
    #     return

    threshold = max_v * 0.75
    ar_max_lenght_key = []
    for i in range(100):
        if array_frequancy_dell[i] >= threshold:
            ar_max_lenght_key.append(i)
            print(f'Возможная длина ключа: {i} (частота {array_frequancy_dell[i]})')

    if not ar_max_lenght_key:
        print("Нет кандидатов для анализа.")
        return

    best_score = -1
    best_key = ''
    best_plain = ''

    for L in ar_max_lenght_key:
        # Разбиваем на группы
        groups = split_groups(string, L)
        # Собираем ключ
        key_chars = []
        for g in groups:
            shift = find_shift(g)
            key_chars.append(chr(ord('a') + shift))
        key = ''.join(key_chars)

        # Расшифровываем
        plain = incryption(string, key)

        # Оцениваем качество
        score = english_score(plain)
        print(f'L={L:2d}, key="{key}", score={score}')

        if score > best_score:
            best_score = score
            best_key = key
            best_plain = plain

    print("\n✅ Наиболее вероятный результат:")
    print(f"   Длина ключа: {len(best_key)}")
    print(f"   Ключ: '{best_key}'")
    print("   Расшифрованный текст (начало 500 символов):")
    print(best_plain[:500])


# ord('a') == 97, ord('z') == 122
#ord('A') == 65, ord('Z') == 90
def action():
    choice = (input('Напишите: \n "1" - шифровка строки \n "2" - дешифровка \n "3" - взлом по Касиски \n\t:'))

    if choice != '1' and choice != '2' and choice != '3':
        print('Не подходящее число')
        return

    instring = input('Строка:').lower()
    if choice != '3' :
        inkey = input('Ключ:').lower()

    end_array = ''
    truestring = ''
    for i in instring:
        if i in symbol:
            truestring += i
    instring = truestring

    if choice == '1':
        end_array += f'{(cryption(instring, inkey))}'

    elif choice == '2':
        end_array += f'{(incryption(instring, inkey))}'

    elif choice == '3':
        end_array += f'{incryption_sasiski(instring)}'

    print(end_array)

    return end_array

i = '1'
while i!= '0' :
    action()
    i = (input('Если хотите закончить, введите: 0 '))
