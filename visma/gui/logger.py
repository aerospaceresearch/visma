import os
import sys
import datetime
from PyQt5.QtWidgets import QVBoxLayout, qApp, QLabel, QDoubleSpinBox, QScrollArea, QPlainTextEdit, QTextEdit, QApplication, QWidget
from visma.gui import window

INFO = 20
WARNING = 30
ERROR = 40
CRITICAL = 50
THRES_LEV = 0
NAME = ''
logString = ''
now = datetime.datetime.now()

'''
def logTextBox(workspace):
    workspace.logBox = QPlainTextEdit()
    workspace.logBox.setReadOnly(True)
    textLayout = QVBoxLayout()
    textLayout.addWidget(workspace.logBox)
    return textLayout

def refreshLogger(workspace):
    text = open('/home/mayank/Desktop/mynk/aeroME/visma/log.txt').read()
    workspace.logBox.setPlainText(text)    
'''

def setLogName(name):
    global NAME
    NAME = name

def setLevel(level):
    global THRES_LEV
    THRES_LEV = level

def info(msg, *args):
    if INFO >= THRES_LEV:
        logWriter('INFO', msg, *args)

def warn(msg, *args):
    if INFO >= THRES_LEV:
        logWriter('WARNING', msg, *args)
        
def error(msg, *args):
    if ERROR >= THRES_LEV:
        logWriter('ERROR', msg, *args)
    
def logWriter(levType, msg, *args):
    try:
        f = open(os.path.abspath("log.txt"), "a")
    except IOError:
        print('Can\'t open the log file')
    logString = now.strftime("%Y-%m-%d %H:%M") + ' - ' + NAME + ' - ' + '%s: %s'%(levType, msg % args) + '\n'
    f.write(logString)
