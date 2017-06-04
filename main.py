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
        eqautionList.setLayout(self.equationsLayout())
        eqautionList.setFrameShape(QFrame.StyledPanel)
        eqautionList.setStatusTip("Track of old equations")
        #eqautionList.setStyleSheet("background-color: rgb(0, 0, 255)")
        inputList = QFrame()
        inputList.setLayout(self.inputsLayout())
        inputList.setFrameShape(QFrame.StyledPanel)
        inputList.setStatusTip("Input characters")
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
        #QApplication.setStyle(QStyleFactory.create('Cleanlooks'))
        
    def equationsLayout(self):
       vbox = QVBoxLayout(self)

       listWidget = myListWidget()
        
       #Resize width and height
       listWidget.resize(400,300)
        
       listWidget.addItem("Equation 1"); 
       listWidget.addItem("Equation 2");
       listWidget.addItem("Equation 3");
       listWidget.addItem("Equation 4");
        
       listWidget.itemClicked.connect(listWidget.Clicked)    
       vbox.addWidget(listWidget)
       return vbox

    def inputsLayout(self):
        vbox = QVBoxLayout(self)
        
        combo = QtGui.QComboBox(self)
        combo.addItem("LaTeX")
        combo.addItem("Greek")
        #combo.move(50, 50)
    
        combo.activated[str].connect(self.onActivated)        
        
        
        vbox.addWidget(combo)
        inputBox = QGridLayout(self)
        buttons = {}
        for i in range(10):
            for j in range(3):
                buttons[(i, j)] = QtGui.QPushButton('row %d, col %d' % (i, j))
                inputBox.addWidget(buttons[(i, j)], i, j)       
        vbox.addLayout(inputBox)
        return vbox
    def onActivated(self, text):
        pass


class myListWidget(QListWidget):

   def Clicked(self,item):
      QMessageBox.information(self, "ListWidget", "You clicked: "+item.text())


def main():
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()