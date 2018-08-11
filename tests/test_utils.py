from visma.utils.integers import gcd, factors
from visma.utils.polynomials import syntheticDivision

##################
# utils.integers #
##################


def test_gcd():
    assert gcd([1]) == 1
    assert gcd([3, 6, 12, 24]) == 3
    assert gcd([-2, 4, 8]) == -2
    assert gcd([2, -4, 8]) == 2


def test_factors():
    assert factors(24) == [1, 2, 3, 4, 6, 8, 12, 24]
    assert factors(0.5) == []  # Invalid input


#####################
# utils.polynomials #
#####################

def test_syntheticDivision():
    assert syntheticDivision([1, 2, 1], -1) == ([1.0, 1.0], 0.0)
    # (x^2 + 2x + 1)/(x+1)
    assert syntheticDivision([3, 2, 1, 3], 2) == ([3.0, 8.0, 17.0], 37.0)
    # (3x^2 + 2x + x + 3)/(x-2)
