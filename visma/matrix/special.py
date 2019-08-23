from visma.io.tokenize import tokenizer
from visma.matrix.structure import SquareMat


def cramerMatrices(coefficients):
    '''
    Arguments:
    coefficients -- 3 X 4 list -- each each row contains coefficients for x, y, z and constant term respectively

    Returns:
    Dx, Dy, Dz, D -- 3 X 4 list -- Cramer's Matrices for implementing Cramer's Rule.
    '''
    D = [[0] * 3 for _ in range(3)]
    Dx = [[0] * 3 for _ in range(3)]
    Dy = [[0] * 3 for _ in range(3)]
    Dz = [[0] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            D[i][j] = coefficients[i][j]
            Dx[i][j] = coefficients[i][j]
            Dy[i][j] = coefficients[i][j]
            Dz[i][j] = coefficients[i][j]
    for k in range(3):
        Dx[k][0] = coefficients[k][3]
        Dy[k][1] = coefficients[k][3]
        Dz[k][2] = coefficients[k][3]
    for i in range(3):
        for j in range(3):
            D[i][j] = tokenizer(str(D[i][j]))
            Dx[i][j] = tokenizer(str(Dx[i][j]))
            Dy[i][j] = tokenizer(str(Dy[i][j]))
            Dz[i][j] = tokenizer(str(Dz[i][j]))
    matD = SquareMat()
    matD.value = D
    matDx = SquareMat()
    matDx.value = Dx
    matDy = SquareMat()
    matDy.value = Dy
    matDz = SquareMat()
    matDz.value = Dz
    return matD, matDx, matDy, matDz
