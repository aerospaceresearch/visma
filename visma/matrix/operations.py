from visma.functions.operator import Binary
from visma.functions.structure import Expression
from visma.simplify.simplify import simplify
from visma.matrix.structure import Matrix


def simplifyMatrix(mat):
    """Simplifies each element in the matrix

    Arguments:
        mat {visma.matrix.structure.Matrix} -- matrix token

    Returns:
        mat {visma.matrix.structure.Matrix} -- simplified matrix token
    """
    for i in range(mat.dim[0]):
        for j in range(mat.dim[1]):
            mat.value[i][j], _, _, _, _ = simplify(mat.value[i][j])
    return mat


def addMatrix(matA, matB):
    """Adds two matrices

    Arguments:
        matA {visma.matrix.structure.Matrix} -- matrix token
        matB {visma.matrix.structure.Matrix} -- matrix token

    Returns:
        matSum {visma.matrix.structure.Matrix} -- sum matrix token

    Note:
        Make dimCheck before calling addMatrix
    """
    matSum = Matrix()
    matSum.empty(matA.dim)
    for i in range(matA.dim[0]):
        for j in range(matA.dim[1]):
            matSum.value[i][j].extend(matA.value[i][j])
            matSum.value[i][j].append(Binary('+'))
            matSum.value[i][j].extend(matB.value[i][j])
    matSum = simplifyMatrix(matSum)
    return matSum


def subtractMatrix(matA, matB):
    """Subtracts two matrices

    Arguments:
        matA {visma.matrix.structure.Matrix} -- matrix token
        matB {visma.matrix.structure.Matrix} -- matrix token

    Returns:
        matDifference {visma.matrix.structure.Matrix} -- difference matrix token

    Note:
        Make dimCheck before calling subtractMatrix
    """
    matDifference = Matrix()
    matDifference.empty(matA.dim)
    for i in range(matA.dim[0]):
        for j in range(matA.dim[1]):
            matDifference.value[i][j].extend(matA.value[i][j])
            matDifference.value[i][j].append(Binary('-'))
            matDifference.value[i][j].extend(matB.value[i][j])
    matDifference = simplifyMatrix(matDifference)
    return matDifference


def multiplyMatrix(matA, matB):
    """Multiplies two matrices

    Arguments:
        matA {visma.matrix.structure.Matrix} -- matrix token
        matB {visma.matrix.structure.Matrix} -- matrix token

    Returns:
        matPro {visma.matrix.structure.Matrix} -- product matrix token

    Note:
        Make mulitplyCheck before calling multiplyMatrix
        Not commutative
    """
    matPro = Matrix()
    matPro.empty([matA.dim[0], matB.dim[1]])
    for i in range(matA.dim[0]):
        for j in range(matB.dim[1]):
            for k in range(matA.dim[1]):
                if matPro.value[i][j] != []:
                    matPro.value[i][j].append(Binary('+'))
                if len(matA.value[i][k]) != 1:
                    matPro.value[i][j].append(Expression(matA.value[i][k]))
                else:
                    matPro.value[i][j].extend(matA.value[i][k])
                matPro.value[i][j].append(Binary('*'))
                if len(matB.value[k][j]) != 1:
                    matPro.value[i][j].append(Expression(matB.value[k][j]))
                else:
                    matPro.value[i][j].extend(matB.value[k][j])
    matPro = simplifyMatrix(matPro)
    return matPro
