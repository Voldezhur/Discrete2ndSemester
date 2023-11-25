from random import getrandbits, randrange

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


prime1 = getPrime(512)
prime2 = getPrime(512)

print("Первое простое число:\n{}\n".format(prime1))
print("Второе простое число:\n{}\n".format(prime2))

print("Сложение:\n{}".format(prime1 + prime2))
print("Вычитание:\n{}".format(prime1 - prime2))
print("Умножение:\n{}".format(prime1 * prime2))
print("Деление:\n{}".format(prime1 / prime2))
print("Остаток от деления первого на второе:\n{}".format(prime1 % prime2))
print("Возведение первого числа в степень 3 по модулю 100:\n{}".format(pow(prime1, 3, 100)))

