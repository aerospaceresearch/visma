"""
Initial Author: Siddharth Kothiyal (sidkothiyal, https://github.com/sidkothiyal)
Other Authors:
Owner: AerospaceResearch.net
About: This module is created to handle the GUI of the project, this module interacts with solve initially to check for all the available functions, and then according	to the event selected by the user, it interacts with solve, or polynomial roots module.
Invokes animator module as a seperate subprocess using Popen, and passes the equations/expressions to be animated and comments which go along with them in the json format as arguments.
Note: Please try to maintain proper documentation
Logic Description:
"""

import sys
import os
from PyQt4.QtGui import QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QTextEdit, QSplitter, QLabel, QFrame, QApplication, QAbstractButton, qApp, QPainter
from PyQt4.QtCore import Qt
from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from visma.calculus.differentiation import differentiate
from visma.calculus.integration import integrate
from visma.io.checks import checkTypes, find_wrt_variable
from visma.io.tokenize import tokenizer, get_lhs_rhs
from visma.io.parser import resultLatex
from visma.gui.plotter import plotThis
import visma.solvers.polynomial.roots as ViSoPoRo
from visma.simplify.simplify import simplify, simplify_equation
from visma.simplify.addsub import addition, addition_equation, subtraction, subtraction_equation
from visma.simplify.muldiv import multiplication, multiplication_equation, division, division_equation

# from visma.gui.plotter import plotthis

# TODO: Revamp GUI


class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.initUI()

    def initUI(self):
        # exitAction = QtGui.QAction(QtGui.QIcon('assets/exit.png'), 'Exit', self)
        exitAction = QtGui.QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        # TODO: Add function for adding custom equation lists
        # fileMenu.addAction(addEqList)
        configMenu = menubar.addMenu('&Config')
        #
        helpMenu = menubar.addMenu('&Help')
        #
        workSpace = WorkSpace()
        self.setCentralWidget(workSpace)
        self.setGeometry(300, 300, 1280, 720)
        self.setWindowTitle('VisMa - Visual Math')
        self.show()


class WorkSpace(QWidget):

    inputLaTeX = ['x', 'y', 'z', '(', ')', '7', '8', '9', 'DEL', 'C', '\\alpha', '\\beta',  '\\gamma', '{', '}', '4', '5', '6', '\\div', '\\times', '\\sin', '\\cos', '\\tan', '[', ']', '1', '2', '3', '+', '-', 'log', 'e', '^', 'i', '\\pi', '.', '0', '=', '<', '>']
    inputGreek = ['x', 'y', 'z', '(', ')', '7', '8', '9', 'DEL', 'C', u'\u03B1', u'\u03B2', u'\u03B3', '{', '}', '4', '5', '6', '/', '*', 'sin', 'cos', 'tan', '[', ']', '1', '2', '3', '+', '-', 'log', 'e', '^', 'i', u'\u03C0', '.', '0', '=', '<', '>']

    mode = 'interaction'
    buttons = {}
    solutionOptionsBox = QGridLayout()
    solutionButtons = {}
    inputBox = QGridLayout()
    selectedCombo = "Greek"
    equations = []

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
        super(WorkSpace, self).__init__()
        self.initUI()

    def initUI(self):
        hbox = QHBoxLayout(self)

        equationList = QWidget()
        equationList.setLayout(self.equationsLayout())
        equationList.setStatusTip("Track of old equations")
        equationList.setFixedWidth(300)

        inputList = QWidget()
        inputList.setLayout(self.inputsLayout())
        inputList.setStatusTip("Input characters")
        inputList.setFixedHeight(200)

        buttonSpace = QWidget()
        buttonSpace.setLayout(self.buttonsLayout())
        buttonSpace.setFixedWidth(300)
        buttonSpace.setStatusTip("Interact")

        plotFig = QWidget()
        plotFig.setLayout(self.plotFigure())
        plotFig.setStatusTip("Graph plot")

        stepsFig = QWidget()
        stepsFig.setLayout(self.stepsFigure())
        stepsFig.setStatusTip("Step-by-step solver")

        self.textedit = QTextEdit()
        self.textedit.textChanged.connect(self.textChangeTrigger)
        self.textedit.setFixedHeight(70)
        self.textedit.setStatusTip("Input equation")

        splitter4 = QSplitter(Qt.Vertical)
        splitter4.addWidget(self.textedit)
        splitter4.addWidget(inputList)

        splitter3 = QSplitter(Qt.Horizontal)
        splitter3.addWidget(splitter4)
        splitter3.addWidget(buttonSpace)

        splitter2 = QSplitter(Qt.Horizontal)
        splitter2.addWidget(stepsFig)
        splitter2.addWidget(plotFig)
        splitter2.addWidget(equationList)

        splitter1 = QSplitter(Qt.Vertical)
        splitter1.addWidget(splitter3)
        splitter1.addWidget(splitter2)

        hbox.addWidget(splitter1)
        self.setLayout(hbox)

    def textChangeTrigger(self):
        pass
        # print self.textedit.toPlainText()

    def equationsLayout(self):
        self.myQListWidget = QtGui.QListWidget(self)
        for index, name in self.equations:
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setTextUp(index)
            myQCustomQWidget.setTextDown(name)
            myQListWidgetItem = QtGui.QListWidgetItem(self.myQListWidget)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(
                myQListWidgetItem, myQCustomQWidget)
        self.myQListWidget.resize(400, 300)
        self.myQListWidget.itemClicked.connect(self.Clicked)
        self.equationListVbox.addWidget(QLabel("<h3>Equation History</h3>"))
        self.equationListVbox.addWidget(self.myQListWidget)
        return self.equationListVbox

    def plotFigure(self):
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        class NavigationCustomToolbar(NavigationToolbar):
            toolitems = [t for t in NavigationToolbar.toolitems if t[0] in ('Home', 'Pan', 'Zoom', 'Save')]

        # self.toolbar = NavigationCustomToolbar(self.canvas, self)
        self.button = QtGui.QPushButton('Plot')
        self.button.clicked.connect(self.plot)
        layout = QtGui.QVBoxLayout()
        layout.addWidget(QLabel("<h3>Plotter</h3>"))
        layout.addWidget(self.canvas)
        # layout.addWidget(self.toolbar)
        layout.addWidget(self.button)
        return layout

    def plot(self):
        ax = self.figure.add_subplot(111)
        ax.clear()
        x, y, LHS, RHS = plotThis(equationTokens[-1])
        ax.contour(x, y, (LHS - RHS), [0])
        ax.grid()
        self.canvas.draw()

    def stepsFigure(self):
        self.stpsfigure = Figure()
        self.stpscanvas = FigureCanvas(self.stpsfigure)
        self.stpsfigure.clear()
        self.stpsbutton = QtGui.QPushButton('Show steps')
        self.stpsbutton.clicked.connect(self.showSteps)

        stpslayout = QtGui.QVBoxLayout()
        stpslayout.addWidget(QLabel("<h3>Step-by-step solution</h3>"))
        stpslayout.addWidget(self.stpscanvas)
        stpslayout.addWidget(self.stpsbutton)
        return stpslayout

    def showSteps(self):
        text = self.stpsfigure.suptitle(theResult,
                                        x=0.0, y=1.0,
                                        horizontalalignment='left',
                                        verticalalignment='top',
                                        size=qApp.font().pointSize()*1.5)
        self.stpscanvas.draw()

    def Clicked(self, item):
        index, name = self.equations[self.myQListWidget.currentRow()]
        self.textedit.setText(name)

    def buttonsLayout(self):
        vbox = QVBoxLayout()

        interactionModeLayout = QVBoxLayout()
        vismaButton = QtGui.QPushButton('VisMa')
        interactionModeButton = vismaButton

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
        cursor = self.textedit.textCursor()
        interactionText = cursor.selectedText()
        if str(interactionText) == '':
            self.mode = 'normal'
            textSelected = str(self.textedit.toPlainText())
        else:
            textSelected = str(interactionText)
            self.mode = 'interaction'
        self.tokens = tokenizer(textSelected)
        # DBP: print self.tokens
        self.addEquation()
        lhs, rhs = get_lhs_rhs(self.tokens)
        self.lTokens = lhs
        self.rTokens = rhs
        operations, self.solutionType = checkTypes(
            lhs, rhs)
        if isinstance(operations, list):
            opButtons = []
            if len(operations) > 0:
                if len(operations) == 1:
                    if operations[0] != 'solve':
                        opButtons = ['Simplify']
                else:
                    opButtons = ['Simplify']
            for operation in operations:
                if operation == '+':
                    opButtons.append("Addition")
                elif operation == '-':
                    opButtons.append("Subtraction")
                elif operation == '*':
                    opButtons.append("Multiplication")
                elif operation == '/':
                    opButtons.append("Division")
                elif operation == 'solve':
                    opButtons.append("Solve For")
                elif operation == 'find roots':
                    opButtons.append("Find Roots")
                elif operation == 'integrate':
                    opButtons.append("Integrate")
                elif operation == 'differentiate':
                    opButtons.append("Differentiate")

            if self.buttonSet:
                for i in reversed(xrange(self.solutionOptionsBox.count())):
                    self.solutionOptionsBox.itemAt(i).widget().setParent(None)
                for i in xrange(int(len(opButtons) / 2) + 1):
                    for j in xrange(2):
                        if len(opButtons) > (i * 2 + j):
                            self.solutionButtons[(i, j)] = QtGui.QPushButton(
                                opButtons[i * 2 + j])
                            self.solutionButtons[(i, j)].resize(100, 100)
                            self.solutionButtons[(i, j)].clicked.connect(
                                self.onSolvePress(opButtons[i * 2 + j]))
                            self.solutionOptionsBox.addWidget(
                                self.solutionButtons[(i, j)], i, j)
            else:
                self.bottomButton.setParent(None)
                self.solutionWidget = QWidget()
                for i in xrange(int(len(opButtons) / 2) + 1):
                    for j in xrange(2):
                        if len(opButtons) > (i * 2 + j):
                            self.solutionButtons[(i, j)] = QtGui.QPushButton(
                                opButtons[i * 2 + j])
                            self.solutionButtons[(i, j)].resize(100, 100)
                            self.solutionButtons[(i, j)].clicked.connect(
                                self.onSolvePress(opButtons[i * 2 + j]))
                            self.solutionOptionsBox.addWidget(
                                self.solutionButtons[(i, j)], i, j)
                self.solutionWidget.setLayout(self.solutionOptionsBox)
                self.buttonSplitter.addWidget(self.solutionWidget)
                self.buttonSet = True

    def refreshButtons(self, operations):
        if isinstance(operations, list):
            opButtons = []
            if len(operations) > 0:
                if len(operations) == 1:
                    if operations[0] != 'solve':
                        opButtons = ['Simplify']
                else:
                    opButtons = ['Simplify']
            for operation in operations:
                if operation == '+':
                    opButtons.append("Addition")
                elif operation == '-':
                    opButtons.append("Subtraction")
                elif operation == '*':
                    opButtons.append("Multiplication")
                elif operation == '/':
                    opButtons.append("Division")
                elif operation == 'solve':
                    opButtons.append("Solve For")
                elif operations == 'find roots':
                    opButtons.append("Find Roots")
                elif operation == 'integrate':
                    opButtons.append("Integrate")
                elif operation == 'differentiate':
                    opButtons.append("Differentiate")
            for i in reversed(xrange(self.solutionOptionsBox.count())):
                self.solutionOptionsBox.itemAt(i).widget().setParent(None)
            for i in xrange(int(len(opButtons) / 2) + 1):
                for j in xrange(2):
                    if len(opButtons) > (i * 2 + j):
                        self.solutionButtons[(i, j)] = QtGui.QPushButton(
                            opButtons[i * 2 + j])
                        self.solutionButtons[(i, j)].resize(100, 100)
                        self.solutionButtons[(i, j)].clicked.connect(
                            self.onSolvePress(opButtons[i * 2 + j]))
                        self.solutionOptionsBox.addWidget(
                            self.solutionButtons[(i, j)], i, j)

    def clearButtons(self):
        for i in reversed(xrange(self.solutionOptionsBox.count())):
            self.solutionOptionsBox.itemAt(i).widget().setParent(None)

    def wrtVariableButtons(self, variables, operation):
        if isinstance(variables, list):
            varButtons = []
            if len(variables) > 0:
                for variable in variables:
                    varButtons.append(variable)
                varButtons.append("Back")
                for i in reversed(xrange(self.solutionOptionsBox.count())):
                    self.solutionOptionsBox.itemAt(i).widget().setParent(None)
                for i in xrange(int(len(varButtons) / 2) + 1):
                    for j in xrange(2):
                        if len(varButtons) > (i * 2 + j):
                            self.solutionButtons[(i, j)] = QtGui.QPushButton(
                                varButtons[i * 2 + j])
                            self.solutionButtons[(i, j)].resize(100, 100)
                            self.solutionButtons[(i, j)].clicked.connect(
                                self.onWRTVariablePress(varButtons[i * 2 + j], operation))
                            self.solutionOptionsBox.addWidget(
                                self.solutionButtons[(i, j)], i, j)

    def newEquation(self):
        self.textedit.setText("")

    def saveEquation(self):
        for i in reversed(xrange(self.equationListVbox.count())):
            self.equationListVbox.itemAt(i).widget().setParent(None)

        eqn = unicode(self.textedit.toPlainText())
        if len(self.equations) == 1:
            index, name = self.equations[0]
            if index == "No equations stored":
                self.equations[0] = ("Equation No. 1", eqn)
            else:
                self.equations.append(("Equation No. 2", eqn))
        else:
            self.equations.append(
                ("Equation No. " + str(len(self.equations) + 1), eqn))

        self.textedit.setText('')
        file = open('local/eqn-list.vis', 'r+')
        self.myQListWidget = QtGui.QListWidget(self)
        i = 0
        for index, name in self.equations:
            if i != 0:
                file.write("\n")
            file.write(name)
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setTextUp(index)
            myQCustomQWidget.setTextDown(name)
            myQListWidgetItem = QtGui.QListWidgetItem(self.myQListWidget)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(
                myQListWidgetItem, myQCustomQWidget)
            i += 1
        file.close()
        self.myQListWidget.resize(400, 300)

        self.myQListWidget.itemClicked.connect(self.Clicked)
        self.equationListVbox.addWidget(self.myQListWidget)
        return self.equationListVbox

    def addEquation(self):
        eqn = unicode(self.textedit.toPlainText())
        for index, equation in self.equations:
            if equation == eqn:
                return self.equationListVbox

        for i in reversed(xrange(self.equationListVbox.count())):
            self.equationListVbox.itemAt(i).widget().setParent(None)

        if len(self.equations) == 1:
            index, name = self.equations[0]
            if index == "No equations stored":
                self.equations[0] = ("Equation No. 1", eqn)
            else:
                self.equations.append(("Equation No. 2", eqn))
        else:
            self.equations.append(
                ("Equation No. " + str(len(self.equations) + 1), eqn))
        file = open('local/eqn-list.vis', 'r+')
        self.myQListWidget = QtGui.QListWidget(self)
        i = 0
        for index, name in self.equations:
            if i != 0:
                file.write("\n")
            file.write(name)
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setTextUp(index)
            myQCustomQWidget.setTextDown(name)
            myQListWidgetItem = QtGui.QListWidgetItem(self.myQListWidget)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(
                myQListWidgetItem, myQCustomQWidget)
            i += 1
        file.close()
        self.myQListWidget.resize(400, 300)

        self.myQListWidget.itemClicked.connect(self.Clicked)
        self.equationListVbox.addWidget(QLabel("<h3>Equation History</h3>"))
        self.equationListVbox.addWidget(self.myQListWidget)
        return self.equationListVbox

    def inputsLayout(self, loadList="Greek"):
        inputLayout = QHBoxLayout(self)
        blank = QFrame()

        comboLabel = QtGui.QLabel()
        comboLabel.setText("Input Type:")
        comboLabel.setFixedSize(100, 30)

        combo = QtGui.QComboBox(self)
        combo.addItem("Greek")
        combo.addItem("LaTeX")
        combo.setFixedSize(100, 30)
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
        for i in xrange(4):
            for j in xrange(10):
                if str(loadList) in "Greek":
                    if (i * 10 + j) < len(self.inputGreek):
                        self.buttons[(i, j)] = QtGui.QPushButton(
                            self.inputGreek[i * 10 + j])
                        self.buttons[(i, j)].resize(100, 100)
                        self.buttons[(i, j)].clicked.connect(
                            self.onInputPress(self.inputGreek[i * 10 + j]))
                        self.inputBox.addWidget(self.buttons[(i, j)], i, j)
                elif str(loadList) in "LaTeX":
                    if (i * 10 + j) < len(self.inputLaTeX):
                        self.buttons[(i, j)] = QtGui.QPushButton(
                            self.inputLaTeX[i * 10 + j])
                        self.buttons[(i, j)].resize(100, 100)
                        self.buttons[(i, j)].clicked.connect(
                            self.onInputPress(self.inputLaTeX[i * 10 + j]))
                        # (self.inputLaTeX[i * 3 + j])
                        self.inputBox.addWidget(self.buttons[(i, j)], i, j)
        inputWidget.setLayout(self.inputBox)
        inputSplitter.addWidget(topSplitter)
        inputSplitter.addWidget(inputWidget)
        inputLayout.addWidget(inputSplitter)
        return inputLayout

    def onActivated(self, text):
        for i in reversed(xrange(self.inputBox.count())):
            self.inputBox.itemAt(i).widget().setParent(None)

        for i in xrange(4):
            for j in xrange(10):
                if str(text) in "Greek":
                    if (i * 10 + j) < len(self.inputGreek):
                        self.buttons[(i, j)] = QtGui.QPushButton(
                            self.inputGreek[i * 10 + j])
                        self.buttons[(i, j)].resize(100, 100)
                        self.buttons[(i, j)].clicked.connect(
                            self.onInputPress(self.inputGreek[i * 10 + j]))
                        self.inputBox.addWidget(self.buttons[(i, j)], i, j)
                elif str(text) in "LaTeX":
                    if (i * 10 + j) < len(self.inputLaTeX):
                        self.buttons[(i, j)] = QtGui.QPushButton(
                            self.inputLaTeX[i * 10 + j])
                        self.buttons[(i, j)].resize(100, 100)
                        self.buttons[(i, j)].clicked.connect(
                            self.onInputPress(self.inputLaTeX[i * 10 + j]))
                        self.inputBox.addWidget(self.buttons[(i, j)], i, j)
        self.selectedCombo = str(text)

    def onInputPress(self, name):
        def calluser():
            self.textedit.insertPlainText(unicode(name) + " ")
        return calluser

    def onSolvePress(self, name):
        def calluser():
            availableOperations = []
            token_string = ''
            global equationTokens
            equationTokens = []
            resultOut = True
            if name == 'Addition':
                if self.solutionType == 'expression':
                    self.tokens, availableOperations, token_string, equationTokens, comments = addition(
                        self.tokens, True)
                else:
                    self.lTokens, self.rTokens, availableOperations, token_string, equationTokens, comments = addition_equation(
                        self.lTokens, self.rTokens, True)
            elif name == 'Subtraction':
                if self.solutionType == 'expression':
                    self.tokens, availableOperations, token_string, equationTokens, comments = subtraction(
                        self.tokens, True)
                else:
                    self.lTokens, self.rTokens, availableOperations, token_string, equationTokens, comments = subtraction_equation(
                        self.lTokens, self.rTokens, True)
            elif name == 'Multiplication':
                if self.solutionType == 'expression':
                    self.tokens, availableOperations, token_string, equationTokens, comments = multiplication(
                        self.tokens, True)
                else:
                    self.lTokens, self.rTokens, availableOperations, token_string, equationTokens, comments = multiplication_equation(
                        self.lTokens, self.rTokens, True)
            elif name == 'Division':
                if self.solutionType == 'expression':
                    self.tokens, availableOperations, token_string, equationTokens, comments = division(
                        self.tokens, True)
                else:
                    self.lTokens, self.rTokens, availableOperations, token_string, equationTokens, comments = division_equation(
                        self.lTokens, self.rTokens, True)
            elif name == 'Simplify':
                if self.solutionType == 'expression':
                    self.tokens, availableOperations, token_string, equationTokens, comments = simplify(self.tokens)
                else:
                    self.lTokens, self.rTokens, availableOperations, token_string, equationTokens, comments = simplify_equation(self.lTokens, self.rTokens)
            elif name == 'Solve For':
                lhs, rhs = get_lhs_rhs(self.tokens)
                variables = find_wrt_variable(lhs, rhs)
                self.wrtVariableButtons(variables, name)
                resultOut = False
            elif name == 'Find Roots':
                self.lTokens, self.rTokens, availableOperations, token_string, equationTokens, comments = ViSoPoRo.quadratic_roots(self.lTokens, self.rTokens)
            elif name == 'Integrate':
                lhs, rhs = get_lhs_rhs(self.tokens)
                variables = find_wrt_variable(lhs, rhs)
                self.wrtVariableButtons(variables, name)
                resultOut = False
            elif name == 'Differentiate':
                lhs, rhs = get_lhs_rhs(self.tokens)
                variables = find_wrt_variable(lhs, rhs)
                self.wrtVariableButtons(variables, name)
                resultOut = False
            # Popen(['python', 'visma/gui/animator.py', json.dumps(equationTokens, default=lambda o: o.__dict__), json.dumps(comments)])
            # finalSteps = tokensToLatex(name, equationTokens, comments)
            if resultOut:
                global theResult
                theResult = resultLatex(name, equationTokens, comments)
                if len(availableOperations) == 0:
                    self.clearButtons()
                else:
                    self.refreshButtons(availableOperations)
                if self.mode == 'normal':
                    self.textedit.setText(token_string)
                elif self.mode == 'interaction':
                    cursor = self.textedit.textCursor()
                    cursor.insertText(token_string)
        return calluser

    def onWRTVariablePress(self, varName, operation):
        def calluser():
            availableOperations = []
            token_string = ''
            global equationTokens
            equationTokens = []
            if varName == 'Back':
                textSelected = str(self.textedit.toPlainText())
                self.tokens = tokenizer(textSelected)
                # print self.tokens
                lhs, rhs = get_lhs_rhs(self.tokens)
                operations, self.solutionType = checkTypes(
                    lhs, rhs)
                self.refreshButtons(operations)

            elif operation == 'Solve For':
                # self.lTokens, self.rTokens, availableOperations, token_string, equationTokens, comments = solveFor(self.lTokens, self.rTokens, varName)
                pass

            elif operation == 'Integrate':
                self.lTokens, availableOperations, token_string, equationTokens, comments = integrate(self.lTokens, varName)

            elif operation == 'Differentiate':
                self.lTokens, availableOperations, token_string, equationTokens, comments = differentiate(self.lTokens, varName)

            global theResult
            theResult = resultLatex(operation, equationTokens, comments)
            if len(availableOperations) == 0:
                self.clearButtons()
            else:
                self.refreshButtons(availableOperations)
            if self.mode == 'normal':
                self.textedit.setText(token_string)
            elif self.mode == 'interaction':
                cursor = self.textedit.textCursor()
                cursor.insertText(token_string)
        return calluser


class QCustomQWidget (QtGui.QWidget):

    def __init__(self, parent=None):
        super(QCustomQWidget, self).__init__(parent)
        self.textQVBoxLayout = QtGui.QVBoxLayout()
        self.textUpQLabel = QtGui.QLabel()
        self.textDownQLabel = QtGui.QLabel()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout = QtGui.QHBoxLayout()
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)
        # setStyleSheet
        self.textUpQLabel.setStyleSheet('''
        color: rgb(255, 0, 0);
        ''')
        self.textDownQLabel.setStyleSheet('''
        color: rgb(0, 0, 0);
        ''')

    def setTextUp(self, text):
        self.textUpQLabel.setText(text)

    def setTextDown(self, text):
        self.textDownQLabel.setText(text)


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
