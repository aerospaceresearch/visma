from visma.gui.window import initGUI
# from visma.gui.cli import commandExec


def init():
    cin = input('>>> ')
    while(cin != 'exit'):
        if cin == 'gui':
            initGUI()
        else:
            # commandExec(cin) [CLI module goes here]
            pass
        cin = input('>>> ')


if __name__ == '__main__':
    init()
