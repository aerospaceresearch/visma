from visma.functions.constant import Constant
from visma.functions.operator import Multiply
from visma.functions.operator import Minus
from visma.functions.operator import Plus
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

    def __init__(self):
        self.scope = None
        self.value = []
        self.coefficient = 1
        self.power = 1
        self.dim = [0, 0]

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
        if mat is None:
            self.dimension()
            mat = np.array(self.value)
        if(mat.shape[0] > 2):
            ans = []
            for i in range(mat.shape[0]):
                mat1 = mat
                mat1 = np.concatenate((mat[1:, :i], mat[1::, i+1:]), axis=1)
                a = Expression()
                a.tokens = self.determinant(mat1)
                m = Multiply()
                a = [a] + [m] + mat[0][i].tolist()
                if(i % 2 == 0):
                    ans = ans + [Plus()] + a
                else:
                    ans = ans + [Minus()] + a
        elif(mat.shape[0] == 2):
            a = Multiply()
            b = Minus()
            mat = mat.tolist()
            ans = mat[0][0] + [a] + mat[1][1] + [b] + mat[0][1] + [a] + mat[1][0]
        else:
            ans = mat[0][0]
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
        for i in range(self.dim[0]):
            trace.extend(self.value[i][i])
            trace.append(Binary('+'))
        trace.append(Constant(0))
        trace, _, _, _, _ = simplify(trace)
        return trace


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
