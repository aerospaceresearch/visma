def syntheticDivision(coefficients, divisor):
    """Returns quotient and remainder  polynomial coefficients, given integer
    coefficients of polynomial
    """
    quotient = [float(coefficients[0])]
    for i in xrange(len(coefficients) - 1):
        quotient.append(quotient[-1] * divisor + coefficients[i + 1])
    remainder = quotient.pop()
    return quotient, remainder
