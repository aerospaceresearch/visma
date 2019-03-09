import os
from visma.gui.window import initGUI
from visma.gui.cli import commandExec
from visma.gui import logger
from subprocess import call
from pyfiglet import Figlet


def init():
    open(os.path.abspath("log.txt"), "w").close()
    logger.setLevel(10)
    logger.setLogName('main')
    logger.info('Initialising VisMa...(currently in CLI mode)')
    ClearScr()
    cin = input('>>> ')
    while(cin != 'exit'):
        if cin == 'gui':
            initGUI()
        if cin =='clear':
            ClearScr()
        else:
            try:
                commandExec(cin)
            except Exception:
                logger.error("Invalid Expression: %s ", cin)
                print("Invalid Expression")
                pass
        cin = input('>>> ')
    if (cin == 'exit'):
        logger.info('Exiting VisMa...')
def ClearScr():
    try:
        call('clear')#in case of linux/unix/mac 
    except:
        call('cls')#in case of windows
    print("")
    print("__"*100);
    f = Figlet(font='slant')
    print(f.renderText('VISual MAth'))
    print("")
    print("__"*100);

if __name__ == '__main__':
    init()
