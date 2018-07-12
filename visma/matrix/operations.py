from visma.functions.operator import Plus
from visma.simplify.simplify import simplify
from visma.matrix.structure import Matrix


def simplifyMatrix(mat):
    for i in range(mat.dim[0]):
        for j in range(mat.dim[1]):
            mat.value[i][j], _, _, _, _ = simplify(mat.value[i][j])
    return mat


def addMatrix(matA, matB):
    matSum = Matrix()
    matSum.empty(matA.dim)
    for i in range(matA.dim[0]):
        for j in range(matA.dim[1]):
            matSum.value[i][j].extend(matA.value[i][j])
            matSum.value[i][j].extend([Plus()])
            matSum.value[i][j].extend(matB.value[i][j])
    matSum = simplifyMatrix(matSum)
    return matSum


def multiplyMatrix(matA, matB):
    matPro = Matrix()
    matPro.empty([matA.dim[0], matB.dim[1]])
