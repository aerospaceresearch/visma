def syntheticDivision(coefficients, divisor):
    """Returns quotient and remainder polynomial coefficients, given integer coefficients of polynomial

    Arguments:
        coefficients {list} -- list of integer coefficients of poly
        divisor {int} -- divisor

    Returns:
        quotient {list} -- list of integer coefficients of quotient poly
        remainder {int} -- remainder

    Example:
        coefficients <-- [1, 2, 3] => (x^2 + 2x + 3)
        divisor <-- -1 => (x + 1)
        quotient --> [1, 1] => (x + 1)
        remainder --> 2
    """

    quotient = [float(coefficients[0])]
    for i in range(len(coefficients) - 1):
        quotient.append(quotient[-1] * divisor + coefficients[i + 1])
    remainder = quotient.pop()
    return quotient, remainder
