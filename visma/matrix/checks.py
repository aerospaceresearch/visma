# from visma.gui import logger


def isMatrix(matTok):
    """Checks if given token is matrix

    Arguments:
        matTok {visma.matrix.structure.Matrix} -- matrix token

    Returns:
        bool -- if matrix or not
    """
    matTok.dimension()
    for i in range(0, matTok.dim[0]):
        if len(matTok.value[i]) != matTok.dim[1]:
            # logger.setLevel(0)
            # logger.setLogName('\'isMatrix\' in checks.py')
            # logger.error('Invalid matrix. Check dimensions')
            return False
    return True


def dimCheck(matA, matB):
    """Checks if dimension of the given two matrices are same

    Arguments:
        matA {visma.matrix.structure.Matrix} -- matrix token
        matB {visma.matrix.structure.Matrix} -- matrix token

    Returns:
        bool -- if dimensions same or not
    """
    matA.dimension()
    matB.dimension()
    if matA.dim == matB.dim:
        return True
    return False


def multiplyCheck(matA, matB):
    """Checks if the two matrices can be multiplied

    Arguments:
        matA {visma.matrix.structure.Matrix} -- matrix token
        matB {visma.matrix.structure.Matrix} -- matrix token

    Returns:
        bool -- to multiply or not
    """
    if matA.dim[1] == matB.dim[0]:
        return True
    return False


def isEqual(matA, matB):
    """Checks if the two matrices are equal

    Arguments:
        matA {visma.matrix.structure.Matrix} -- matrix token
        matB {visma.matrix.structure.Matrix} -- matrix token

    Returns:
        bool -- to multiply or not
    """
    if not dimCheck(matA, matB) or matA.__str__() != matB.__str__():
        return False
    else:
        return True
