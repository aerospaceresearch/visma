from visma.functions.operator import Binary
from visma.functions.structure import Expression
from visma.functions.constant import Constant
from visma.simplify.simplify import simplify
from visma.matrix.structure import Matrix
from visma.gui import logger


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


def subMatrix(matA, matB):
    """Subtracts two matrices

    Arguments:
        matA {visma.matrix.structure.Matrix} -- matrix token
        matB {visma.matrix.structure.Matrix} -- matrix token

    Returns:
        matSub {visma.matrix.structure.Matrix} -- subtracted matrix token

    Note:
        Make dimCheck before calling subMatrix
    """
    matSub = Matrix()
    matSub.empty(matA.dim)
    for i in range(matA.dim[0]):
        for j in range(matA.dim[1]):
            matSub.value[i][j].extend(matA.value[i][j])
            matSub.value[i][j].append(Binary('-'))
            matSub.value[i][j].extend(matB.value[i][j])
    matSub = simplifyMatrix(matSub)
    return matSub


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


def scalarAdd(const, mat):
    """
    Adds constant terms with Matrix

    Arguments:
        const {string}--- constant value
        mat {visma.matrix.structure.Matrix} -- matrix token

    Returns:
        matRes {visma.matrix.structure.Matrix} -- sum matrix token

    Note:
        This scalar addition follows the following equation
            {mat} + {lambda}{identity mat}

    """
    matRes = Matrix()
    matRes.empty(mat.dim)
    for i in range(mat.dim[0]):
        for j in range(mat.dim[1]):
            if i != j:
                matRes.value[i][j].extend(mat.value[i][j])
            else:
                if len(mat.value[i][j]) != 1:
                    matRes.value[i][j].append(Expression(mat.value[i][j]))
                else:
                    matRes.value[i][j].extend(mat.value[i][j])
                matRes.value[i][j].append(Binary('+'))
                matRes.value[i][j].append(Constant(int(const)))
    matRes = simplifyMatrix(matRes)
    return matRes


def scalarSub(const, mat):
    """
    Subtracts constant terms with Matrix

    Arguments:
        const {string}--- constant value
        mat {visma.matrix.structure.Matrix} -- matrix token

    Returns:
        matRes {visma.matrix.structure.Matrix} -- subtracted matrix token

    Note:
        This scalar addition follows the following equation
            {mat} - {lambda}{identity mat}

    """
    matRes = Matrix()
    matRes.empty([mat.dim[0], mat.dim[1]])
    for i in range(mat.dim[0]):
        for j in range(mat.dim[1]):
            if i != j:
                matRes.value[i][j].extend(mat.value[i][j])
            else:
                if len(mat.value[i][j]) != 1:
                    matRes.value[i][j].append(Expression(mat.value[i][j]))
                else:
                    matRes.value[i][j].extend(mat.value[i][j])
                matRes.value[i][j].append(Binary('-'))
                matRes.value[i][j].append(Constant(int(const)))
    matRes = simplifyMatrix(matRes)
    return matRes


def scalarMult(const, mat):
    """Multiplies constant terms with Matrix

    Arguments:
        const {string}--- constant value
        mat {visma.matrix.structure.Matrix} -- matrix token

    Returns:
        matRes {visma.matrix.structure.Matrix} -- product matrix token
    """
    matRes = Matrix()
    matRes.empty([mat.dim[0], mat.dim[1]])
    for i in range(mat.dim[0]):
        for j in range(mat.dim[1]):
            if len(mat.value[i][j]) != 1:
                matRes.value[i][j].append(Expression(mat.value[i][j]))
            else:
                matRes.value[i][j].extend(mat.value[i][j])

            matRes.value[i][j].append(Binary('*'))
            matRes.value[i][j].append(Constant(int(const)))
    matRes = simplifyMatrix(matRes)
    return matRes


def scalarDiv(const, mat):
    """Divides constant terms with Matrix

    Arguments:
        const {string}--- constant value
        mat {visma.matrix.structure.Matrix} -- matrix token

    Returns:
        matRes {visma.matrix.structure.Matrix} -- result matrix token
    """
    if const != 0:
        matRes = Matrix()
        matRes.empty([mat.dim[0], mat.dim[1]])
        for i in range(mat.dim[0]):
            for j in range(mat.dim[1]):
                if len(mat.value[i][j]) != 1:
                    matRes.value[i][j].append(Expression(mat.value[i][j]))
                else:
                    matRes.value[i][j].extend(mat.value[i][j])

                matRes.value[i][j].append(Binary('/'))
                matRes.value[i][j].append(Constant(int(const)))
        matRes = simplifyMatrix(matRes)
        return matRes
    else:
        logger.error("ZeroDivisionError: Cannot divide matrix by zero")


def traceMat(mat):
    """Returns the trace of a square matrix (sum of diagonal elements)

    Arguments:
        mat {visma.matrix.structure.Matrix} -- matrix token

    Returns:
        trace {visma.matrix.structure.Matrix} -- 1x1 Matrix token
    """
    trace = Matrix()
    trace.empty([1, 1])
    for i in range(mat.dim[0]):
        if len(mat.value[i][i]) != 1:
            trace.value[0][0].append(Expression(mat.value[i][i]))
        else:
            trace.value[0][0].extend(mat.value[i][i])
        trace.value[0][0].append(Binary('+'))
    trace.value[0][0].append(Constant('0'))
    trace.value[0][0] = simplify(trace.value[0][0])
    trace = simplifyMatrix(trace)
    return trace
