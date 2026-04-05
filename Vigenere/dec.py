from collections import Counter
import math

class Kasiski:
    """Класс для криптоанализа методом Касиски-Керкхоффа."""
    
    # Стандартные алфавиты и частотные таблицы
    RU_ALFABET= "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    EN_ALFABET= "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    RU_FREQ = {
        'О': 11.0, 'Е': 8.5, 'А': 8.0, 'И': 7.5, 'Н': 7.0, 'Т': 6.5,
        'С': 5.5, 'Р': 4.5, 'В': 4.5, 'Л': 4.0, 'К': 3.5, 'М': 3.5,
        'Д': 3.0, 'П': 3.0, 'У': 3.0, 'Я': 2.5, 'Ы': 2.5, 'З': 2.0,
        'Ь': 2.0, 'Б': 2.0, 'Г': 2.0, 'Ч': 1.5, 'Й': 1.5, 'Ж': 1.0,
        'Ш': 1.0, 'Ю': 1.0, 'Ц': 1.0, 'Э': 1.0, 'Х': 1.0, 'Ф': 0.5,
        'Щ': 0.5, 'Ё': 0.5, 'Ъ': 0.5
    }
    
    EN_FREQ = {
        'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 6.7, 'N': 6.7,
        'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'U': 2.8,
        'C': 2.8, 'M': 2.4, 'W': 2.4, 'F': 2.2, 'Y': 2.0, 'G': 2.0,
        'P': 1.9, 'B': 1.5, 'V': 1.0, 'K': 0.8, 'J': 0.2, 'X': 0.2,
        'Q': 0.1, 'Z': 0.1
    }
    
    def __init__(self, message):
        """
        Инициализирует класс, автоматически определяя язык текста.
        Параметр message — зашифрованный текст.
        """
        self.message = message
        self.language = self.detect_language(message)
        
        if self.language == "RU":
            self.ALFABET= self.RU_ALFABET
            self.freq_table = self.RU_FREQ
        elif self.language == "EN":
            self.ALFABET= self.EN_ALFABET
            self.freq_table = self.EN_FREQ
    
    def detect_language(self, text):
        """
        Простой автоматический выбор языка по наличию русских букв.
        Возвращает "RU" или "EN".
        """
        for char in text:
            if char.upper() in self.RU_ALFABET:
                return "RU"
        return "EN"
    
    def normalize_text(self, text):
        """
        Приводит текст к единому регистру и оставляет только буквы.
        """
        text = text.upper()
        cleaned = "".join(char for char in text if char in self.ALFABET)
        return cleaned
    
    def split_into_columns(self, text, num_columns):
        """
        Разбивает текст на столбцы (каждый столбец — последовательность букв с фиксированным шагом).
        """
        columns = []
        for col_num in range(num_columns):
            column = text[col_num::num_columns]
            columns.append(column)
        return columns
    
    def calculate_ic(self, text):
        """
        Рассчитывает индекс совпадений для заданного фрагмента текста.
        """
        length = len(text)
        if length <= 1:
            return 0
        
        total = 0
        for letter in self.ALFABET:
            count = text.count(letter)
            total += (count * (count - 1)) / (length * (length - 1))
        return total
    
    def guess_key_length(self):
        """
        Оценивает длину ключа по индексу совпадений.
        Возвращает наиболее вероятную длину.
        """
        cleaned_text = self.normalize_text(self.message)
        scores = []
        
        for key_len in range(1, 10):  # Пробуем длины от 1 до 9
            columns = self.split_into_columns(cleaned_text, key_len)
            avg_ic = sum(map(self.calculate_ic, columns)) / len(columns)
            scores.append(avg_ic)
        
        best_length = scores.index(max(scores)) + 1
        return best_length
    
    def caesar_decrypt(self, text, shift):
        """
        Выполняет дешифровку Цезаря с заданным сдвигом.
        """
        decrypted = ""
        for char in text:
            if char not in self.ALFABET:
                decrypted += char
                continue
                
            index = self.ALFABET.index(char)
            new_index = (index - shift) % len(self.ALFABET)
            decrypted += self.ALFABET[new_index]
        return decrypted
    
    def calculate_diff(self, text):
        """
        Вычисляет разницу между наблюдаемой частотой букв и стандартной.
        Чем меньше разница — тем лучше подобран сдвиг.
        """
        counts = Counter(text)
        diff = 0
        
        for letter in self.ALFABET:
            observed_freq = counts.get(letter, 0) * 100 / len(text)
            standard_freq = self.freq_table.get(letter, 0)
            diff += abs(observed_freq - standard_freq)
        
        return diff
    
    def find_optimal_shift(self, text):
        """
        Поиск наилучшего сдвига путём минимизации отклонения частот.
        """
        shifts = [self.caesar_decrypt(text, shift) for shift in range(len(self.ALFABET))]
        diffs = [self.calculate_diff(shifted) for shifted in shifts]
        best_shift = diffs.index(min(diffs))
        return best_shift
    
    def remove_repeats(self, key):
        """
        Устраняет проблему повторяющихся частей ключа.
        Возвращает минимальное возможное слово.
        """
        key_length = len(key)
        
        # Проверяем, делится ли длина ключа нацело хотя бы на одно число
        for period in range(1, key_length // 2 + 1):
            if key_length % period != 0:
                continue
                
            # Проверяем, повторяется ли первая часть периода
            base_pattern = key[:period]
            repeated_pattern = base_pattern * (key_length // period)
            
            if repeated_pattern == key:
                return base_pattern
        
        return key  # Если не найдено повторений, возвращаем оригинальный ключ
    
    def recover_key(self):
        """
        Основной метод восстановления ключа.
        Возвращает восстановленную ключевую фразу.
        """
        cleaned_text = self.normalize_text(self.message)
        key_length = self.guess_key_length()
        columns = self.split_into_columns(cleaned_text, key_length)
        recovered_key = ""
        
        for column in columns:
            optimal_shift = self.find_optimal_shift(column)
            recovered_key += self.ALFABET[optimal_shift]
        
        # Новый этап: устранение повторяющихся частей ключа
        final_key = self.remove_repeats(recovered_key)
        return final_key



# # Пример использования:
# ciphertext = "GLBOZQICIR CVZYTRCOKHKK UVJ CBY CUVUKZ IV ZBM SILKLV CIZRX IXNQLCKOUT OHBKFTOAMTWM (GC) PGM JKWWSY WTY WL NPK GWYN XUQMXZCR UVJ NZGHALIZSUBOPM ZYKNHWRIOOYA UZ BNY 21AZ WMTNCXS. QZ CA XUXOXTE WPGHOOHO TYIXFG KPMXS IYJMIN WL BCSUV RCNK — ZZUG PKUTZBKGLM GHL KXCIUBOIV ZI JAMQTYAY, YVZYZZUQTGMTN, ITX BXUVYJWXNIZCWT. VCZ QPGN MDUKZFG OM IO, UVJ BWC CA ON ZKMPGJQTA WAL AUWQKNG? CBIZ CA GLBOZQICIR CVZYTRCOKHKK? UQ XYNKLA ZI BNY AOGCRUBOIV UZ PAGIT CVZYTRCOKHKK CV SUKNCVKM BNUB GLM VLWMLISGMJ NW ZBQTE, TKUZT, UVJ MWRPM VLWHFMSM. UUXMXH IO MGYNMSM IXY XXCUGLQRS JGMMJ IV SUKNCVK FMGLVOHO GHL JYMV HMALIR HMZQWXEA. ZBMYY AEMBKGA GHIRSHK GIYMQBY ISICTNA UZ LGNI, OXMTNQLS XGNBKLVY, UVJ WWTNQTOWAMTE CUVLWBY BNYQX JMXZWXGITWM CCBNICZ VMOHO KRXRCKONTE JZUAZGGUKX NUL MBYZE NIYE. IVJTOWIZCWTM WL UQ GWZUMA OHLAMBXCMY UQ OM IRLMGXG HYQTA CYYL OH VAGMXICY ZQKFLY QQZB QSJZKMAOPM XYAAFBY: BMGFBNWIXY: IO UTMIZONPSM KGH LKNMIN LOMMGMMY MCIB IY WITWMX ZZUG UKXQIUT OGIMYA CCBN UKIOZGWG XCDGFQTA WX YDKH AALXGMAOHO KRXKLQKHKKX LUWBULA. ZBME UTYI PKFX VLMJCKZ JIZCMTN WANKUGMY UVJ JMXMWTUTOTM ZLMGNUKHB VFITM. MJOKGNQUH: QTNMRFQMYVZ FMGLVOHO VFIZZWXGA GXIVN BU YIIB AZOLKHB’Y JIIY ITX TKUZTCVM MBEFM, VLWBCLOHO VYZYIVGFQFYL KRMXWQYYA GHL OHAZUVZ ZMKXJGWS. LCVGHKK: VITEA AMM GC BU XMZYKZ ZZGOLAFMTN BXUVYUKZCWTM QT LMGF BOGM, GMAKMA ILMJCB XCAQ, UVJ UCZIUGNM IIUVFMD CVBYAZGMTN AZLIZYOOYA. ZLITMXULBGNQUH: AKFN-JLQBCVM WIXM ITX ASUZZ NZGZNOW AEMBKGA VIEKLMJ VG GC XXIUOMM ZI ZKXCIY IIWQJYVZM, MGMM ZLILZQI WWTAMYNQUH, ITX ZKPWROBOIVOTM ALJGH UUVQRCBE. YBNCKGF KUHKKLVY UVJ LQYEA JYAVCBK CBY YVULUUOA VIBKHBOUT, ZBM XUXOX LKPMRIXSYVZ IN GC ZGCAKM AKLQUOA IIVIYZTM. WTY WL NPK VQMAMYN NKUZY CA SUAYCDK DWH XQYJTGWMSYVZ UA GOBUGIZCWT LMVFIIYA NOUGH EULSKLA OH DGLQUOA OHLAMBXCMY. NPKLM OM IRMW ZBM VLWHFMS IN GFOULQZBUOW JOUA — GC AEMBKGA IUV OHPKLQZ UVJ YDKH ISJTOZG VLMPOLOWMY JZKMMTN QT NPKCZ ZLIOHQTA LGNI, RYIJCVM NW AHNGCZ JYKOMQUHA. GHWZBMX GIPIZ OMAAY QY NPK JWZYVZCIR GQYOAK IN GC. LKYXLUSKM, IANWTIUUOA CYIVIVY, UVJ GIYM AALDKCTRUVIY IXY ZKUT ZBZKUBY NPGN KUOTJ XMYNIHCTOTM YIKOYBOYA OZ TKZB AHZKACRUBKX. UGHG KRXKLBY YUVBIYCHK NPK OZMYVZ HMKX NUL AZLWTA MZBQIUT LLISYEULSY UVJ CVZYZTUBOIVGF ZKACRUBOIVY NW KHAALM GC QY XMBYTUJMJ LMYJWTMQHFG. ZBM LOBALM UZ IO FWUEQTA INYIJ, MKOYVZCAZM XXYLOWB ZBIZ UQ CCTR VMIIUK YDKH UULM OHBKAZGNMJ CVZI WAL LGCTE FQBYA. ZBM AFBOGIZY OUUT LIZ SUVE LMYYIXWPKLA OM BNY KXYIZCWT IN GLBOZQICIR AMTYZGF QTNMRFQMYVIY (IMC) — AEMBKGA ZBIZ WIT JMXZWXG ITS QTNMRFMINCGF BGMS ZBIZ U PAGIT WIT XW, UL MBYV YOZVUAY BCSUV IUXGVQRCBOYA. ZBQY LIOMMY JZUZWAHL VBQRIAUJPOWIR KCKMBOIVY: WIT GIIBQTYA KPMX UKNCMBY BXOM IIVYWQUOATYAY? QPGN ZOAPZM ANICRX POAPRS IJPITWMJ UQ NUDK? BWC QQRF PAGITCBE WWKRQYN EONP KHBONQKM XUNMTNQGFTE GWXY QTNMRFQMYVZ NPGH WALAKFDKM? KUHKROAOIV GLBOZQICIR CVZYTRCOKHKK CA TYQZBMX CVNYZKHBRS OUIL TIZ HUL — ON QY U XUQMXZCR NWUF ENIAK CUVUKZ XMVYVJM MTNQXYTE IV NIE CY KNIWYY BU XMBYTUJ ITX CYY QZ. NW SUFOGQFY QZM JKHMLCBY QPOFM SCVOGQFCVM LQYEA, CY UAMB VLQULQZCHK LMYJWTMQHFM OHVUPIZCWT, NZGHAVUZKHKE, UVJ YBNCKGF OACLKFQTYA. ZBM LOBALM UZ IO QQRF JK XMICLKX JE NPK WPUCKKM EK GIQY BUXIE."
# analyzer = Kasiski(ciphertext)
# recovered_key = analyzer.recover_key()

# print("Вероятный ключ:", recovered_key)