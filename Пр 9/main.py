# Генератор псевдослучайных чисел фон Неймана
# Сид умножается сам на себя
# Из центра этого числа берется слайс

key = 195183147123

fonNeymanSeed = [key]  # Сид для генератора (длина: 12 чисел)
# Сид в списке, т.к. список mutable тип данных => можно изменять из функции
def fonNeyman(x):
    B = str(fonNeymanSeed[0]*fonNeymanSeed[0])

    num = B[4:x+4]  # Берем число из центра

    # Проверка, чтобы число, более чем двузначное, не начиалось на 0
    # Если число начинается на 0, заменить 0 на 1
    if len(num) > 1:
        if num[0] == '0':
            num = '1' + num[1:]

    # Генерация нового сида
    newSeed = B[4:11]
    if newSeed[0] == '0':
        newSeed = '1' + newSeed[1:]

    # Запись нового сида во внешний массив - для сохранения значения до следующего вызова функции
    fonNeymanSeed[0] = int(newSeed)

    return num


inputFile = open("input.txt")
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

# Проход по тексту и шифровка блоками по 8
cipheredText = ""
currentIndex = 1
gamma = fonNeyman(8)

print("Блоки гаммы:")
outputFile.write("\nБлоки Гаммы:")
for i in text:
    if currentIndex % 8 == 0:  # Если прошли по блоку, берем следующую гамму шифра
        print(gamma)
        outputFile.write('\n' + gamma)
        gamma = fonNeyman(8)

    cipheredText += chr(ord(i) + int(gamma[currentIndex % 8 - 1]))
    currentIndex += 1

print("\nЗашифрованный текст: \n{}\n".format(cipheredText))
outputFile.write("\n\nЗашифрованный текст: \n{}\n".format(cipheredText))

# Расшифровка
decipheredText = ""
currentIndex = 1
fonNeymanSeed = [key]  # Придаем сиду изначальное значение
gamma = fonNeyman(8)

for i in cipheredText:
    if currentIndex % 8 == 0:  # Если прошли по блоку, берем следующую гамму шифра
        print(gamma)
        gamma = fonNeyman(8)

    decipheredText += chr(ord(i) - int(gamma[currentIndex % 8 - 1]))
    currentIndex += 1

print("\nРасшифрованный текст: \n{}\n".format(decipheredText))
outputFile.write("\nРасшифрованный текст: \n{}\n".format(decipheredText))


outputFile.close()
