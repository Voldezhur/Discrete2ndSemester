# ВАЖНО - в входном файле используются все буквы алфавита
inputFile = open("the-full-bee-movie-script.txt")
freqFile = open("frequencies2.txt")
outputFile = open("output.txt", "w+")

# Получаем информацию о частоте букв из файла
alphaFreq = [x.lower().split(' ') for x in freqFile.readlines()]

freqFile.close()

# Переделываем частоты букв из строк в числа,
# Делим на 100, чтобы переделать из процентов в дроби,
# Округляем до трех знаков после запятой
for i in range(len(alphaFreq)):
    alphaFreq[i][1] = round(float(alphaFreq[i][1][:-1]) / 100, 3)

print(alphaFreq)

outputFile.write("Частота букв в английском алфавите:")
for i in alphaFreq:
    outputFile.write("\n{}\t-\t{}".format(i[0], i[1]))

inputString = inputFile.read()
inputFile.close()
text = ""

# Удаление пробелов, знаков препинания и чисел, перевод к нижнему регистру и запись в строку
for i in inputString:
    if i.isalpha():
        text += i.lower()

outputFile.write("\n\nИсходный текст:\n{}".format(text))

alpha = []

# Создаем алфавит
for i in text:
    if i not in alpha:
        alpha.append(i)

# -------- Цезарь
cipherKey = 9
outputFile.write("\n\nКлюч для шифра цезаря: {}".format(cipherKey))

ceasarAlpha = list(alpha)
# Сдвигаем алфавит на ключ шифра
for i in range(len(ceasarAlpha)):
    ceasarAlpha[i] = chr(ord(ceasarAlpha[i]) + cipherKey)

# Создаем словарь для шифрования и дешифрования
ceasarDict = {alpha[i]: ceasarAlpha[i] for i in range(len(alpha))}
ceasarDecipherDict = {ceasarAlpha[i]: alpha[i] for i in range(len(alpha))}

print("Получившийся словарь:\n{}".format(ceasarDict))
outputFile.write("\n\nПолучившийся словарь:")
for i in ceasarDict:
    outputFile.write("\n{}\t-\t{}".format(i, ceasarDict[i]))

# Шифрование
cipheredText = ""
for i in text:
    cipheredText += ceasarDict[i]

print("\nТекст, зашифрованный шифром Цезаря:\n{}".format(cipheredText))

cipheredFreq = []

for i in cipheredText:
    hasNotBeenChecked = True

    for j in cipheredFreq:
        if j[0] == i:
            hasNotBeenChecked = False  # Если буква уже рассматривалась, дальше не проверяем

    if hasNotBeenChecked:  # Если не рассматривалась, записываем в список
        numOfApp = cipheredText.count(i)
        cipheredFreq.append((i, round(numOfApp / len(cipheredText), 3)))

cipheredFreq.sort(key=lambda x: x[1], reverse=True)  # Сортировка по второму члену кортежа

print(cipheredFreq)

# Дешифровка по вероятностям
# Берем самую часто встречающуюся букву и сопоставляем
key = ord(cipheredFreq[0][0]) - ord(alphaFreq[0][0])
print("Полученный ключ:", key)
outputFile.write("\n\nПолученный ключ: {}".format(key))

decipheredText = ""

for i in cipheredText:
    decipheredText += chr(ord(i) - key)

print("\nРасшифрованный текст: {}".format(decipheredText))
outputFile.write("\n\nРасшифрованный текст: {}".format(decipheredText))


outputFile.close()
