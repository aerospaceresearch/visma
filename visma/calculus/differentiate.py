from visma.functions import *

###################
# Differentiation #
###################

# following is for differentiating functions within functions like func1(func2(func3))


def differentiate_tokens(funclist):

    difffunc = []

    for func in funclist:

        while(func.__class__ != Variable):

            func.coefficient *= func.power
            func.power -= 1
            if(func.power == 0):
                const = func
                const.value = 1
                const.differentiate()
                difffunc.append(const)
            else:
                difffunc.append(func)

            func.differentiate()
            difffunc.append(func)

            # TODO: Send each of these steps to animator

            func = func.operand

            if isinstance(func, Constant):
                func.value = 0
                func.coefficient = 1
                func.power = 1
                difffunc = [func]
                break


# The differentiated function list has been generated in difffunc

        return difffunc

# FIXME: Find workaround for differentiating func1(func2+func3)
