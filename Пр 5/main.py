from math import log2, ceil
from random import randint
import numpy as np

outputFile = open("output.txt", mode='w')


# Нахождение необходимых значений
k = 4  # Информационные разряды
r = ceil(log2((k + 1) + ceil(log2(k + 1))))  # Кодовые разряды
n = k + r  # Длина кода


# Начинаем создание вспомогательной таблицы
table = np.zeros((r + 1, n))

for i in range(1, n + 1):  # Запись в столбцы двоичных чисел от 1 до длины кода включительно
    binNum = bin(i)[2:][::-1]  # Переводим число в двоичную систему и переворачиваем - получается строка

    for j in range(len(binNum)):  # Записываем в столбец начиная со второй строчки
        table[j + 1][i - 1] = int(binNum[j])  # i - 1 чтобы заполнился первый столбик

outputFile.write('Вспомогательная таблица:\n{}'.format(str(table)))
print('Вспомогательная таблица:\n{}'.format(table))

a = []
for j in range(k):  # Строим случайную информационную комбинацию
    a.append(randint(0, 1))

outputFile.write('\n\nИнформационная комбинация:\n{}'.format(a))
print('\nИнформационная комбинация:\n{}'.format(a))


# Записываем информационную комбинацию в первую строку таблицы,
# не вписывая ничего в столбики, где только одна единица
for i in range(n):  # В первую строчку записываем -1 - это значит клетка пустая
    table[0][i] = -1

reversed_a = a[::-1]  # Переворачиваем a, чтобы можно было применять pop()

for i in range(n):
    if list(table[:, i]).count(1) > 1:
        table[0][i] = reversed_a.pop()

outputFile.write('\n\nВспомогательная таблица после добавления комбинации: (-1 значит пусто)\n{}'.format(str(table)))
print('\nВспомогательная таблица после добавления комбинации:\n{}'.format(table))


# Считаем проверочные биты
checkList = []  # Список проверочных битов, после нахождения всех, запишем в таблицу

for j in range(1, r + 1):  # Проходим по строкам, начиная со второй
    A = []  # список битов для подсчета логической операции

    for i in range(n):  # Проходим по столбцам и записываем в список только биты из столбцов, где в первой строчке пусто
        if table[0][i] != -1:
            A.append(int(table[j][i]))

    # Подсчет сложения по модулю 2 побитовой конъюнкции строки и инф, последовательности
    checkBit = None  # Проверочный бит
    for k in range(len(a)):
        checkBit = ((a[k] and A[k]) != checkBit) if checkBit is not None else (a[k] and A[k])

    checkList.append(1 if checkBit else 0)  # В список битов записываем 1 или 0, т.к. иначе писалось бы True или False

outputFile.write('\n\nПроверочные биты:\n{}'.format(checkList))
print('\nПроверочные биты:\n{}'.format(checkList))

reversed_checkList = checkList[::-1]  # Переворачиваем, чтобы можно было использовать pop()

for i in range(n):
    if table[0][i] == -1:
        table[0][i] = reversed_checkList.pop()

outputFile.write('\n\nВспомогательная таблица после добавления Проверочных битов:\n{}'.format(str(table)))
print('\nВспомогательная таблица после добавления проверочных битов:\n{}'.format(table))


# Закодированная последовательность == первая строка таблицы
beta = table[0, :]

outputFile.write('\n\n{} - Кодовая комбинация'.format(beta))
print('\n{} - Кодовая комбинация'.format(beta))


# Вносим ошибку в случайный разряд кода в комбинации и в таблице
randIndex = randint(0, n - 1)
beta[randIndex] = not beta[randIndex]

outputFile.write('\n\n{} - Кодовая комбинация с ошибкой'.format(beta))
print('\n{} - Кодовая комбинация с ошибкой'.format(beta))


# Считаем синдром
# Считаем сложение по модулю 2 побитовой конъюнкции строки с каждой строкой таблицы
syndrome = []  # Список проверочных битов, после нахождения всех, запишем в таблицу

for j in range(1, r + 1):  # Проходим по строкам, начиная со второй
    A = []  # Список битов для подсчета логической операции

    for i in range(n):  # Проходим по столбцам и записываем в список
        A.append(int(table[j][i]))

    # Подсчет сложения по модулю 2 побитовой конъюнкции строки и инф, последовательности
    fixBit = None  # Проверочный бит
    for k in range(len(beta)):
        fixBit = ((beta[k] and A[k]) != fixBit) if fixBit is not None else (beta[k] and A[k])

    syndrome.append(1 if fixBit else 0)  # В список битов записываем 1 или 0, т.к. иначе писалось бы True или False

outputFile.write('\n\nПроверочные биты:\n{}'.format(syndrome))
print('\nПроверочные биты:\n{}'.format(syndrome))


# Смотрим, на какой разряд указывает синдром
# Идем по столбцам проверочной матрицы и сравниваем с синдромом
errorIndex = 0
tableWithoutFirst = table[1:, :]

for i in range(n):
    column = tableWithoutFirst[:, i]
    if np.array_equal(column, syndrome):
        errorIndex = i
        break

outputFile.write('\n\nОшибка в {} разряде'.format(errorIndex + 1))
print('\nОшибка в {} разряде'.format(errorIndex + 1))


# Исправление ошибки
beta[errorIndex] = not beta[errorIndex]

outputFile.write('\n\n{} - Исправленная кодовая комбинация'.format(beta))
print('\n{} - Исправленная кодовая комбинация'.format(beta))


outputFile.close()
