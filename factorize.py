from multiprocessing import Process, Pool, cpu_count
from time import time


def find_numbers(number: int) -> list:
    result = []
    for num in range(1, number + 1):
        if number % num == 0:
            result.append(num)
    print(result)
    return result


def factorize(*args: int) -> list:
    timer = time()
    print('Синхронна версія')
    result = []
    for num in args:
        numbers = find_numbers(num)
        result.append(numbers)
    print(time() - timer)
    print('=======================================')

    print('Асинхронна версія')
    timer = time()
    with Pool(cpu_count()) as pool:
        result_pr = pool.map(find_numbers, args)
    print(time() - timer)
    # return result_pr
    return result


if __name__ == '__main__':
    a, b, c, d = factorize(128, 255, 99999, 10651060)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106,
                 1521580, 2130212, 2662765, 5325530, 10651060]
