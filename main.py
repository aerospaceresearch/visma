import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui


class Window(QtGui.QMainWindow):
    
    def __init__(self):
        super(Window, self).__init__()
        
        self.initUI()
        
        
    def initUI(self):               
        
        textEdit = QtGui.QTextEdit()
        self.setCentralWidget(textEdit)

        exitAction = QtGui.QAction(QtGui.QIcon('resources/exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exitAction)
        
        workSpace = WorkSpace()
        self.setCentralWidget(workSpace)
        self.setGeometry(300, 300, 1280, 720)
        self.setWindowTitle('VisMa')    
        self.show()
        
        

class WorkSpace(QWidget):

    def __init__(self):
        super(WorkSpace, self).__init__()
        self.initUI()
    
    def initUI(self):
    
        hbox = QHBoxLayout(self)

        eqautionList = QFrame()
        eqautionList.setFrameShape(QFrame.StyledPanel)
        #eqautionList.setStyleSheet("background-color: rgb(0, 0, 255)")
        inputList = QFrame()
        inputList.setFrameShape(QFrame.StyledPanel)
        #inputList.setStyleSheet("background-color: rgb(0, 255, 0)")
        buttonSpace = QFrame()
        buttonSpace.setFrameShape(QFrame.StyledPanel)
        #buttonSpace.setStyleSheet("background-color: rgb(255, 0, 0)")

        splitter1 = QSplitter(Qt.Vertical)
        textedit = QTextEdit()
        splitter1.addWidget(textedit)
        splitter1.addWidget(buttonSpace)
        splitter1.setSizes([600, 400])

        splitter2 = QSplitter(Qt.Horizontal)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(inputList)
        splitter2.setSizes([800, 400])

        splitter3 = QSplitter(Qt.Horizontal)
        splitter3.addWidget(eqautionList)
        splitter3.addWidget(splitter2)
        splitter3.setSizes([400, 1200])
        
        hbox.addWidget(splitter3)

        self.setLayout(hbox)
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))

    
def main():
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()