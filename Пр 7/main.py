inputFile = open("bigInput.txt")
outputFile = open("output.txt", "w+")

inputString = inputFile.read()
text = ""
alpha = []
referenceAlphabet = "a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z".split(',')
# Удаление пробелов, чисел и знаков препинания, перевод к нижнему регистру и запись в строку
for i in inputString:
    if i.isalpha():
        text += i.lower()

# Создаем алфавит
for i in text:
    if i not in alpha:
        alpha.append(i)

# Вывод строки в файл
outputFile.write("Исходный текст:\n{}".format(text))

alpha = sorted(alpha)

cipherKey = int(input("Введите ключ шифра Цезаря: "))
gronsfeldNums = input("Введите числовую последовательность для шифра Гронсфельда: ").split(',')

# -------- Цезарь
outputFile.write("\n\nКлюч для шифра цезаря: {}".format(cipherKey))

ceasarAlpha = list(alpha)
# Сдвигаем алфавит на ключ шифра
for i in range(cipherKey):
    ceasarAlpha.append(ceasarAlpha.pop(0))

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

outputFile.write("\n\nТекст, зашифрованный шифром Цезаря:\n{}".format(cipheredText))
print("\nТекст, зашифрованный шифром Цезаря:\n{}".format(cipheredText))

# Дешифрование
decipheredText = ""
for i in cipheredText:
    decipheredText += ceasarDecipherDict[i]

outputFile.write("\n\nРасшифрованный текст:\n{}".format(decipheredText))
print("\nРасшифрованный текст:\n{}".format(decipheredText))

# -------- Гронсфельд
gronsfeldKey = []

for i in range(len(text)):
    gronsfeldKey.append(int(gronsfeldNums[i % len(gronsfeldNums)]))

outputFile.write("\n\nКлюч для шифра Гронсфельда: {}".format(gronsfeldKey))

# Шифровка текста
cipheredText = ""

for i in range(len(text)):
    symbol = text[i]
    cipheredSymbol = referenceAlphabet[(referenceAlphabet.index(text[i]) + gronsfeldKey[i]) % len(referenceAlphabet)]
    cipheredText += cipheredSymbol

outputFile.write("\n\nТекст, зашифрованный шифром Гронсфельда:\n{}".format(cipheredText))
print("\nТекст, зашифрованный шифром Гронсфельда:\n{}".format(cipheredText))

# Дешифровка текста
decipheredText = ""

for i in range(len(cipheredText)):
    symbol = cipheredText[i]
    decipheredSymbol = referenceAlphabet[(referenceAlphabet.index(cipheredText[i]) - gronsfeldKey[i]) % len(referenceAlphabet)]
    decipheredText += decipheredSymbol

outputFile.write("\n\nРасшифрованный текст:\n{}".format(decipheredText))
print("\nРасшифрованный текст:\n{}".format(decipheredText))


outputFile.close()
