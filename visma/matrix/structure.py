from visma.functions.constant import Constant
from visma.functions.operator import Multiply
from visma.functions.operator import Minus
from visma.functions.operator import Plus
from visma.functions.constant import Zero
from visma.functions.structure import Expression
import numpy as np
from visma.functions.operator import Binary


class Matrix(object):
    """Class for matrix type

    The elements in the matrix are function tokens.

    Example:
        [              1            ,            2xy^2            ;
                      4xy           ,             x+y             ]
        is tokenized to
        [[         [Constant]        ,          [Variable]        ],
         [         [Variable]        , [Variable, Binary, Variable]]]
        and stored in matrix.value.
    """

    def __init__(self, value=None, coefficient=None, power=None, dim=None, scope=None):
        self.scope = None
        if value is not None:
            self.value = value
        else:
            self.value = []
        if coefficient is not None:
            self.coefficient = coefficient
        else:
            self.coefficient = 1
        if power is not None:
            self.power = power
        else:
            self.power = 1
        if dim is not None:
            self.dim = dim
        else:
            self.dim = [0, 0]

    def convertMatrixToString(self, Latex=False):
        from visma.io.parser import tokensToString
        MatrixString = ''
        self.dim[0] = len(self.value)
        self.dim[1] = len(self.value[0])
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                if not Latex:
                    MatrixString += tokensToString(self.value[i][j]) + '\t'
                else:
                    MatrixString += tokensToString(self.value[i][j]) + '    '
            MatrixString += '\n'
        return MatrixString

    def __add__(self, other):
        """Adds two matrices
         Arguments:
            self {visma.matrix.structure.Matrix} -- matrix token
            other {visma.matrix.structure.Matrix} -- matrix token
         Returns:
            matSum {visma.matrix.structure.Matrix} -- sum matrix token
         Note:
            Make dimCheck before calling addMatrix
        """
        matSum = Matrix()
        matSum.empty(self.dim)
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                matSum.value[i][j].extend(self.value[i][j])
                matSum.value[i][j].append(Binary('+'))
                matSum.value[i][j].extend(other.value[i][j])
        from visma.matrix.operations import simplifyMatrix
        matSum = simplifyMatrix(matSum)
        return matSum

    def __sub__(self, other):
        """Subtracts two matrices
         Arguments:
            self {visma.matrix.structure.Matrix} -- matrix token
            other {visma.matrix.structure.Matrix} -- matrix token
         Returns:
            matSub {visma.matrix.structure.Matrix} -- subtracted matrix token
         Note:
            Make dimCheck before calling subMatrix
        """
        matSub = Matrix()
        matSub.empty(self.dim)
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                matSub.value[i][j].extend(self.value[i][j])
                matSub.value[i][j].append(Binary('-'))
                matSub.value[i][j].extend(other.value[i][j])
        from visma.matrix.operations import simplifyMatrix
        matSub = simplifyMatrix(matSub)
        return matSub

    def __mul__(self, other):
        """Multiplies two matrices
         Arguments:
            self {visma.matrix.structure.Matrix} -- matrix token
            other {visma.matrix.structure.Matrix} -- matrix token
         Returns:
            matPro {visma.matrix.structure.Matrix} -- product matrix token
         Note:
            Make mulitplyCheck before calling multiplyMatrix
            Not commutative
        """
        matPro = Matrix()
        matPro.empty([self.dim[0], other.dim[1]])
        for i in range(self.dim[0]):
            for j in range(other.dim[1]):
                for k in range(self.dim[1]):
                    if matPro.value[i][j] != []:
                        matPro.value[i][j].append(Binary('+'))
                    if len(self.value[i][k]) != 1:
                        matPro.value[i][j].append(Expression(self.value[i][k]))
                    else:
                        matPro.value[i][j].extend(self.value[i][k])
                    matPro.value[i][j].append(Binary('*'))
                    if len(other.value[k][j]) != 1:
                        matPro.value[i][j].append(Expression(other.value[k][j]))
                    else:
                        matPro.value[i][j].extend(other.value[k][j])
        from visma.matrix.operations import simplifyMatrix
        matPro = simplifyMatrix(matPro)
        return matPro

    def __str__(self):
        represent = "["
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                for tok in self.value[i][j]:
                    represent += tok.__str__()
                represent += ","
            represent = represent[:-1] + ";"
        represent = represent[:-1] + "]"
        return represent

    def empty(self, dim=None):
        """Empties the matrix into a matrix of dimension dim

        Keyword Arguments:
            dim {list} -- dimension of matrix (default: {None})
        """
        if dim is not None:
            self.dim = dim
        self.value = [[[] for _ in range(self.dim[1])] for _ in range(self.dim[0])]

    def prop(self, scope=None, value=None, coeff=None, power=None, operand=None, operator=None):
        if scope is not None:
            self.scope = scope
        if value is not None:
            self.value = value
        if coeff is not None:
            self.coefficient = coeff
        if power is not None:
            self.power = power

    def isSquare(self):
        """Checks if matrix is square

        Returns:
            bool -- if square matrix or not
        """
        if self.dim[0] == self.dim[1]:
            self.__class__ = SquareMat
            return True
        else:
            return False

    def isIdentity(self):
        """Checks if matrix is identity

        Returns:
            bool -- if identity matrix or not
        """
        if self.isDiagonal():
            for i in range(0, self.dim[0]):
                if self.value[i][i][0].value != 1:
                    return False
            self.__class__ = IdenMat
            return True
        else:
            return False

    def isDiagonal(self):
        """Checks if matrix is diagonal

        Returns:
            bool -- if diagonal matrix or not
        """
        if self.isSquare():
            for i in range(0, self.dim[0]):
                for j in range(0, self.dim[1]):
                    if i != j and (self.value[i][j][0].value != 0 or len(self.value[i][j]) > 1):
                        return False
            self.__class__ = DiagMat
            return True
        else:
            return False

    def dimension(self):
        """Gets the dimension of the matrix

        dim[0] -- number of rows
        dim[1] -- number of columns
        """
        self.dim[0] = len(self.value)
        self.dim[1] = len(self.value[0])

    def transposeMat(self):
        """Returns Transpose of Matrix

        Returns:
            matRes {visma.matrix.structure.Matrix} -- result matrix token
        """
        matRes = Matrix()
        matRes.empty([self.dim[1], self.dim[0]])
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                matRes.value[j][i] = self.value[i][j]
        return matRes


class SquareMat(Matrix):
    """Class for Square matrix

    Square matrix is a matrix with equal dimensions.

    Extends:
        Matrix
    """

    def determinant(self, mat=None):
        """Calculates square matrices' determinant

        Returns:
            list of tokens forming the determinant
        """
        from visma.simplify.simplify import simplify

        if mat is None:
            self.dimension()
            mat = np.array(self.value)
        if(mat.shape[0] > 2):
            ans = []
            for i in range(mat.shape[0]):
                mat1 = SquareMat()
                mat1.value = np.concatenate((mat[1:, :i], mat[1:, i+1:]), axis=1).tolist()
                a, _, _, _, _ = simplify(mat1.determinant())
                if(a[0].value != 0 and a != []):
                    a, _, _, _, _ = simplify(a + [Multiply()] + mat[0][i].tolist())
                    if(i % 2 == 0):
                        if(ans != []):
                            ans, _, _, _, _ = simplify(ans + [Plus()] + a)
                        else:
                            ans = a
                    else:
                        ans, _, _, _, _ = simplify(ans + [Minus()] + a)
        elif(mat.shape[0] == 2):
            a = Multiply()
            b = Minus()
            mat = mat.tolist()
            a1, _, _, _, _ = simplify(mat[0][0] + [a] + mat[1][1])
            a2, _, _, _, _ = simplify(mat[0][1] + [a] + mat[1][0])
            ans, _, _, _, _ = simplify([a1[0], b, a2[0]])
            if (isinstance(ans[0], Minus) or isinstance(ans[0], Plus)) and ans[0].value not in ['+', '-']:
                ans[0] = Constant(ans[0].value)
        else:
            ans, _, _, _, _ = simplify(mat[0][0])
        if not ans:
            ans = Zero()
        return ans

    def traceMat(self):
        """Returns the trace of a square matrix (sum of diagonal elements)

        Arguments:
            mat {visma.matrix.structure.Matrix} -- matrix token

        Returns:
            trace {visma.matrix.structure.Matrix} -- string token
        """
        from visma.simplify.simplify import simplify
        trace = []
        self.dim[0] = len(self.value)
        self.dim[1] = len(self.value[0])
        for i in range(self.dim[0]):
            trace.extend(self.value[i][i])
            trace.append(Binary('+'))
        trace.pop()
        trace, _, _, _, _ = simplify(trace)
        return trace

    def inverse(self):
        """Calculates the inverse of the matrix using Gauss-Jordan Elimination

        Arguments:
            matrix {visma.matrix.structure.Matrix} -- matrix token

        Returns:
            inv {visma.matrix.structure.Matrix} -- result matrix token
        """
        from visma.simplify.simplify import simplify
        from visma.io.tokenize import tokenizer
        from visma.io.parser import tokensToString

        if tokensToString(self.determinant()) == "0":
            return -1
        self.dim[0] = len(self.value)
        self.dim[1] = len(self.value[0])
        n = self.dim[0]
        mat = Matrix()
        mat.empty([n, 2*n])
        for i in range(0, n):
            for j in range(0, 2*n):
                if j < n:
                    mat.value[i][j] = self.value[i][j]
                else:
                    mat.value[i][j] = []

        for i in range(0, n):
            for j in range(n, 2*n):
                if j == (i + n):
                    mat.value[i][j].extend(tokenizer('1'))
                else:
                    mat.value[i][j].extend(tokenizer("0"))

        for i in range(n-1, 0, -1):
            if mat.value[i-1][0][0].value < mat.value[i][0][0].value:
                for j in range(0, 2*n):
                    temp = mat.value[i][j]
                    mat.value[i][j] = mat.value[i-1][j]
                    mat.value[i-1][j] = temp

        for i in range(0, n):
            for j in range(0, n):
                if j != i:
                    temp = []
                    if len(mat.value[j][i]) != 1:
                        temp.append(Expression(mat.value[j][i]))
                    else:
                        temp.extend(mat.value[j][i])
                    temp.append(Binary('/'))
                    if len(mat.value[i][i]) != 1:
                        temp.append(Expression(mat.value[i][i]))
                    else:
                        temp.extend(mat.value[i][i])
                    temp, _, _, _, _ = simplify(temp)

                    for k in range(0, 2*n):
                        t = []
                        if mat.value[i][k][0].value != 0:
                            if len(mat.value[i][k]) != 1:
                                t.append(Expression(mat.value[i][k]))
                            else:
                                t.extend(mat.value[i][k])
                            t.append(Binary('*'))
                            if len(temp) != 1:
                                t.append(Expression(temp))
                            else:
                                t.extend(temp)
                            t, _, _, _, _ = simplify(t)
                            mat.value[j][k].append(Binary('-'))
                            if len(t) != 1:
                                mat.value[j][k].append(Expression(t))
                            else:
                                mat.value[j][k].extend(t)
                            mat.value[j][k], _, _, _, _ = simplify(mat.value[j][k])

        for i in range(0, n):
            temp = []
            temp.extend(mat.value[i][i])
            for j in range(0, 2*n):
                if mat.value[i][j][0].value != 0:
                    mat.value[i][j].append(Binary('/'))
                    mat.value[i][j].extend(temp)
                    mat.value[i][j], _, _, _, _ = simplify(mat.value[i][j])

        inv = SquareMat()
        inv.empty([n, n])
        for i in range(0, n):
            for j in range(n, 2*n):
                inv.value[i][j-n] = mat.value[i][j]
        return inv

    def cofactor(self):
        """Calculates cofactors matrix of the Square Matrix

        Returns:
            An object of type SquareMat
        """
        mat1 = SquareMat()
        mat1.value = []
        for i in range(self.dim[0]):
            if(i % 2 == 0):
                coeff = -1
            else:
                coeff = 1
            mat1.value.append([])
            for j in range(self.dim[1]):
                coeff *= -1
                mat = SquareMat()
                temp = np.array(self.value)
                mat.value = np.concatenate((np.concatenate((temp[:i, :j], temp[i+1:, :j])), np.concatenate((temp[:i, j+1:], temp[i+1:, j+1:]))), axis=1).tolist()
                val = mat.determinant()[0]
                val.value *= coeff
                mat1.value[i].append([val])
        mat1.dimension()
        return mat1


class DiagMat(SquareMat):
    """Class for Diagonal matrix

    Diagonal matrix is a square matrix with all elements as 0 except for the diagonal elements.

    Extends:
        SquareMat
    """

    def __init__(self, dim, diagElem):
        """
        dim {list} -- dimension of matrix
        diagElem {list} -- list of tokens list
        """
        super().__init__()
        self.dim = dim
        for i in range(0, dim[0]):
            row = []
            for j in range(0, dim[1]):
                if i == j:
                    row.append(diagElem[i])
                else:
                    row.append([Constant(0)])
            self.value.append(row)


class IdenMat(DiagMat):
    """Class for identity matrix

    Identity matrix is a diagonal matrix with all elements as 0 except for the diagonal elements which are 1.

    Extends:
        DiagMat
    """

    def __init__(self, dim):
        super().__init__(dim, [[Constant(1)]]*dim[0])
        for i in range(0, dim[0]):
            self.value[i][i] = Constant(1)
