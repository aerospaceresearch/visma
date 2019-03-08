import os
import datetime
from PyQt5.QtWidgets import QTextEdit, QVBoxLayout


INFO = 20
WARNING = 30
ERROR = 40
CRITICAL = 50
THRES_LEV = 0
NAME = ''
logString = ''
now = datetime.datetime.now()


def logTextBox(workspace):
    workspace.logBox = QTextEdit()
    workspace.logBox.setReadOnly(True)
    textLayout = QVBoxLayout()
    textLayout.addWidget(workspace.logBox)
    return textLayout


def setLogName(name):
    global NAME
    NAME = name


def setLevel(level):
    global THRES_LEV
    THRES_LEV = level


def info(msg, *args):
    if INFO >= THRES_LEV:
        info = logWriter('INFO', msg, *args)
        return info


def warn(msg, *args):
    if WARNING >= THRES_LEV:
        warn = logWriter('WARNING', msg, *args)
        return warn


def error(msg, *args):
    if ERROR >= THRES_LEV:
        error = logWriter('ERROR', msg, *args)
        return error


def logWriter(levType, msg, *args):
    try:
        f = open(os.path.abspath("log.txt"), "a")
    except IOError:
        print('Can\'t open the log file')
    logString = now.strftime("%Y-%m-%d %H:%M") + ' - ' + NAME + ' - ' + '%s: %s' % (levType, msg % args) + '\n'
    f.write(logString)
    return logString
