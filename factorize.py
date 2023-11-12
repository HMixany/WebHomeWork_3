def factorize(*args):
    result = []
    for num in args:
        numbers = []
        for i in range(1, num+1):
            if num % i == 0:
                numbers.append(i)
        result.append(numbers)
    return result


if __name__ == '__main__':
    a, b, c, d = factorize(128, 255, 99999, 10651060)
    print(a)
    print(b)
    print(c)
    print(d)
