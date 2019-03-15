import os
from visma.gui.window import initGUI
from visma.gui.cli import commandExec
from visma.gui import logger

userInterface = "_______________________________________________________________________________________________\n"\
                    "| gui  ->> opens Visma in GUI mode.                                                           |\n"\
                    "| exit ->> Closes the program.                                                                |\n"\
                    "|---------------------------------------------------------------------------------------------|\n"\
                    "| simplify(equation or expression) ->> Simplifies the given equation.                         |\n"\
                    "| addition(equation or expression) ->> Adds the elements used.                                |\n"\
                    "| subtraction(equation or expression) ->> Subtracts the elements used.                        |\n"\
                    "| multiplication(equation or expression)  ->> Multiplies the elements used.                   |\n"\
                    "| division(equation or expression)  ->> Divides the elements used.                            |\n"\
                    "|---------------------------------------------------------------------------------------------|\n"\
                    "| factorize(expression)  ->> Factorizes the expression.                                       |\n"\
                    "| find-roots(equation)  ->> Solves the quadratic equation for the variable in the equation.   |\n"\
                    "| solve(equation , variable)  ->> Solves the equation for the given variable.                 |\n"\
                    "|---------------------------------------------------------------------------------------------|\n"\
                    "| integrate(expression , variable)  ->> Integrates the expression by the given variable.      |\n"\
                    "| differentiate(expression , variable)->> Differentiates the expression by the given variable.|\n"\
                    "|_____________________________________________________________________________________________|\n"\
                    ">>> "


def init():
    open(os.path.abspath("log.txt"), "w").close()
    logger.setLevel(10)
    logger.setLogName('main')
    logger.info('Initialising VisMa...(currently in CLI mode)')
    cin = input(userInterface)
    while cin != 'exit':
        if cin == 'gui':
            initGUI()
        else:
            try:
                commandExec(cin)
            except Exception:
                logger.error("Invalid Expression: %s ", cin)
                print("Invalid Expression")
        cin = input('>>> ')
    if cin == 'exit':
        logger.info('Exiting VisMa...')


if __name__ == '__main__':
    init()
