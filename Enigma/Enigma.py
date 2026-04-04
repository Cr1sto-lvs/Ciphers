class EnigmaMachine:
      def __init__(self):
          # Три простых ротора с фиксированными внутренними соединениями
          self.rotors = [
              {chr(i+ord('A')): chr((i+3)%26+ord('A')) for i in range(26)},    # Первый ротор
              {chr(i+ord('A')): chr((i+5)%26+ord('A')) for i in range(26)},    # Второй ротор
              {chr(i+ord('A')): chr((i+7)%26+ord('A')) for i in range(26)}     # Третий ротор
          ]
          
          # Начальные позиции роторов
          self.positions = ['A', 'B', 'C']    # Изначально установлены в позиции A-B-C
      
      def rotate_rotor(self, rotor_num):
          """Изменяет положение ротора"""
          current_position = ord(self.positions[rotor_num]) - ord('A')
          new_position = (current_position + 1) % 26
          self.positions[rotor_num] = chr(new_position + ord('A'))
      
      def reflector(self, letter):
          """Отражатель - простая замена символов зеркально"""
          return chr(ord('Z') - (ord(letter) - ord('A')))
      
      def process_char(self, char, mode='encrypt'):
          """
          Метод для обработки одной буквы в зависимости от режима ('encrypt' или 'decrypt')
          """
          if not char.isalpha():
              return char
          
          input_char = char.upper()
          result = input_char
          
          # Сохраняем начальные позиции роторов
          initial_positions = [ord(pos) - ord('A') for pos in self.positions]
          
          # 1. Проходим через роторы вперед
          for idx, rotor in enumerate(self.rotors):
              shifted_input = chr((ord(result) - ord('A') + initial_positions[idx]) % 26 + ord('A'))
              result = rotor.get(shifted_input, shifted_input)
          
          # 2. Проходим через отражатель
          result = self.reflector(result)
          
          # 3. Обратный путь через роторы (для обоих режимов - шифрование и дешифрация)
          for idx, rotor in enumerate(reversed(self.rotors)):
              rev_map = {v:k for k,v in rotor.items()}
              reverse_shift = chr((ord(result) - ord('A') - initial_positions[len(self.rotors)-1-idx]) % 26 + ord('A'))
              result = rev_map.get(reverse_shift, reverse_shift)
          
          # Совмещаем результат с начальной позицией первого ротора
          final_result = chr((ord(result) - ord('A') + initial_positions[0]) % 26 + ord('A'))
          
          # Перемещение первого ротора
          self.rotate_rotor(0)
          if initial_positions[0] == 25:
              self.rotate_rotor(1)
          if initial_positions[1] == 25:
              self.rotate_rotor(2)
          
          return final_result
      
      def encrypt_message(self, message):
          encrypted_text = ''.join([self.process_char(c, mode='encrypt') for c in message])
          return encrypted_text
      
      def decrypt_message(self, cipher_text):
          decrypted_text = ''.join([self.process_char(c, mode='decrypt') for c in cipher_text])
          return decrypted_text


# Пример использования
if __name__ == "__main__":
      enigma = EnigmaMachine()
      plaintext = "HELLO WORLD"
      ciphertext = enigma.encrypt_message(plaintext)
      print(f'Исходный текст: {plaintext}')
      print(f'Зашифрованный текст: {ciphertext}')
      
      # Расшифровка сообщения
      decrypted_text = enigma.decrypt_message(ciphertext)
      print(f'Расшифрованный текст: {decrypted_text}')