import random


# ***************************************************


def factorial(n):
    if n == 1:
        return 1
    return n * factorial(n - 1)


def print_hi(name):
    print(f'Hi, {name}')


if __name__ == '__main__':
    value = int(input('Introduzca valor \n'))
    print('El factorial de ' + str(value) + ' es -->' + str(factorial(value)))

    for i in range(0, 10):
        ran = random.randint(1, 10)
        print(ran)
