from math import log2, ceil
from random import randint
import numpy as np

# Нахождение необходимых значений
k = 4  # Информационные разряды
r = ceil(log2((k + 1) + ceil(log2(k + 1))))  # Кодовые разряды
n = k + r  # Длина кода

# Начинаем создание проверочной матрицы
H = np.zeros((r, n))

for i in range(r):  # Создание единичной матрицы в конце проверочной
    H[i][i + n - r] = 1

# Запись в информационные столбцы случайных двоичных чисел
i = 0
added = []  # Список добавленных столбцов, чтобы не было повторений
while i < k:  # Количество шагов равно количеству информационных столбцов
    num = ''
    for j in range(r):  # Строим случайное число
        num += str(randint(0, 1))

    # Записываем число в столбец, только если оно уже не было добавлено
    # И если оно не равно нулю
    if not (num in added) and num.count('1') > 1:
        # Записываем число в столбец
        for x in range(r):
            H[x][i] = num[x]
        added.append(num)  # Записываем число в список добавленных
        i += 1

outputFile = open("output.txt", mode='w')

outputFile.write('Проверочная матрица:\n{}'.format(str(H)))
print('Проверочная матрица:\n{}'.format(H))


# Начинаем создание порождающей матрицы
G = np.zeros((k, n))

for i in range(k):  # Создание единичной матрицы в начале порождающей
    G[i][i] = 1

for x in range(k):  # Транспонирование проверочной матрицы и добавление ее в конец
    for y in range(r):
        G[x][y + k] = H[y][x]

outputFile.write('\n\nПорождающая матрица:\n{}'.format(str(G)))
print('\nПорождающая матрица:\n{}'.format(G))


# Кодирование
a = []
for j in range(k):  # Строим случайную информационную комбинацию
    a.append(randint(0, 1))

outputFile.write('\n\n{} - Информационная комбинация'.format(a))
print('\n{} - Информационная комбинация'.format(a))

beta = np.matmul(a, G)  # Умножаем комбинацию на порождающую матрицу
for i in range(len(beta)):
    beta[i] = 1 if beta[i] % 2 == 1 else 0  # Числа больше одного делаем равными одному

outputFile.write('\n\n{} - Кодовая комбинация'.format(beta))
print('\n{} - Кодовая комбинация'.format(beta))


# Вносим ошибку в случайный разряд кода
randIndex = randint(0, n - 1)
beta[randIndex] = not beta[randIndex]

outputFile.write('\n\n{} - Кодовая комбинация с ошибкой'.format(beta))
print('\n{} - Кодовая комбинация с ошибкой'.format(beta))

# Ищем синдром
syndrome = np.matmul(beta, np.transpose(H))
for i in range(len(syndrome)):
    syndrome[i] = 1 if syndrome[i] % 2 == 1 else 0  # Числа больше одного делаем равными одному

outputFile.write('\n\nСиндром: {}'.format(syndrome))
print('\nСиндром: {}'.format(syndrome))

# Смотрим, на какой разряд указывает синдром
# Идем по столбцам проверочной матрицы и сравниваем с синдромом
errorIndex = 0

for i in range(n):
    column = H[:, i]
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
