#####################
# Rules of Calculus #
#####################

import functions

###################
# Differentiation #
###################

'''
following is for differentiating functions within functions like func1(func2(func3))
'''

def differentiation(funclist):

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
            '''
            animator code
            '''

            func = func.operand

            if(func.__class__ == Constant):
                func.value = 0
                func.coefficient = 1
                func.power = 1
                difffunc = [func]
                break


# The differentiated function list has been generated in difffunc

return difffunc[]

# TODO: Find workaround for differentiating func1(func2+func3)
