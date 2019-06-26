import os
from cmd import Cmd
from visma.gui.cli import commandExec
from visma.gui.window import initGUI
from visma.gui import logger


def init():
    open(os.path.abspath("log.txt"), "w").close()
    logger.setLevel(10)
    logger.setLogName('main')
    logger.info('Initialising VisMa...(currently in CLI mode)')

    class VisMa_Prompt(Cmd):
        '''This inititates the main VisMa Prompt from where user may move to CLI/GUI'''

        userManual = "|_________________________________________________________________________________________________|\n"\
                     "| gui  ->> opens Visma in GUI mode.                                                               |\n"\
                     "| Ctrl + D ->> Closes the prompt.                                                                     |\n"\
                     "| exit ->> Closes the prompt.                                                                     |\n"\
                     "|-------------------------------------------------------------------------------------------------|\n"\
                     "| simplify( equation or expression ) ->> Simplifies the given equation.                           |\n"\
                     "| addition( equation or expression ) ->> Adds the elements used.                                  |\n"\
                     "| subtraction( equation or expression ) ->> Subtracts the elements used.                          |\n"\
                     "| multiplication( equation or expression )  ->> Multiplies the elements used.                     |\n"\
                     "| division( equation or expression )  ->> Divides the elements used.                              |\n"\
                     "|-------------------------------------------------------------------------------------------------|\n"\
                     "| factorize( expression )  ->> Factorizes the expression.                                         |\n"\
                     "| find-roots( equation )  ->> Solves the quadratic equation for the variable in the equation.     |\n"\
                     "| solve( equation , variable )  ->> Solves the equation for the given variable.                   |\n"\
                     "|-------------------------------------------------------------------------------------------------|\n"\
                     "| integrate( expression , variable )  ->> Integrates the expression by the given variable.        |\n"\
                     "| differentiate( expression , variable ) ->> Differentiates the expression by the given variable. |\n"\
                     "|_________________________________________________________________________________________________|\n"\

        prompt = '>>> '
        intro = "Welcome! This is Visual Maths Interactive Shell...\n" + "type 'help' for a User Manual and Ctrl + D to Exit prompt\n"

        def do_exit(self, inp):
            '''Exits VisMa Prompt'''
            print("Exiting VisMa...")
            logger.info('Exiting VisMa...')
            return True

        def emptyline(self):
            logger.error('Empty line received as input')
            print('Empty line received as input\n')

        def do_manual(self, inp):
            '''Displays a list of commands that can be used'''
            print(self.userManual)

        def do_gui(self, inp):
            '''Starts GUI of VisMa'''
            initGUI()
            print("Initiating GUI...")
            logger.info("Initiating GUI...")

        def default(self, inp):
            '''Directs to CommandExec and performs operations thereafter'''
            try:
                commandExec(inp)
            except Exception:
                logger.error('Invalid Expression: ' + inp)
                print('Invalid Expression: ' + inp + '\n')

        do_EOF = do_exit

    VisMa_Prompt().cmdloop()


if __name__ == '__main__':
    init()
