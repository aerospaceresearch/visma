from visma.matrix.checks import isMatrix, dimCheck, mulDimCheck
from tests.tester import getTokens

#################
# matrix.checks #
#################


def test_isMatrix():

    mat = getTokens("[1, 2, 3; x, z, 3]")
    assert isMatrix(mat)

    mat = getTokens("[1, 2; 1, 3; 1]")
    assert mat == []  # not a matrix


def test_dimCheck():

    matA = getTokens("[2, x; 3, y]")
    matB = getTokens("[1, 2, x; 2, 3, y]")
    assert not dimCheck(matA, matB)

    matA = getTokens("[2, x; 3, y]")
    matB = getTokens("[1, 2; 2, 3]")
    assert dimCheck(matA, matB)


def test_mulDimCheck():

    matA = getTokens("[1, 2; x, 2; 3, y]")
    matB = getTokens("[2, x; 3, y]")
    assert mulDimCheck(matA, matB)

    matA = getTokens("[2, x, 1; 3, y, z]")
    matB = getTokens("[1, 2; 2, 3]")
    assert not mulDimCheck(matA, matB)
