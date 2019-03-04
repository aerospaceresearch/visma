from visma.gui.window import initGUI
from visma.gui.cli import commandExec


def init():
    cin = input('>>> ')
    while cin != 'exit':
        if cin == 'gui':
            initGUI()
        else:
            try:
                commandExec(cin)
            except ZeroDivisionError:
                print("Invalid Expression")
        cin = input('>>> ')


if __name__ == '__main__':
    init()
