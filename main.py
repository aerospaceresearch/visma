import os
from visma.gui.window import initGUI
from visma.gui.cli import commandExec
from visma.gui import logger


def init():
    open(os.path.abspath("log.txt"), "w").close()
    logger.setLevel(10)
    logger.setLogName('main')
    logger.info('Initialising VisMa...(currently in CLI mode)')
    userInterface = "-----------------------------------------------------------------------------\n" \
                    "| simplify( Equation )   ->> Simplifies the given equation.                 |\n" \
                    "|                                                                           |\n" \
                    "| exit     ->> Exits the Program.                                           |\n" \
                    "-----------------------------------------------------------------------------\n" \
                    ">>> "
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
