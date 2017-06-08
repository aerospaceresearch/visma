import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui


class Window(QtGui.QMainWindow):
    
    def __init__(self):
        super(Window, self).__init__()
        self.initUI()

    def initUI(self):
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

    inputLaTeX = ['\\times', '\\div', '\\alpha', '\\beta', '\\gamma', '\\pi', '+', '-', '=', '^{}', '\\frac{}',
                       '\\\sqrt[n]{}']
    inputGreek = ['*', '/', u'\u03B1', u'\u03B2', u'\u03B3', '+', '-', '=', '^{}', 'sqrt[n]{}']
    buttons = {}
    inputBox = QGridLayout()
    selectedCombo = "LaTeX"
    global textedit

    def __init__(self):
        super(WorkSpace, self).__init__()
        self.initUI()

    def initUI(self):
    
        hbox = QHBoxLayout(self)

        eqautionList = QWidget()
        eqautionList.setLayout(self.equationsLayout())
        eqautionList.setStatusTip("Track of old equations")

        inputList = QWidget()
        inputList.setLayout(self.inputsLayout())
        inputList.setStatusTip("Input characters")

        buttonSpace = QWidget()
        buttonSpace.setLayout(self.buttonsLayout())

        self.textedit = QTextEdit()

        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(self.textedit)
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

    def equationsLayout(self):
        vbox = QVBoxLayout()

        myQListWidget = QtGui.QListWidget(self)     
        for index, name in [
            ('Equation 1', 'x + y = 2'),
            ('Equation 2', 'x^2 + x = 5'),
            ('Equation 3', 'x - y = 3')]:
            # Create QCustomQWidget
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setTextUp(index)
            myQCustomQWidget.setTextDown(name)
            #myQCustomQWidget.setIcon(icon)
            # Create QListWidgetItem
            myQListWidgetItem = QtGui.QListWidgetItem(myQListWidget)
            # Set size hint
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            # Add QListWidgetItem into QListWidget
            myQListWidget.addItem(myQListWidgetItem)
            myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
        
        #Resize width and height
        myQListWidget.resize(400,300)
        
        #myQListWidget.itemClicked.connect(myQListWidget.Clicked)  
        vbox.addWidget(myQListWidget)
        return vbox

    def buttonsLayout(self):
        vbox = QVBoxLayout()

        blank = QFrame()

        topButtonSplitter = QSplitter(Qt.Horizontal)
        topButtonSplitter.addWidget(blank)
        permanentButtons = QWidget(self)
        documentButtonsLayout = QHBoxLayout()
        newButton = PicButton(QPixmap("resources/new.png"))
        saveButton = PicButton(QPixmap("resources/save.png"))
        newButton.setToolTip('Add New Equation')
        saveButton.setToolTip('Save Equation')
        documentButtonsLayout.addWidget(newButton)
        documentButtonsLayout.addWidget(saveButton)

        permanentButtons.setLayout(documentButtonsLayout)
        topButtonSplitter.addWidget(permanentButtons)
        topButtonSplitter.setSizes([10000, 2])

        bottomButton = QFrame()
        buttonSplitter = QSplitter(Qt.Vertical)
        buttonSplitter.addWidget(topButtonSplitter)
        buttonSplitter.addWidget(bottomButton)
        buttonSplitter.setSizes([01, 1000])
        vbox.addWidget(buttonSplitter)
        return vbox

    def inputsLayout(self, loadList="Greek"):
        inputLayout = QHBoxLayout(self)
        blank = QFrame()
        
        comboLabel = QtGui.QLabel()
        comboLabel.setText("Input Type:")

        combo = QtGui.QComboBox(self)
        combo.addItem("LaTeX")
        combo.addItem("Greek")
        combo.resize(10, 10)
        combo.activated[str].connect(self.onActivated)
        
        inputTypeSplitter = QSplitter(Qt.Horizontal)
        inputTypeSplitter.addWidget(comboLabel)
        inputTypeSplitter.addWidget(combo)

        topSplitter = QSplitter(Qt.Horizontal)
        topSplitter.addWidget(blank)
        topSplitter.addWidget(inputTypeSplitter)
        inputSplitter = QSplitter(Qt.Vertical)
        inputWidget = QWidget()
        self.selectedCombo = str(loadList)
        for i in range(10):
            for j in range(3):
                if str(loadList) in "Greek":
                    if (i*3 + j) < len(self.inputGreek):
                        self.buttons[(i, j)] = QtGui.QPushButton(self.inputGreek[i * 3 + j])
                        self.buttons[(i, j)].resize(100, 100)
                        self.buttons[(i, j)].clicked.connect(self.onInput(self.inputGreek[i * 3 + j]))
                        self.inputBox.addWidget(self.buttons[(i, j)], i, j)
                elif str(loadList) in "LaTeX":
                    if (i*3 + j) < len(self.inputLaTeX):
                        self.buttons[(i, j)] = QtGui.QPushButton(self.inputLaTeX[i * 3 + j])
                        self.buttons[(i, j)].resize(100, 100)
                        self.buttons[(i, j)].clicked.connect(self.onInput(self.inputLaTeX[i * 3 + j]))
                        self.inputBox.addWidget(self.buttons[(i, j)], i, j)
        inputWidget.setLayout(self.inputBox)
        inputSplitter.addWidget(topSplitter)
        inputSplitter.addWidget(inputWidget)
        inputSplitter.setSizes([10, 1000])
        inputLayout.addWidget(inputSplitter)
        return inputLayout
    
    def onActivated(self, text):
        for i in range(10):
            for j in range(3):
                if self.selectedCombo == "Greek":
                    if (i*3 + j) < len(self.inputGreek):
                        self.inputBox.removeWidget(self.buttons[(i, j)])
                elif self.selectedCombo == "LaTeX":
                    if (i * 3 + j) < len(self.inputLaTeX):
                        self.inputBox.removeWidget(self.buttons[(i, j)])

        for i in range(10):
            for j in range(3):
                if str(text) in "Greek":
                    if (i*3 + j) < len(self.inputGreek):
                        self.buttons[(i, j)] = QtGui.QPushButton(self.inputGreek[i * 3 + j])
                        self.buttons[(i, j)].resize(100, 100)
                        self.buttons[(i, j)].clicked.connect(self.onInput(self.inputGreek[i * 3 + j]))
                        self.inputBox.addWidget(self.buttons[(i, j)], i, j)
                elif str(text) in "LaTeX":
                    if (i*3 + j) < len(self.inputLaTeX):
                        self.buttons[(i, j)] = QtGui.QPushButton(self.inputLaTeX[i * 3 + j])
                        self.buttons[(i, j)].resize(100, 100)
                        self.buttons[(i, j)].clicked.connect(self.onInput(self.inputLaTeX[i * 3 + j]))
                        self.inputBox.addWidget(self.buttons[(i, j)], i, j)
        self.selectedCombo = str(text)

    def onInput(self, name):
        self.textedit.append(name + " ")


class QCustomQWidget (QtGui.QWidget):
    def __init__ (self, parent = None):
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QtGui.QVBoxLayout()
        self.textUpQLabel    = QtGui.QLabel()
        self.textDownQLabel  = QtGui.QLabel()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout  = QtGui.QHBoxLayout()
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        self.textUpQLabel.setStyleSheet('''
            color: rgb(0, 0, 255);
        ''')
        self.textDownQLabel.setStyleSheet('''
            color: rgb(255, 0, 0);
        ''')

    def setTextUp (self, text):
        self.textUpQLabel.setText(text)

    def setTextDown (self, text):
        self.textDownQLabel.setText(text)

    def Clicked(self,item):
        QMessageBox.information(self, "ListWidget", "You clicked: "+item.text())     


class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super(PicButton, self).__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()

def main():
    app = QApplication(sys.argv)
    ex = Window()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()