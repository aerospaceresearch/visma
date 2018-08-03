from visma.functions.constant import Constant


class Matrix(object):
    """Class for matrix type

    The elements in the matrix are function tokens.

    Example:
        [              1            ,            2xy^2            ;
                      4xy           ,             x+y             ]
        is tokenized to
        [         [Constant]        ,          [Variable]         ;
                  [Variable]        , [Variable, Binary, Variable]]
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

    def transpose(self, RHS, wrtVar=None):
        pass

    def inverse(self):
        pass

    def cofactor(self):
        pass

    def dimension(self):
        """Gets the dimension of the matrix

        dim[0] -- no of rows
        dim[1] -- no of columns
        """
        self.dim[0] = len(self.value)
        self.dim[1] = len(self.value[0])


class ValMat(Matrix):
    """[summary]

    [description]

    Extends:
        Matrix
    """
    def __init__(self, dim, token):
        super().__init__()
        for i in range(0, dim[0]):
            row = []
            for j in range(0, dim[1]):
                if i == j:
                    row.append(token)
                else:
                    row.append(token)
            self.value.append(row)


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
