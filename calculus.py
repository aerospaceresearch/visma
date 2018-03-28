import functions

###################
# Differentiation #
###################

# following is for differentiating functions within functions like func1(func2(func3))

def differentiation(func):

    funclist = []

    while(func.__class__ != Variable):

        func.coefficient *= func.power
        func.power -= 1
        if(func.power == 0):
            const = func
            const.value = const.coefficient
            const.differentiate()
            funclist.append(const)
        else:
            funclist.append(func)

        func.differentiate()
        funclist.append(func)

# TODO: Send each of these steps to animator

        '''
        animator code
        '''

        func = func.operand

        if(func.__class__ == Constant):
            func.value = 0
            func.coefficient = 1
            func.power = 1
            funclist = [func]
            break

# The differentiated function is the product of all functions in funclist
return funclist[]

# TODO: Find workaround for differentiating func1(func2+func3)
