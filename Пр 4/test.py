import numpy as np

a = np.array([[1, 1, 0, 1, 1, 0, 0],
              [1, 0, 1, 1, 0, 1, 0],
              [0, 1, 1, 1, 0, 0, 1]])

b = np.array([0, 1, 0, 0, 1, 1, 1])

# a = np.array([[1, 1, 1], [0, 0, 1]])
# b = np.array([1, 0, 0])

print(a)
print(b, '\n')

mul = np.matmul(b, np.transpose(a))

print(np.transpose(a))
print(b, '\n')

for i in range(len(mul)):
    mul[i] = 1 if mul[i] > 0 else 0  # Числа больше одного делаем равными одному

print(mul)