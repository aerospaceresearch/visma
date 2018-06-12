def gcd(numbers):
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


def factors(x):
    factors = []
    for i in xrange(1, abs(int(x)) + 1):
        if x % i == 0:
            factors.append(i)
    return factors
