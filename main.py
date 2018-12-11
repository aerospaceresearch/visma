from visma.gui.window import initGUI
# from visma.gui.cli import commandExec


from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QTextEdit, QSplitter, QFrame, QAbstractButton
from PyQt5.QtCore import Qt
from PyQt5 import QtGui, QtWidgets

from visma.calculus.differentiation import differentiate
from visma.calculus.integration import integrate
from visma.io.checks import checkTypes, getVariables
from visma.io.tokenize import tokenizer, getLHSandRHS
from visma.io.parser import resultLatex
from visma.gui.plotter import plotFigure2D, plotFigure3D, plot
from visma.gui.qsolver import quickSimplify, qSolveFigure, showQSolve
from visma.gui.settings import preferenceLayout
from visma.gui.steps import stepsFigure, showSteps
from visma.simplify.simplify import simplify, simplifyEquation
from visma.simplify.addsub import addition, additionEquation, subtraction, subtractionEquation
from visma.simplify.muldiv import multiplication, multiplicationEquation, division, divisionEquation
from visma.solvers.solve import solveFor
from visma.solvers.polynomial.roots import quadraticRoots
from visma.transform.factorization import factorize


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        font = QtGui.QFont()
        font.setPointSize(12)
        self.setFont(font)

    def initUI(self):
        exitAction = QtWidgets.QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        wikiAction = QtWidgets.QAction('Wiki', self)
        wikiAction.setStatusTip('Open Github wiki')
        # TODO: Pop a mini browser for docs and wiki
        wikiAction.triggered.connect(lambda: webbrowser.open('https://github.com/aerospaceresearch/visma/wiki'))

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        # TODO: Add function for adding custom equation lists
        # fileMenu.addAction(addEqList)
        # configMenu = menubar.addMenu('&Config')

        helpMenu = menubar.addMenu('&Help')
        helpMenu.addAction(wikiAction)
        self.workSpace = WorkSpace()
        self.setCentralWidget(self.workSpace)
        self.GUIwidth = 1300
        self.GUIheight = 900
        self.setGeometry(300, 300, self.GUIwidth, self.GUIheight)
        self.setWindowTitle('VISual MAth')
        self.show()


class WorkSpace(QWidget):

    inputGreek = ['x', 'y', 'z', '(', ')', '7', '8', '9', 'DEL', 'C', 'f', 'g', 'h', '{', '}', '4', '5', '6', '/', '*', 'sin', 'cos', 'tan', '[', ']', '1', '2', '3', '+', '-', 'log', 'exp', '^', 'i', u'\u03C0', '.', '0', '=', '<', '>']
    inputLaTeX = ['x', 'y', 'z', '(', ')', '7', '8', '9', 'DEL', 'C', 'f', 'g',  'h', '{', '}', '4', '5', '6', '\\div', '\\times', '\\sin', '\\cos', '\\tan', '[', ']', '1', '2', '3', '+', '-', 'log', 'exp', '^', 'i', '\\pi', '.', '0', '=', '<', '>']

    mode = 'interaction'
    showQuickSim = True
    showStepByStep = True
    showPlotter = False
    enableQSolver = True
    buttons = {}
    solutionOptionsBox = QGridLayout()
    solutionButtons = {}
    inputBox = QGridLayout()
    selectedCombo = "Greek"
    equations = []
    stepsFontSize = 1
    axisRange = [10, 10, 10, 30]  # axisRange[-1] --> MeshDensity in 3D graphs
    resultOut = False

    try:
        with open('local/eqn-list.vis', 'r+') as fp:
            for line in fp:
                if not line.isspace():
                    fp.write(line)
                    equations.insert(
                        0, ('Equation No.' + str(len(equations) + 1), line))
            fp.close()
    except IOError:
        if not os.path.exists('local'):
            os.mkdir('local')
        file = open('local/eqn-list.vis', 'w')
        file.close()

    if len(equations) == 0:
        equations = [('No equations stored', '')]

    equationListVbox = QVBoxLayout()
    tokens = []
    lTokens = []
    rTokens = []
    buttonSet = False
    solutionType = ""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout(self)

        self.equationList = QTabWidget()
        self.equationList.tab1 = QWidget()
        # self.equationList.tab2 = QWidget()
        self.equationList.addTab(self.equationList.tab1, "History")
        # self.equationList.addTab(self.equationList.tab2, "favourites")
        self.equationList.tab1.setLayout(self.equationsLayout())
        self.equationList.tab1.setStatusTip("Track of old equations")
        self.equationList.setFixedWidth(300)

        inputSpace = QTabWidget()
        inputSpace.tab1 = QWidget()
        inputSpace.tab2 = QWidget()
        inputSpace.addTab(inputSpace.tab1, "Input")
        inputSpace.addTab(inputSpace.tab2, "Settings")
        inputSpace.tab1.setLayout(self.inputsLayout())
        inputSpace.tab2.setLayout(preferenceLayout(self))
        inputSpace.tab1.setStatusTip("Input characters")
        inputSpace.setFixedHeight(200)

        buttonSpace = QWidget()
        buttonSpace.setLayout(self.buttonsLayout())
        buttonSpace.setFixedWidth(300)
        buttonSpace.setStatusTip("Interact")

        self.tabPlot = QTabWidget()
        self.tabPlot.tab1 = QWidget()
        self.tabPlot.tab2 = QWidget()
        self.tabPlot.addTab(self.tabPlot.tab1, "2D-plot")
        self.tabPlot.addTab(self.tabPlot.tab2, "3D-plot")
        self.tabPlot.tab1.setLayout(plotFigure2D(self))
        self.tabPlot.tab1.setStatusTip("Visualize equation in 2D")
        self.tabPlot.tab2.setLayout(plotFigure3D(self))
        self.tabPlot.tab2.setStatusTip("Visualize equation in 3D")

        tabStepsLogs = QTabWidget()
        tabStepsLogs.tab1 = QWidget()
        tabStepsLogs.tab2 = QWidget()
        tabStepsLogs.addTab(tabStepsLogs.tab1, "Step-by-Step")
        # tabStepsLogs.addTab(tabStepsLogs.tab2, "logger")
        tabStepsLogs.tab1.setLayout(stepsFigure(self))
        tabStepsLogs.tab1.setStatusTip("Step-by-step solver")
        # tabStepsLogs.tab2.setStatusTip("Logger")

        font = QtGui.QFont()
        font.setPointSize(16)
        self.textedit = QTextEdit()

        self.textedit.setFont(font)
        self.textedit.textChanged.connect(self.textChangeTrigger)
        self.textedit.setFixedHeight(60)
        self.textedit.setStatusTip("Input equation")

        quickSolve = QWidget()
        quickSolve.setLayout(qSolveFigure(self))
        quickSolve.setFixedHeight(45)
        quickSolve.setStatusTip("Quick solver")

        splitter4 = QSplitter(Qt.Vertical)
        splitter4.addWidget(self.textedit)
        splitter4.addWidget(quickSolve)
        splitter4.addWidget(inputSpace)

        splitter3 = QSplitter(Qt.Horizontal)
        splitter3.addWidget(splitter4)
        splitter3.addWidget(buttonSpace)

        splitter2 = QSplitter(Qt.Horizontal)
        splitter2.addWidget(tabStepsLogs)
        splitter2.addWidget(self.tabPlot)
        splitter2.addWidget(self.equationList)

        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(splitter3)
        splitter1.addWidget(splitter2)

        hbox.addWidget(splitter1)
        self.setLayout(hbox)

    def textChangeTrigger(self):
        if self.textedit.toPlainText() == "":
            self.enableQSolver = True
        if self.enableQSolver and self.showQuickSim:
            self.qSol = quickSimplify(self)
            if self.qSol is None:
                self.qSol = ""
            showQSolve(self, self.showQuickSim)
        elif self.showQuickSim is False:
            self.qSol = ""
            showQSolve(self, self.showQuickSim)

    def clearAll(self):
        self.textedit.clear()
        self.eqToks = [[]]
        self.output = ""
        showSteps(self)
        plot(self)

    def equationsLayout(self):
        self.myQListWidget = QtWidgets.QListWidget(self)
        for index, name in self.equations:
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setTextUp(index)
            myQCustomQWidget.setTextDown(name)
            myQListWidgetItem = QtWidgets.QListWidgetItem(self.myQListWidget)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(
                myQListWidgetItem, myQCustomQWidget)
        self.myQListWidget.resize(400, 300)
        self.equationListVbox.addWidget(self.myQListWidget)
        self.myQListWidget.itemClicked.connect(self.Clicked)
        self.clearButton = QtWidgets.QPushButton('Clear equations')
        self.clearButton.clicked.connect(self.clearHistory)
        self.clearButton.setStatusTip("Restart UI for clearing history")
        # FIXME: Clear button. Clear rightaway.
        self.equationListVbox.addWidget(self.clearButton)
        return self.equationListVbox

    def clearHistory(self):
        file = open('local/eqn-list.vis', 'w')
        file.truncate()
        file.close()

    def Clicked(self, item):
        _, name = self.equations[self.myQListWidget.currentRow()]
        self.textedit.setText(name)

    def buttonsLayout(self):
        vbox = QVBoxLayout()
        interactionModeLayout = QVBoxLayout()
        interactionModeButton = QtWidgets.QPushButton('visma')
        interactionModeButton.clicked.connect(self.interactionMode)
        interactionModeLayout.addWidget(interactionModeButton)
        interactionModeWidget = QWidget(self)
        interactionModeWidget.setLayout(interactionModeLayout)
        interactionModeWidget.setFixedSize(275, 50)
        topButtonSplitter = QSplitter(Qt.Horizontal)
        topButtonSplitter.addWidget(interactionModeWidget)
        permanentButtons = QWidget(self)
        """
        documentButtonsLayout = QHBoxLayout()
        newButton = PicButton(QPixmap("assets/new.png"))
        saveButton = PicButton(QPixmap("assets/save.png"))
        newButton.setToolTip('Add New Equation')
        saveButton.setToolTip('Save Equation')
        documentButtonsLayout.addWidget(newButton)
        documentButtonsLayout.addWidget(saveButton)
        newButton.clicked.connect(self.newEquation)
        saveButton.clicked.connect(self.saveEquation)
        permanentButtons.setLayout(documentButtonsLayout)
        """
        topButtonSplitter.addWidget(permanentButtons)
        self.bottomButton = QFrame()
        self.buttonSplitter = QSplitter(Qt.Vertical)
        self.buttonSplitter.addWidget(topButtonSplitter)
        self.buttonSplitter.addWidget(self.bottomButton)
        vbox.addWidget(self.buttonSplitter)
        return vbox

    def interactionMode(self):
        self.enableQSolver = False
        showQSolve(self, self.enableQSolver)
        cursor = self.textedit.textCursor()
        interactionText = cursor.selectedText()
        if str(interactionText) == '':
            self.mode = 'normal'
            self.input = str(self.textedit.toPlainText())

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
