import copy

from visma.functions.structure import Function
from visma.functions.constant import Constant, Zero
from visma.functions.operator import Operator
from visma.solvers.solve import simplify_equation, tokens_to_string

###################
# Differentiation #
###################


def differentiate(lTokens, rTokens, wrtVar):
    lTokens, rTokens, availableOperations, \
      token_string, animation, comments \
      = simplify_equation(lTokens, rTokens)
    lTokens = differentiateTokens(lTokens, wrtVar)
    rTokens = differentiateTokens(rTokens, wrtVar)

    tokenToStringBuilder = copy.deepcopy(lTokens)
    animation.append(copy.deepcopy(tokenToStringBuilder))
    token_string = tokens_to_string(tokenToStringBuilder)
    comments.append([])
    return lTokens, rTokens, [], token_string, animation, comments


def differentiateTokens(funclist, wrtVar):
    difffunc = []
    for func in funclist:
        if isinstance(func, Operator) and wrtVar not in func.functionOf:
            difffunc.append(func)
        else:
            newfunc = []
            while(isinstance(func, Function)):
                funcCopy = copy.deepcopy(func)
                funcCopy.coefficient *= funcCopy.power
                # Fix: [0]
                funcCopy.power[0] -= 1
                if(func.power != 0):
                    newfunc.append(funcCopy)
                func.differentiate()
                if not(isinstance(func, Constant) and func.value == 1):
                    newfunc.append(func)

                # TODO: Send each of these steps to animator

                if func.operand is None:
                    break
                else:
                    func = func.operand

                if isinstance(func, Constant):
                    func = Zero()
                    newfunc = [func]
                    break
            difffunc.extend(newfunc)

        # The differentiated function list has been generated in difffunc
        # FIXME: Find workaround for differentiating func1(func2+func3)
        return difffunc
