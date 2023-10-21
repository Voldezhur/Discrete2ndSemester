import math

# Класс деревьев - необходим для работы алгоритма Хаффмана
class Node:
    def __init__(self, data, frequency):
        self.parent = None
        self.left = None
        self.right = None
        self.code = ''
        self.data = data
        self.frequency = frequency

    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print(self.data),
        if self.right:
            self.right.PrintTree()

    def insertLeft(self, node):
        self.left = node
        self.left.code = '0'
        self.left.parent = self

    def insertRight(self, node):
        self.right = node
        self.right.code = '1'
        self.right.parent = self

    def listify(self, nodesList, collectedCode):
        collectedCode += self.code

        if self.right is None and self.left is None:
            nodesList.append((self.data, collectedCode))

        if self.left:
            self.left.listify(nodesList, collectedCode)

        if self.right:
            self.right.listify(nodesList, collectedCode)


# Алгоритм Хаффмана
# Работает с расчетом на то, что все элементы входного списка - деревья Node
def huffman(inputList):
    if len(inputList) <= 1:
        return inputList

    # Комбинируем последние два символа в один и суммируем их вероятность
    a = inputList[-1]
    b = inputList[-2]

    symbolCombination = Node(a.data + b.data, a.frequency + b.frequency)  # Создание комбинации из двух последних элементов

    # Вставка старых элементов слева и справа от комбинации
    symbolCombination.insertLeft(a)
    symbolCombination.insertRight(b)

    # Создание нового массива, с заменой последних двух элементов на новую комбинацию + сортировка
    newList = inputList[:len(inputList)-2]
    newList.append(symbolCombination)
    newList.sort(key=lambda x: x.frequency, reverse=True)
    return huffman(newList)


outputFile = open('output.txt', mode='w')
inputFile = open("input.txt")
inputString = inputFile.read()
text = ""

# Удаление пробелов и знаков препинания, перевод к нижнему регистру и запись в строку
for i in inputString:
    if i.isalpha():
        text += i.lower()

inputFile.close()


# -------------------- Однобуквенные --------------------

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

outputFile.write("Энтропия однобуквенных сочетаний: {}".format(oneLetterEntropy))
print("\nЭнтропия однобуквенных сочетаний:", oneLetterEntropy, sep='\n')

oneLetterTree = []  # Список деревьев для работы алгоритма Хаффмана

# Переделываем список в список деревьев
for i in range(len(oneLetter)):
    oneLetterTree.append(Node(oneLetter[i][0], oneLetter[i][1]))


codesTree = huffman(oneLetterTree)  # Дерево кодов
codesDict = []  # Список, в который будут записываться коды
collectedCode = ''  # Служебная переменная, для работы функции
codesTree[0].listify(codesDict, collectedCode)  # Функция переводит дерево в юзабельный список, но надо отсортировать
codesDict.sort(key=lambda x: len(x[1]))  # Сортировка списка кодов по длине кода
codesDict = dict(codesDict)  # переделываем список кодов в словарь, чтобы потом было проще искать код по букве


# Средняя длина элементарного кода
medianLength = 0
codesList = [(k, v) for k, v in codesDict.items()]  # Создаем список из словаря кодоа, чтобы было удобнее пройти по всем элементам

for i in range(len(oneLetter)):
    medianLength += len(codesList[i][1]) * oneLetter[i][1]  # Сумма длины кода, умноженного на вероятность буквы

outputFile.write("\nСредняя длина кода: {}".format(round(medianLength, 3)))
print("\nСредняя длина кода:", round(medianLength, 3))


# Эффективность сжатия
effectiveness = round((oneLetterEntropy / medianLength) * 100)
outputFile.write("\nЭффективность сжатия: {}%\n\n".format(effectiveness))
print("\nЭффективность сжатия: ", effectiveness, '%', sep='')


# Вывод кодов в файл
outputFile.write('---------- Таблица кодов ----------\n')
for i in oneLetter:
    outputFile.write('Буква: {}\t\tЧастота: {}\t\tКод: {}\n'.format(i[0], i[1], codesDict[i[0]]))

print(codesDict)


# Кодирование вводного текста, не считая пробелов, переносов строки и знаков препинания
outputString = text

# Заменяем символы на соответствующий код
for i in range(len(codesList)):
    outputString = outputString.replace(codesList[i][0], codesList[i][1] + ' ')

# for i in range(len(outputString)):
    # outputString[i] = [item[1] for item in lettersWithCodes if item[0] == outputString[i]]


# Вывод в файл
outputFile.write("\n\nИсходный текст:\n" + text)
outputFile.write("\n\nЗакодированный текст:\n" + outputString)


# Декодирование
code = ""  # Сюда будет записываться код
decodedString = ""  # Сюда будет записываться декодированная строчка
for i in outputString:
    code += i  # Добавляем в код следующую цифру, пока не дойдем до пробела

    if code[-1] == ' ':  # Дошли до пробела - можно декодировать
        decodedString += list(codesDict.keys())[list(codesDict.values()).index(code[:len(code) - 1])]  # Меняем на букву, которую нашли по коду в словаре
        code = ""  # Обнуляем код

# Вывод в файл
outputFile.write("\n\nДекодированный текст:\n" + decodedString)



# -------------------- Двубуквенные --------------------



outputFile.write("\n\n\n\n---------- Для двубуквенных ----------\n\n\n")

# Определяем вероятности
twoLetter = []

# Если в тексте нечетное кол-во символов, добавляем в конец случайный символ, чтобы работала программа
if len(outputString) % 2 == 1:
    outputString += 'a'

combinationList = []
# Идем подряд по двум буквам и добавляем в массив комбинации
for i in range(0, len(text) - 1):
    combination = str(text[i]) + str(text[i + 1])
    combinationList.append(combination)

combinationList = set(combinationList)  # Удаляем дубликаты комбинаций
combinationList = list(combinationList)

twoLetter = []
for i in combinationList:
    twoLetter.append((i, text.count(i) / (len(text) - 1)))

print(twoLetter)

twoLetter.sort(key=lambda x: x[1], reverse=True)  # Сортировка по второму члену кортежа
print("\nВероятности двубуквенных сочетаний:", twoLetter, sep='\n')

# Определяем энтропию
twoLetterEntropy = 0

for i in twoLetter:
    p = i[1]

    twoLetterEntropy += round(p * math.log2(p), 5)

twoLetterEntropy = -twoLetterEntropy

outputFile.write("\nЭнтропия двубуквенных сочетаний: {}".format(twoLetterEntropy))
print("\nЭнтропия двубуквенных сочетаний:", twoLetterEntropy, sep='\n')

twoLetterTree = []  # Список деревьев для работы алгоритма Хаффмана

# Переделываем список в список деревьев
for i in range(len(twoLetter)):
    twoLetterTree.append(Node(twoLetter[i][0], twoLetter[i][1]))

codesTree2 = huffman(twoLetterTree)  # Дерево кодов
codesDict2 = []  # Список, в который будут записываться коды
collectedCode = ''  # Служебная переменная, для работы функции (в нее записывается код по мере хода до листа)
codesTree2[0].listify(codesDict2, collectedCode)  # Функция переводит дерево в юзабельный список, но надо отсортировать
codesDict2.sort(key=lambda x: len(x[1]))  # Сортировка списка кодов по длине кода
codesDict2 = dict(codesDict2)  # переделываем список кодов в словарь, чтобы потом было проще искать код по букве

# Средняя длина элементарного кода
medianLength = 0
codesList2 = [(k, v) for k, v in codesDict2.items()]  # Создаем список из словаря кодоа, чтобы было удобнее пройти по всем элементам

for i in range(len(twoLetter)):
    medianLength += len(codesList2[i][1]) * twoLetter[i][1]  # Сумма длины кода, умноженного на вероятность буквы

outputFile.write("\nСредняя длина кода: {}".format(round(medianLength, 3)))
print("\nСредняя длина кода:", round(medianLength, 3))

# Эффективность сжатия
effectiveness = round((twoLetterEntropy / medianLength) * 100)
outputFile.write("\nЭффективность сжатия: {}%\n\n".format(effectiveness))
print("\nЭффективность сжатия: ", effectiveness, '%', sep='')

# Вывод кодов в файл
outputFile.write('---------- Таблица кодов ----------\n')
for i in twoLetter:
    outputFile.write('Буква: {}\t\tЧастота: {}\t\tКод: {}\n'.format(i[0], i[1], codesDict2[i[0]]))

print(codesDict2)


# Кодирование вводного текста, не считая пробелов, переносов строки и знаков препинания
outputString = ''

# Заменяем символы на соответствующий код и сразу выводим в файл
outputFile.write("\n\nИсходный текст:\n" + text)
outputFile.write("\n\nЗакодированный текст по двубуквенным:\n")

# Идем подряд по двум буквам и ищем эту комбинацию в словаре
for i in range(0, len(text) - 1, 2):
    combination = str(text[i]) + str(text[i + 1])
    code = codesDict2[combination] + ' '
    outputFile.write(code)
    outputString += code


# Декодирование
code = ""  # Сюда будет записываться код
decodedString = ""  # Сюда будет записываться декодированная строчка
for i in outputString:
    if i == ' ':  # Дошли до пробела - можно декодировать
        decodedString += list(codesDict2.keys())[list(codesDict2.values()).index(code)]  # Меняем на букву, которую нашли по коду в словаре
        code = ""  # Обнуляем код

    else:
        code += i  # Добавляем в код следующую цифру, пока не дойдем до пробела

# Вывод в файл
outputFile.write("\n\nДекодированный текст по двубуквенным:\n" + decodedString)
outputFile.close()


outputFile.close()
