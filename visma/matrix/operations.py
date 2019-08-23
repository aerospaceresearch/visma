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
    mat.dim[0] = len(mat.value)
    mat.dim[1] = len(mat.value[0])
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
    matA.dim[0] = len(matA.value)
    matA.dim[1] = len(matA.value[0])
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
    matA.dim[0] = len(matA.value)
    matA.dim[1] = len(matA.value[0])
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
    matA.dim[0] = len(matA.value)
    matA.dim[1] = len(matA.value[0])
    matB.dim[0] = len(matB.value)
    matB.dim[1] = len(matB.value[0])
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
    mat.dim[0] = len(mat.value)
    mat.dim[1] = len(mat.value[0])
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


def row_echelon(mat):
    """
    Returns the row echelon form of the given matrix

    Arguments:
        mat {visma.matrix.structure.Matrix} -- matrix token

    Returns:
        row_echelon {visma.matrix.structure.Matrix} -- result matrix token
    """

    N = mat.dim[0]
    M = mat.dim[1]
    for k in range(0, N):
        if abs(mat.value[k][k][0].value) == 0.0:
            if k == N-1:
                return simplifyMatrix(mat)
            else:
                for i in range(0, N):
                    t = mat.value[k][i]
                    mat.value[k][i] = mat.value[k+1][i]
                    mat.value[k+1][i] = t
        else:
            for i in range(k+1, N):
                temp = []
                temp.extend(mat.value[i][k])
                temp.append(Binary('/'))
                temp.extend(mat.value[k][k])
                temp, _, _, _, _ = simplify(temp)
                for j in range(k+1, M):
                    temp2 = []
                    temp2.extend(mat.value[k][j])
                    temp2.append(Binary('*'))
                    temp2.extend(temp)
                    temp2, _, _, _, _ = simplify(temp2)
                    mat.value[i][j].append(Binary('-'))
                    mat.value[i][j].extend(temp2)
                mat.value[i][k].append(Binary('*'))
                mat.value[i][k].append(Constant(0))
                mat = simplifyMatrix(mat)
    return simplifyMatrix(mat)


def gauss_elim(mat):
    """
    Returns calculated values of unknown variables

    Arguments:
        mat {visma.matrix.structure.Matrix} -- matrix token

    Returns:
        result {visma.matrix.structure.Matrix} -- result matrix token
    Note: result is a Nx1 matrix
    """

    echelon = Matrix()
    echelon = row_echelon(mat)
    result = Matrix()
    result.empty([mat.dim[0], 1])

    N = mat.dim[0]
    M = mat.dim[1]
    index = N-1
    for i in range(N-1, -1, -1):
        sum_ = []
        temp = []
        if echelon.value[i][i][0].value == 0.0:        # no unique solution for this case
            return -1
        for j in range(i+1, M-1):
            temp = []
            temp.extend(echelon.value[i][j])
            temp.append(Binary('*'))
            temp.extend(result.value[j][0])
            temp, _, _, _, _ = simplify(temp)
            sum_.extend(temp)
            if j != M-2:
                sum_.append(Binary('+'))
        sum_, _, _, _, _ = simplify(sum_)

        result.value[index][0].extend(echelon.value[i][M-1])
        if sum_:
            if sum_[0].value < 0:
                result.value[index][0].append(Binary('-'))     # negative sign makes the negative sign in value positive
            else:
                result.value[index][0].append(Binary('-'))
            result.value[index][0].extend(sum_)
        result.value[index][0], _, _, _, _ = simplify(result.value[index][0])
        result.value[index][0].append(Binary('/'))
        result.value[index][0].extend(echelon.value[i][i])
        result.value[index][0], _, _, _, _ = simplify(result.value[index][0])
        index -= 1

    return result
