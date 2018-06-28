def gcd(numbers):
    """Return the greatest common divisor for a given list of integers.

    >>> gcd([1])
    1
    >>> gcd([3, 6, 12, 24])
    3
    """
    gcd = 1
    absValues = [abs(i) for i in numbers]
    large = max(absValues)
    if numbers[0] >= 0:
        for i in range(large, 1, -1):
            if all(number % i == 0 for number in absValues) is True:
                gcd = i
                break
    else:
        for i in range(-large, -1):
            if all(number % i == 0 for number in absValues) is True:
                gcd = i
                break
    return gcd


def factors(number):
    """Return the factors list for given number.

    >>> factors(24)
    [1, 2, 3, 4, 6, 8, 12, 24]
    >>> factors(0.5)  # Invalid input
    []
    """
    factors = []
    for i in xrange(1, abs(int(number)) + 1):
        if number % i == 0:
            factors.append(i)
    return factors


if __name__ == "__main__":
    import doctest
    doctest.testmod()
