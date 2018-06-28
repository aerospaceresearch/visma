def syntheticDivision(coefficients, divisor):
    """Returns quotient and remainder  polynomial coefficients, given integer
    coefficients of polynomial

    >>> syntheticDivision([1, 2, 1],-1)  # (x^2 + 2x + 2)/(x+1)
    ([1.0, 1.0], 0.0)
    >>> syntheticDivision([3, 2, 1, 3], 2)  # (3x^2 + 2x + x + 3)/(x-2)
    ([3.0, 8.0, 17.0], 37.0)
    """
    quotient = [float(coefficients[0])]
    for i in xrange(len(coefficients) - 1):
        quotient.append(quotient[-1] * divisor + coefficients[i + 1])
    remainder = quotient.pop()
    return quotient, remainder


if __name__ == "__main__":
    import doctest
    doctest.testmod()
