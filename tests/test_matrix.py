from visma.matrix.checks import isMatrix, dimCheck, multiplyCheck
from visma.matrix.operations import simplifyMatrix, addMatrix, scalarAdd, scalarSub, scalarMult, scalarDiv
from tests.tester import getTokens

####################
# matrix.structure #
####################


def test_strMatrix():

    mat = getTokens("[1+x, 2; \
                      3  , 4]")
    assert mat.__str__() == "[{1.0}+{x},{2.0};{3.0},{4.0}]"


#################
# matrix.checks #
#################


def test_isMatrix():

    mat = getTokens("[1, 2, 3; \
                      x, z, 3]")
    assert isMatrix(mat)

    mat = getTokens("[1, 2; \
                      1, 3; \
                      1]")
    assert mat == []  # not a matrix; returns empty matrix


def test_dimCheck():

    matA = getTokens("[2, x; \
                       3, y]")
    matB = getTokens("[1, 2, x; \
                       2, 3, y]")
    assert not dimCheck(matA, matB)

    matA = getTokens("[2, x; \
                       3, y]")
    matB = getTokens("[1, 2; \
                       2, 3]")
    assert dimCheck(matA, matB)


def test_multiplyCheck():

    matA = getTokens("[1, 2; \
                       x, 2; \
                       3, y]")
    matB = getTokens("[2, x; \
                       3, y]")
    assert multiplyCheck(matA, matB)

    matA = getTokens("[2, x, 1; \
                       3, y, z]")
    matB = getTokens("[1, 2; 2, 3]")
    assert not multiplyCheck(matA, matB)


#####################
# matrix.operations #
#####################


def test_simplifyMatrix():

    mat = getTokens("[x + y + x, x^2 + x^2; \
                      1 + 4/2  , z^3/z^2  ]")
    matRes = simplifyMatrix(mat)
    assert matRes.__str__() == "[2{x}+{y},2{x}^{2.0};{3.0},{z}]"

    mat = getTokens("[1 + x^2 + 2]")
    matRes = simplifyMatrix(mat)
    assert matRes.__str__() == "[{3.0}+{x}^{2.0}]"


def test_addMatrix():

    matA = getTokens("[2x + y, 2x]")
    matB = getTokens("[-x, -x]")
    matSum = addMatrix(matA, matB)
    # assert matSum.__str__() == "[2{x}+{y}]"  # BUG: Strange simplification for matSum

    matA = getTokens("[ x      , x^2; \
                        3 + x^2, xy ]")
    matB = getTokens("[ y + 1  , x^2; \
                        2 - x^2, xy - 1 ]")
    matSum = addMatrix(matA, matB)
    assert matSum.__str__() == "[{x}+{y}+{1.0},2{x}^{2.0};{5.0},2{x}{y}-{1.0}]"


def test_scalarAddMatrix():

    mat = getTokens("[1, 2; \
                    2,  1]")
    const = 2
    matSum = scalarAdd(const, mat)
    assert matSum.__str__() == "[{3.0},{2.0};{2.0},{3.0}]"

    mat = getTokens("[1, 2, 3;\
                        4, 5, 6;\
                        7, 8, 9]")
    const = 3
    matSum = scalarAdd(const, mat)
    assert matSum.__str__() == "[{4.0},{2.0},{3.0};{4.0},{8.0},{6.0};{7.0},{8.0},{12.0}]"


def test_scalarSubMatrix():

    mat = getTokens("[8,6;\
                      1,9]")
    const = 2
    matSub = scalarSub(const, mat)
    assert matSub.__str__() == "[{6.0},{6.0};{1.0},{7.0}]"

    mat = getTokens("[5,8,2;\
                      12,30,9;\
                      4,17,7]")
    const = 10
    matSub = scalarSub(const, mat)
    assert matSub.__str__() == "[{-5.0},{8.0},{2.0};{12.0},{20.0},{9.0};{4.0},{17.0},{-3.0}]"


def test_scalarMultMatrix():

    mat = getTokens("[1, 2]")
    const = 2
    matSum = scalarMult(const, mat)
    assert matSum.__str__() == "[{2.0},{4.0}]"

    mat = getTokens("[2,4;\
                      -5,7]")
    const = 2
    matSum = scalarMult(const, mat)
    assert matSum.__str__() == "[{4.0},{8.0};{-10.0},{14.0}]"


def test_scalarDivMatrix():

    mat = getTokens("[4, 2]")
    const = 2
    matSum = scalarDiv(const, mat)
    assert matSum.__str__() == "[{2.0},{1.0}]"

    mat = getTokens("[48,36;\
                      24,-3]")
    const = 6
    matSum = scalarDiv(const, mat)
    assert matSum.__str__() == "[{8.0},{6.0};{4.0},{-0.5}]"


def test_multiplyMatrix():
    """
    # FIXME: Fixing addition fixes multiplication
    matA = getTokens("[1, 0; 0, 1]")
    matB = getTokens("[2; 3]")
    matPro = multiplyMatrix(matA, matB)
    # assert matPro.__str__() == ""

    matA = getTokens("[1, 2; x, 2; 3, y]")
    matB = getTokens("[2, x; 3, y]")
    matPro = multiplyMatrix(matA, matB)
    # assert matPro.__str__() == ""

    matA = getTokens("[2, x, 1; \
                       3, y, z]")
    matB = getTokens("[1, 2; 2, 3; 5, 6]")
    matPro = multiplyMatrix(matA, matB)
    # assert matPro.__str__() == ""
    """
    pass
