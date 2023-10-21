import math  # Для подсчета логарифмов и округлений вверх

inputFile = open("input.txt")
outputFile = open("output.txt", "w+")
inputString = inputFile.read()
text = ""


# Удаление пробелов и знаков препинания, перевод к нижнему регистру и запись в строку
for i in inputString:
    if i.isdigit() or i.isalpha():
        text += i.lower()

# Вывод строки в файл
outputFile.write(text)

inputFile.close()
outputFile.close()


# Подсчет вероятностей для однобуквенных комбинаций и запись в список кортежей
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


# Подсчет вероятностей для двубуквенных комбинаций
twoLetter = []

for i in text:
    if text.index(i) != len(text) - 1:  # Если i не последний элемент в строке
        hasNotBeenChecked = True

        secondLetter = text[text.index(i) + 1]  # Вторая буква в комбинации
        combination = i + secondLetter  # Вся двубуквенная комбинация

        for j in twoLetter:
            if j[0] == combination:
                hasNotBeenChecked = False  # Если комбинация уже рассматривалась, дальше не проверяем

        if hasNotBeenChecked:  # Если не рассматривалась, записываем в список
            numOfApp = text.count(combination)
            twoLetter.append((combination, round(numOfApp / (len(text) - 1), 3)))

twoLetter.sort(key=lambda x: x[1], reverse=True)  # Сортировка по второму члену кортежа
print("\nВероятности двубуквенных сочетаний:", twoLetter, sep='\n')


# Определяем энтропию
# Для однобуквенных сочетаний
oneLetterEntropy = 0

for i in oneLetter:
    p = i[1]
    oneLetterEntropy += round(p * math.log2(p), 5)

oneLetterEntropy = -oneLetterEntropy
print("\nЭнтропия однобуквенных сочетаний:", oneLetterEntropy, sep = '\n')

# Для двубуквенных сочетаний
twoLetterEntropy = 0

for i in twoLetter:
    p = i[1]
    twoLetterEntropy += round(p * math.log2(p), 5)

twoLetterEntropy = -twoLetterEntropy

print("\nЭнтропия двубуквенных сочетаний:", twoLetterEntropy, sep='\n')


# Длина кода при равномерном побуквенном кодировании и избыточность
# Для однобуквенных
m1 = len(oneLetter)  # Объем алфавита
oneLetterLength = math.log2(m1)  # Средняя длина кода символа
D1 = 1 - (-oneLetterEntropy / oneLetterLength)  # Избыточность

print("\nСредняя длина кода для однобуквенных комбинаций:", oneLetterLength)
print("Избыточность:", D1)

# Для двубуквенных
m2 = len(twoLetter)  # Объем алфавита
twoLetterLength = math.log2(m2)  # Средняя длина кода символа
D2 = 1 - (-twoLetterEntropy / twoLetterLength)  # Избыточность

print("\nСредняя длина кода для двубуквенных комбинаций:", twoLetterLength)
print("Избыточность:", D2)


# Удаление 20% самых частых символов
# Для однобуквенных
numLettersToDelete = math.ceil(len(oneLetter) * 0.2)  # Сколько требуется удалить символов: округляем вверх

i = numLettersToDelete - 1
lettersToDelete = []

# Находим, какие символы удалить
while i >= 0:
    lettersToDelete.append(oneLetter[i][0])
    i -= 1

# Удаляем из текста символы
text1 = text
for i in lettersToDelete:
    text1 = text1.replace(i, '')

print("\n\n-------- Удаление самых частых символов --------\n")
print("\nПосле удаления 20% самых частых символов:", text1, sep='\n')


# Расчитывание новых вероятностей - просто скопировано с предыдущего раза, только поменялись некоторые переменные
oneLetter1 = []

for i in text1:
    hasNotBeenChecked = True

    for j in oneLetter1:
        if j[0] == i:
            hasNotBeenChecked = False  # Если буква уже рассматривалась, дальше не проверяем

    if hasNotBeenChecked:  # Если не рассматривалась, записываем в список
        numOfApp = text.count(i)
        oneLetter1.append((i, round(numOfApp / len(text1), 3)))


oneLetter1.sort(key=lambda x: x[1], reverse=True)  # Сортировка по второму члену кортежа
print("\nВероятности однобуквенных сочетаний:", oneLetter1, sep='\n')

# Определяем энтропию
oneLetterEntropy = 0

for i in oneLetter:
    p = i[1]
    oneLetterEntropy += round(p * math.log2(p), 3)

oneLetterEntropy = -oneLetterEntropy

print("\nЭнтропия однобуквенных сочетаний:", oneLetterEntropy, sep='\n')


# Удаление 20% самых редких символов
# Для однобуквенных
numLettersToDelete = math.ceil(len(oneLetter) * 0.2)  # Сколько требуется удалить символов: округляем вверх

i = numLettersToDelete - 1
lettersToDelete = []

# Находим, какие символы удалить
while i >= 0:
    lettersToDelete.append(oneLetter.pop()[0])
    i -= 1

# Удаляем из текста символы
text2 = text
for i in lettersToDelete:
    text2 = text.replace(i, '')

print("\n\n-------- Удаление самых редких символов --------\n")
print("\nПосле удаления 20% самых редких символов:", text2, sep='\n')


# Расчитывание новых вероятностей
oneLetter2 = []

for i in text2:
    hasNotBeenChecked = True

    for j in oneLetter2:
        if j[0] == i:
            hasNotBeenChecked = False  # Если буква уже рассматривалась, дальше не проверяем

    if hasNotBeenChecked:  # Если не рассматривалась, записываем в список
        numOfApp = text.count(i)
        oneLetter2.append((i, round(numOfApp / len(text2), 3)))


oneLetter2.sort(key=lambda x: x[1], reverse=True)  # Сортировка по второму члену кортежа
print("\nВероятности однобуквенных сочетаний:", oneLetter2, sep='\n')

# Определяем энтропию
oneLetterEntropy = 0

for i in oneLetter:
    p = i[1]
    oneLetterEntropy += round(p * math.log2(p), 3)

oneLetterEntropy = -oneLetterEntropy

print("\nЭнтропия однобуквенных сочетаний:", oneLetterEntropy, sep='\n')