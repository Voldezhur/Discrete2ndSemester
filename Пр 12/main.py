from cryptography.fernet import Fernet

inputFile = open("the-full-bee-movie-script.txt")
outputFile = open("output.txt", 'w')

inputString = inputFile.read()
inputFile.close()
text = ""

# Удаление пробелов, знаков препинания и чисел, перевод к нижнему регистру и запись в строку
for i in inputString:
    if i.isalpha():
        text += i.lower()

outputFile.write("Исходный текст:\n{}\n".format(text))
print("Исходный текст:\n{}\n".format(text))


# =========== Шифровка Fernet
key = Fernet.generate_key()
encoder = Fernet(key)  # Создаем член класса

cipheredText = encoder.encrypt(text.encode())  # Шифруем

outputFile.write("\nЗашифрованный текст:\n{}\n".format(cipheredText))
print("\nЗашифрованный текст:\n{}\n".format(cipheredText))

decipheredText = encoder.decrypt(cipheredText).decode()  # Расшифровываем

outputFile.write("\nРасшифрованный текст:\n{}\n".format(decipheredText))
print("\nРасшифрованный текст:\n{}\n".format(decipheredText))
# ===========


outputFile.close()
