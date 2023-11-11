from random import randint, randrange
import math


# НОД
def lcd(a, b):
    while a != 0 and b != 0:
        if a > b:
            a = a % b
        else:
            b = b % a

    return a + b


# Алгоритм Якоби
# https://literateprograms.org/jacobi_symbol__python_.html
def Jacobi(a, n):
    if a == 0:
        return 0
    if a == 1:
        return 1
    if a == 2:
        n8 = n % 8
        if n8 == 3 or n8 == 5:
            return -1
        else:
            return 1
    if a % 2 == 0:
        return Jacobi(2, n) * Jacobi(a // 2, n)
    if a >= n:
        return Jacobi(a % n, n)
    if a % 4 == 3 and n % 4 == 3:
        return -Jacobi(n, a)
    else:
        return Jacobi(n, a)


# Символ Лежандра
# https://gist.github.com/bnlucas/5857525
def legendre(a, p):
    if p < 2:
        raise ValueError('Число p должно быть < 2')
    if (a == 0) or (a == 1):
        return a
    if a % 2 == 0:
        r = legendre(a // 2, p)
        if p * p - 1 & 8 != 0:
            r *= -1
    else:
        r = legendre(p % a, a)
        if (a - 1) * (p - 1) & 4 != 0:
            r *= -1
    return r


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


# Соловей-Штрассен
# https://gist.github.com/bnlucas/5857525 (немного исправил)
def SolovayStrassen(num, repeat=10):
    if num == 2 or num == 3:
        return True
    if not num & 1:
        return False

    for i in range(repeat):
        a = randrange(2, num - 1)
        x = legendre(a, num)
        y = pow(a, (num - 1) // 2, num)

        if (x == 0) or (y != x % num):
            return False

    return True


# Тест Леманна
def Lehmann1(num, repeat=100):
    onesCount = 0

    for i in range(repeat):
        randomNumber = randint(1, num - 1)  # Выбираем случайное число

        j = pow(randomNumber, (num - 1) // 2) % num  # пункт 2
        if j == 1 or j == -1:
            return True

        else:
            return False

        if j == 1:
            onesCount += 1
        else:
            onesCount -= 1

    if onesCount < repeat:
        return True

# https://www.chegg.com/homework-help/questions-and-answers/implement-c-java-python-task-implement-lehman-s-algorithm-input-program-number-program-nee-q118355321
def Lehmann(n):
    """
    This function implements Lehman's primality test.

    Args:
        n: The number to be tested.

    Returns:
        True if n is prime, False otherwise.
    """

    if n == 2 or n == 3:
        return True

    # Check if n is even.
    if n % 2 == 0:
        return False

    # Generate a random integer a in the range [2, n-1].
    a = randint(2, n - 1)

    # Calculate x = a^((n-1)/2) mod n.
    x = pow(a, (n - 1) // 2, n)

    # If x is 1 or -1, then n is prime.
    if x == 1 or x == n - 1:
        return True

    # Otherwise, n is composite.
    return False


def rabin_miller(p, repeat=40):
    for i in range(repeat):

        num = p - 1  # 1
        b = 0
        while num > 0 and num % 2 == 0:
            b += 1
            num = num / 2

        m = (p - 1) / pow(2, b)

        a = randint(0, p)  # 2

        j = 0  # 3
        z = pow(a, m) % p
        if z == 1 or z == p - 1:  # 4
            return True

        def number5(num, j, z):
            if j > 0 and z == 1:  # 5
                return False

            j = j + 1  # 6
            if j < b and z != p - 1:
                z = pow(z, 2) % p

            else:
                if z == p - 1:
                    return True

                if z == b and z != p - 1:  # 7
                    return False

        if j > 0 and z == 1:  # 5
            return False

        j = j + 1  # 6
        if j < b and z != p - 1:
            z = pow(z, 2) % p
            return number5(p, j, z)

        else:
            if z == p - 1:
                return True

            if z == b and z != p - 1:  # 7
                return False


# https://gist.github.com/Ayrx/5884790
def miller_rabin(n, k=40):
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


# Факторизация Ферма
# https://github.com/mkazmier/fermat-factor/blob/master/fermat_factor.py
def factorise(n):
    x = math.ceil(math.sqrt(n))
    y = x ** 2 - n
    while not math.sqrt(y).is_integer():
        x += 1
        y = x ** 2 - n
    return x + math.sqrt(y), x - math.sqrt(y)


# Решето Эратосфена
print("Простые числа до 256 по решету эратосфена:\n{}\n".format(Eratosphen(256)))

# Массив для проверки на простоту
nums = [15, 28, 105, 4, 5]

# Проверка массива
for i in nums:
    print("Число {}:".format(i))

    if not SolovayStrassen(i):
        p, q = factorise(i)
        print(p, q)
    else:
        print("Число простое")

num = 4
print("\n\nПроверка числа {} на простоту по методу Соловея-Штрассена: {}".format(num, SolovayStrassen(num)))
print("Проверка числа {} на простоту по методу Рабина-Миллера: {}".format(num, Lehmann(num)))
print("Проверка числа {} на простоту по методу Рабина-Миллера: {}".format(num, miller_rabin(num)))
