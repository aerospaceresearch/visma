from visma.functions.constant import Constant
from visma.functions.structure import Expression
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

    def __init__(self):
        self.scope = None
        self.value = []
        self.coefficient = 1
        self.power = 1
        self.dim = [0, 0]

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

    def inverse(self):
        pass

    def cofactor(self):
        pass

    def dimension(self):
        """Gets the dimension of the matrix

        dim[0] -- number of rows
        dim[1] -- number of columns
        """
        self.dim[0] = len(self.value)
        self.dim[1] = len(self.value[0])

    def transposeMat(self):
        """Returns Transpose of Matrix

        Arguments:
            mat {visma.matrix.structure.Matrix} -- matrix token

        Returns:
            matRes {visma.matrix.structure.Matrix} -- result matrix token
        """
        matRes = Matrix()
        matRes.empty([self.dim[0], self.dim[1]])
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                matRes.value[j][i] = self.value[i][j]
        return matRes


class SquareMat(Matrix):

    def determinant(self):
        pass


class IdenMat(SquareMat):
    """Class for identity matrix

    Identity matrix is a square matrix with all elements as 0 except for the diagonal elements which are 1.

    Extends:
        SquareMat
    """

    def __init__(self, dim):
        super().__init__()
        for i in range(0, dim[0]):
            row = []
            for j in range(0, dim[1]):
                if i == j:
                    row.append(Constant(1))
                else:
                    row.append(Constant(0))
            self.value.append(row)
