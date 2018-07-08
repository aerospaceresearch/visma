from visma.matrix.checks import isMatrix, dimCheck, mulDimCheck
from visma.matrix.operations import simplifyMatrix
from tests.tester import getTokens

####################
# matrix.structure #
####################


def test_strMatrix():

    mat = getTokens("[1+x, 2; 3, 4]")
    assert mat.__str__() == "[{1.0}+{x},{2.0};{3.0},{4.0}]"


#################
# matrix.checks #
#################


def test_isMatrix():

    mat = getTokens("[1, 2, 3; x, z, 3]")
    assert isMatrix(mat)

    mat = getTokens("[1, 2; 1, 3; 1]")
    assert mat == []  # not a matrix


def test_dimCheck():

    matA = getTokens("[2, x; \
                       3, y]")
    matB = getTokens("[1, 2, x; \
                       2, 3, y]")
    assert not dimCheck(matA, matB)

    matA = getTokens("[2, x; 3, y]")
    matB = getTokens("[1, 2; 2, 3]")
    assert dimCheck(matA, matB)


def test_mulDimCheck():

    matA = getTokens("[1, 2; x, 2; 3, y]")
    matB = getTokens("[2, x; 3, y]")
    assert mulDimCheck(matA, matB)

    matA = getTokens("[2, x, 1; \
                       3, y, z]")
    matB = getTokens("[1, 2; 2, 3]")
    assert not mulDimCheck(matA, matB)


#####################
# matrix.operations #
#####################


def test_simplifyMatrix():

    mat = getTokens("[x + y + y, x^2 + x^2; \
                      1 + 4/2  , z^3/z^2  ]")
    matRes = simplifyMatrix(mat)
    assert matRes.__str__() == "[{x}+2{y},2{x}^{2.0};{3.0},{z}]"

    mat = getTokens("[1 + x^2 + 2]")
    matRes = simplifyMatrix(mat)
    assert matRes.__str__() == "[{3.0}+{x}^{2.0}]"
