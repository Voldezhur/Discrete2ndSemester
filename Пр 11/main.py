from random import getrandbits, randrange, randint
import math

# import sys
# sys.set_int_max_str_digits(150000)

# Проверяет все числа до upper не включительно
def Eratosphen(upper):
    nums = range(2, upper)
    prime = []

    for num in nums:
        flag = True  # Проверка, чтобы не было кратно простым числам

        for primeNum in prime:
            if num % primeNum == 0:
                flag = False
                break

        if flag:
            prime.append(num)

    return prime

def rabin_miller(n, k=40):
    # Implementation uses the Miller-Rabin Primality Test
    # The optimal number of rounds for this test is 40
    # See http://stackoverflow.com/questions/6325576/how-many-iterations-of-rabin-miller-should-i-use-for-cryptographic-safe-primes
    # for justification

    # If number is even, it's a composite number

    if n == 2 or n == 3:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


# Первые несколько простых чисел по решету Эратосфена
firstFewPrimes = Eratosphen(1000)

# Получаем число, которое не делится на первые несколько простых чисел
def getLowLevelPrime(n):
    while True:
        candidate = getrandbits(n)

        for i in firstFewPrimes:
            if candidate % i == 0 and i**2 <= candidate:
                break
            else:
                return candidate

def getPrime(n):
    while True:
        candidate = getLowLevelPrime(n)

        if not rabin_miller(candidate):
            continue
        else:
            return candidate


# inputFile = open("the-full-bee-movie-script.txt")
inputFile = open("smallInput.txt")
outputFile = open("output.txt", 'w')

inputString = inputFile.read()
inputFile.close()
text = ""

# Подготовка текста
# Удаление пробелов, знаков препинания и чисел, перевод к нижнему регистру и запись в строку
for i in inputString:
    if i.isalpha():
        text += i.lower()

outputFile.write("Исходный текст:\n{}\n".format(text))
print("Исходный текст:\n{}\n".format(text))

# Получение числа из текста:
# Перевод каждого числа в ASCII код, составление из этих кодов одного большого числа
textNums = []
for i in text:
    textNums.append(ord(i))


# Определение переменных
p = getPrime(512)
q = getPrime(512)

N = p * q

phi = (p - 1) * (q - 1)

# Генерация числа e
e = randint(2, phi - 1)
while math.gcd(phi, e) != 1:
    e = randint(2, phi - 1)

# Поиск числа d
d = pow(e, -1, phi)

# Создание ключей
publicKey = (N, e)
privateKey = (N, d)


outputFile.write("\np = {}\nq = {}\n".format(p, q))
print("p = {}, q = {}\n".format(p, q))

outputFile.write("\nN = {}\nphi = {}\n".format(N, phi))
print("N = {}, phi = {}\n".format(N, phi))

outputFile.write("\ne = {}\nd = {}\n".format(e, d))
print("e = {}\nd = {}\n".format(e, d))

outputFile.write("\nОткрытый ключ = (N, e) = {}\nЗакрытый ключ = (N, d) = {}\n".format(publicKey, privateKey))
print("Открытый ключ = (N, e) = {}\nЗакрытый ключ = (N, d) = {}\n".format(publicKey, privateKey))

outputFile.write("\nЧисла, полученные из текста: {}".format(textNums))
print("Числа, полученные из текста: {}".format(textNums))


# Шифрование - используем открытый ключ
cipher = []
for i in textNums:
    cipher.append(pow(i, e, N))

outputFile.write("\nЗашифрованные числа: {}".format(cipher))
print("Зашифрованные числа: {}".format(cipher))

# Расшифрование - используем закрытый ключ
deciphered = []
for i in cipher:
    deciphered.append(pow(i, d, N))

outputFile.write("\nРасшифрованные числа: {}".format(deciphered))
print("Расшифрованные числа: {}".format(deciphered))

# Перевод обратно в строку
decipheredText = ''
for i in deciphered:
    decipheredText += chr(i)

outputFile.write("\nРасшифрованный текст: {}".format(decipheredText))
print("Расшифрованный текст: {}".format(decipheredText))

outputFile.close()
