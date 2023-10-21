# Только для текстов без чисел

import itertools as it  # Для двубуквенных сочетаний
import math  # Для подсчета логарифмов

inputFile = open("input2.txt")
inputString = inputFile.read()
text = ""


# Удаление пробелов и знаков препинания, перевод к нижнему регистру и запись в строку
for i in inputString:
    if i.isalpha():
        text += i.lower()

inputFile.close()


# ---- Однобуквенные ----

# Подсчет вероятностей и запись в список кортежей
# Также округляем все числа до тысячных
oneLetter = []

for i in text:
    hasNotBeenChecked = True

    for j in oneLetter:
        if j[0] == i:
            hasNotBeenChecked = False  # Если буква уже рассматривалась, дальше не проверяем

    if hasNotBeenChecked:  # Если не рассматривалась, записываем в список
        numOfApp = text.count(i)
        oneLetter.append((i, round(numOfApp / len(text), 3)))


print(text)

oneLetter.sort(key=lambda x: x[1], reverse=True)  # Сортировка по второму члену кортежа
print("\nВероятности однобуквенных сочетаний:", oneLetter, sep='\n')


# Определяем энтропию
oneLetterEntropy = 0

for i in oneLetter:
    p = i[1]
    oneLetterEntropy += round(p * math.log2(p), 3)

oneLetterEntropy = -oneLetterEntropy

print("\nЭнтропия однобуквенных сочетаний:", oneLetterEntropy, sep='\n')
print("\nСредняя энтропия на букву:", oneLetterEntropy / len(oneLetter), sep='\n')

# Алфавитное кодирование по Шеннону-Фано
"""
Сделать кортеж с символами, второй элемент - это код
К коду рекурсивно добавлять 1 или 0, по Шеннону-Фано
В каждом шаге рекурсии массив с кортежами делится пополам
Для первой и второй половины отдельно применяется функция добавления в конец цифры
Выход из рекурсии если длина куска равна 1

Записывать коды в отдельный массив вместо второго элемента кортежа
"""

codes = []
for i in oneLetter:
    codes.append(("", i[1]))


"""
Кортеж из двух элементов - вероятности и коды;
брать коды, копировать и добавлять 1 или 0;
создавать новый массив кортежей с новыми кодами;
"""
def Shannon(symbols):  # Алгоритм Шеннона-Фано
    if len(symbols) <= 1:
        return symbols  # Если один элемент в части - выводим

    A = []
    B = []
    sumOfProb = 0  # Суммарная вероятность во всей части
    for i in symbols:
        sumOfProb += i[1]

    probCount = 0  # Суммарная вероятность первого куска
    i = 0  # Индекс добавляемого элемента

    # Идем по символам и складываем вероятности. Доходим до половины суммарной вероятности - делим в этом месте
    while probCount < sumOfProb / 2.4:
        probCount += symbols[i][1]
        A.append((symbols[i][0], symbols[i][1]))
        i += 1

    for j in range(i, len(symbols)):
        B.append((symbols[i][0], symbols[j][1]))

    # Костыль нумеро уно: удаляем последний элемент из первого массива добавляем его в начало второго
    # B.insert(0, A.pop())

    # К первой части добавляем нули, ко второй единицы
    firstHalf = []
    secondHalf = []

    for j in A:
        firstHalf.append((j[0] + '0', j[1]))
    for j in B:
        secondHalf.append((j[0] + '1', j[1]))

    # Обновляем массив
    codes = Shannon(firstHalf) + Shannon(secondHalf)

    return codes

def addNumber(symbols):  # Старая функция, просто делила пополам
    if len(symbols) <= 1:  # Если длина массива 1 или меньше - дошли до конца
        return symbols

    # Делим массив на две части
    A = symbols[:int(len(symbols)/2)]
    B = symbols[int(len(symbols)/2):]

    # К первой части добавляем нули, ко второй единицы
    for i in range(len(A)):
        A[i] += '0'
    for i in range(len(B)):
        B[i] += '1'

    # Обновляем массив
    symbols = addNumber(A) + addNumber(B)

    return symbols


codes = Shannon(codes)  # Добавляем коды в массив
lettersWithCodes = []  # Список кортежей кодов с буквами

for i in range(len(codes)):
    lettersWithCodes.append((codes[i][0], oneLetter[i][0]))

print("\nСписок кодов:\n", lettersWithCodes, sep='')


# Кодирование вводного текста, не считая пробелов, переносов строки и знаков препинания
outputString = text

# Заменяем символы на соответствующий код
for i in range(len(lettersWithCodes)):
    outputString = outputString.replace(lettersWithCodes[i][1], lettersWithCodes[i][0] + ' ')

# for i in range(len(outputString)):
    # outputString[i] = [item[1] for item in lettersWithCodes if item[0] == outputString[i]]


# Вывод в файл
outputFile = open("output.txt", mode='w')
outputFile.write("Исходный текст:\n" + text)
outputFile.write("\n\n\nЗакодированный текст:\n" + outputString)


# Декодирование
# Переделываем список в словарь, чтобы проще было найти букву по коду
lettersWithCodes = dict(lettersWithCodes)

code = ""  # Сюда будет записываться код
decodedString = ""  # Сюда будет записываться декодированная строчка
for i in outputString:
    code += i  # Добавляем в код следующую цифру, пока не дойдем до пробела

    if code[-1] == ' ':  # Дошли до пробела - можно декодировать
        decodedString += lettersWithCodes[code[:len(code) - 1]]  # Меняем на букву, которую нашли по коду в словаре
        code = ""  # Обнуляем код

# Вывод в файл
outputFile.write("\n\nДекодированный текст:\n" + decodedString)


# Средняя длина элементарного кода
medianLength = 0

for i in range(len(oneLetter)):
    medianLength += len(codes[i][0]) * oneLetter[i][1]  # Сумма длины кода, умноженного на вероятность буквы

print("\nСредняя длина кода:", round(medianLength, 3))


# Эффективность сжатия
effectiveness = round((oneLetterEntropy / medianLength) * 100)
print("\nЭффективность сжатия: ", effectiveness, '%', sep='')


# -------- Двубуквенные --------
"""
взять все комбинации из однобуквенных
все двубуквенные комбинации, вероятность которых равна 0, не записывать
"""
print("\n\n---- Для двубуквенных ----")

# Определяем вероятности
twoLetter = []

# Если в тексте нечетное кол-во символов, добавляем в конец случайный символ, чтобы работала программа
if len(outputString) % 2 == 1:
    outputString += 'a'

# Идем подряд по двум буквам и добавляем в массив
for i in range(0, len(text) - 1, 2):
    combination = str(text[i]) + str(text[i + 1])
    twoLetter.append((combination, text.count(combination) / len(text)))

twoLetter = set(twoLetter)
twoLetter = list(twoLetter)

print(twoLetter)

twoLetter.sort(key=lambda x: x[1], reverse=True)  # Сортировка по второму члену кортежа
print("\nВероятности двубуквенных сочетаний:", twoLetter, sep='\n')

# Определяем энтропию
twoLetterEntropy = 0

for i in twoLetter:
    p = i[1]

    twoLetterEntropy += round(p * math.log2(p), 5)

twoLetterEntropy = -twoLetterEntropy

print("\nЭнтропия двубуквенных сочетаний:", twoLetterEntropy, sep='\n')
print("\nСредняя энтропия на сочетание:", twoLetterEntropy / len(twoLetter), sep='\n')

# Алфавитное кодирование
codes2 = []
for i in twoLetter:
    codes2.append(("", i[1]))

codes2 = Shannon(codes2)  # Добавляем коды в массив
twoLettersWithCodes = []  # Список кортежей кодов с двубуквенными сочетаниями
twoLettersWithCodes2 = []  # Второй список поменяем на словарь, чтобы было проще искать коды

for i in range(len(codes2)):
    twoLettersWithCodes.append((codes2[i][0], twoLetter[i][0]))
    twoLettersWithCodes2.append((twoLetter[i][0], codes2[i][0]))

print("\nСписок кодов:\n", twoLettersWithCodes, sep='')

twoLettersWithCodes2 = dict(twoLettersWithCodes2)  # Поменяли список на словарь для следующего шага

# Кодирование вводного текста, не считая пробелов, переносов строки и знаков препинания
outputString = ''

# Заменяем символы на соответствующий код и сразу выводим в файл
outputFile.write("\n\n\nЗакодированный текст по двубуквенным:\n")

# Идем подряд по двум буквам и ищем эту комбинацию в словаре
for i in range(0, len(text) - 1, 2):
    combination = str(text[i]) + str(text[i + 1])
    code = twoLettersWithCodes2[combination] + ' '
    outputFile.write(code)
    outputString += code


# Декодирование
# Переделываем список в словарь, чтобы проще было найти букву по коду
twoLettersWithCodes = dict(twoLettersWithCodes)

code = ""  # Сюда будет записываться код
decodedString = ""  # Сюда будет записываться декодированная строчка
for i in outputString:
    if i == ' ':  # Дошли до пробела - можно декодировать
        decodedString += twoLettersWithCodes[code]  # Меняем на букву, которую нашли по коду в словаре
        code = ""  # Обнуляем код

    else:
        code += i  # Добавляем в код следующую цифру, пока не дойдем до пробела

# Вывод в файл
outputFile.write("\n\nДекодированный текст по двубуквенным:\n" + decodedString)
outputFile.close()


# Средняя длина элементарного кода
medianLength = 0
twoLettersWithCodes = list(twoLettersWithCodes)
print(codes2)

for i in range(len(codes2) - 1):
    medianLength += len(codes2[i][0]) * codes2[i][1]  # Сумма длины кода, умноженного на вероятность буквы

print("\nСредняя длина кода:", round(medianLength, 3))


# Эффективность сжатия
effectiveness = round((twoLetterEntropy / medianLength) * 100)
print("\nЭффективность сжатия: ", effectiveness, '%', sep='')