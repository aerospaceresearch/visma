from __future__ import division
import copy

from visma.functions.structure import Function
from visma.functions.constant import Constant, Zero
from visma.functions.variable import Variable
from visma.functions.exponential import Logarithm
from visma.functions.operator import Operator, Binary
from visma.simplify.simplify import simplify

###################
# Integration #
###################


def integrate(tokens, wrtVar):

    tokens, availableOperations, token_string, animation, comments = simplify(tokens)

    tokens, animNew, commentsNew = (integrateTokens(tokens, wrtVar))

    animation.append(animNew)
    comments.append(commentsNew)

    tokens, availableOperations, token_string, animation2, comments2 = simplify(tokens)

    animation2.pop(0)
    comments2.pop(0)
    animation.extend(animation2)
    comments.extend(comments2)

    return tokens, availableOperations, token_string, animation, comments


# This is only applicable to Variable and Constant type
# Kind of hacky as of now
# Must be modified to accomodate other function types
# Will add integrate class method later

def integrateTokens(funclist, wrtVar):
    intFunc = []
    animNew = []
    commentsNew = ["Integrating with respect to " + r"$" + wrtVar + r"$" + "\n"]
    for func in funclist:
        if isinstance(func, Operator):  # add isFuntionOf
            intFunc.append(func)
        else:
            newfunc = []
            while(isinstance(func, Function)):
                commentsNew[0] += r"$" + "\int \ " + "( " + func.__str__() + ")" + " d" + wrtVar + r"$"
                funcCopy = copy.deepcopy(func)
                if wrtVar in funcCopy.functionOf():
                    if not isinstance(funcCopy, Constant):
                        for i, var in enumerate(funcCopy.value):
                            log = False
                            if var == wrtVar:
                                if(funcCopy.power[i] == -1):
                                    log = True
                                    funcLog = Logarithm()
                                    funcLog.setProp(coeff=1, power=1)
                                    funcLog.operand.append(Variable())
                                    funcLog.operand[-1].coefficient = 1
                                    funcLog.operand[-1].value.append(funcCopy.value[i])
                                    funcLog.operand[-1].power.append(1)
                                    del funcCopy.power[i]
                                    del funcCopy.value[i]
                                    if funcCopy.value == []:
                                        funcCopy.__class__ = Constant
                                        funcCopy.value = funcCopy.coefficient
                                        funcCopy.coefficient = 1
                                        funcCopy.power = 1
                                    funcCopy = [funcCopy]
                                    funcJoin = Binary()
                                    funcJoin.value = '*'
                                    funcCopy.append(funcJoin)
                                    funcCopy.append(funcLog)
                                else:
                                    funcCopy.power[i] += 1
                                    funcCopy.coefficient /= funcCopy.power[i]

                        if log:
                            commentsNew[0] += r"$" + "= " + funcCopy[0].__str__() + "*" + funcCopy[2].__str__() + "\ ;\ " + r"$"
                            newfunc.extend(funcCopy)
                        else:
                            commentsNew[0] += r"$" + "= " + funcCopy.__str__() + "\ ;\ " + r"$"
                            newfunc.append(funcCopy)
                else:
                    if isinstance(funcCopy, Variable):
                        funcCopy.value.append(wrtVar)
                        funcCopy.power.append(1)
                    if isinstance(funcCopy, Constant):
                        coeff = funcCopy.value
                        funcCopy = Variable()
                        funcCopy.coefficient = coeff
                        funcCopy.value.append(wrtVar)
                        funcCopy.power.append(1)
                    newfunc.append(funcCopy)
                    commentsNew[0] += r"$" + "= " + funcCopy.__str__() + "\ ;\ " + r"$"

                if func.operand is None:
                    break
                else:
                    func = func.operand
                    if isinstance(func, Constant):
                        intFunc = Zero()
                        break

            intFunc.extend(newfunc)

    animNew.extend(intFunc)
    return intFunc, animNew, commentsNew
