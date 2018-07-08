def isMatrix(matTok):
    matTok.dimension()
    for i in range(0, matTok.dim[0]):
        if len(matTok.value[i]) != matTok.dim[1]:
            return False
            # logger.log: Invalid matrix. Check dimensions.
    return True


def dimCheck(matA, matB):
    matA.dimension()
    matB.dimension()
    if matA.dim == matB.dim:
        return True
    return False


def mulDimCheck(matA, matB):
    if matA.dim[1] == matB.dim[0]:
        return True
    return False
