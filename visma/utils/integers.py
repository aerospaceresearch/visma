def gcd(numbers):
    """Return the greatest common divisor for a given list of integers.

    Arguments:
        numbers {list} -- list of integers

    Returns:
        gcd {int} -- greatest common divisor
    """

    gcd = 1
    absValues = [abs(i) for i in numbers]
    smallest = min(absValues)
    if numbers[0] >= 0:
        for i in range(smallest, 1, -1):
            if all(number % i == 0 for number in absValues) is True:
                gcd = i
                break
    else:
        for i in range(-smallest, -1):
            if all(number % i == 0 for number in absValues) is True:
                gcd = i
                break
    return gcd


def factors(number):
    """Return the factors list for given number.

    Arguments:
        number {int} -- an integer

    Returns:
        factors {list} -- list of numbers dividing the given number
    """

    factors = []
    for i in range(1, int(abs(number)**0.5) + 1):
        if number % i == 0:
            factors.extend([i, number // i])
    factors.sort()
    return factors
