class Matrix(object):

    def __init__(self):
        self.scope = None
        self.value = []
        self.coefficient = 1
        self.power = 1

    def setProp(self, scope=None, value=None, coeff=None, power=None, operand=None, operator=None):
        if scope is not None:
            self.scope = scope
        if value is not None:
            self.value = value
        if coeff is not None:
            self.coefficient = coeff
        if power is not None:
            self.power = power

    def isSquare(self):
        if self.dim[0] == self.dim[1]:
            self.__class__ = Square
            return True
        else:
            False

    def transpose(self, RHS, wrtVar=None):
        pass

    def inverse(self):
        pass

    def cofactor(self):
        pass


class Square(Matrix):

    def determinant(self):
        pass


class Identity(Square):

    def __init__(self, dim):
        super(Identity, self).__init__()
        for i in range(0, dim):
            row = []
            for j in range(0, dim):
                if i == j:
                    row.append(1)
                else:
                    row.append(0)
            self.value.append(row)
