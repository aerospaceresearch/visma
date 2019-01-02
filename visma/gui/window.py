"""
Initial Author: Siddharth Kothiyal (sidkothiyal, https://github.com/sidkothiyal)
Other Authors:
Owner: AerospaceResearch.net
About: This module is created to handle the GUI of the project, this module interacts with solve initially to check for all the available functions, and then according	to the event selected by the user, it interacts with solve, or polynomial roots module.
"""

import sys
import os

from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QTextEdit, QSplitter, QFrame, QAbstractButton, QDialog, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt, QUrl
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWebEngineWidgets import QWebEngineView

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
        wikiAction.triggered.connect(self.popupBrowser)

        addEqList = QtWidgets.QAction('Add Equations', self)
        addEqList.setStatusTip('Add custom equations')
        addEqList.triggered.connect(self.loadEquations)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(addEqList)
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

    def popupBrowser(self):
        w = QDialog(self)
        w.resize(600, 500)
        w.setWindowTitle('Wiki')
        web = QWebEngineView(w)
        web.load(QUrl('https://github.com/aerospaceresearch/visma/wiki'))
        web.resize(600, 500)
        web.show()
        w.show()

    def loadEquations(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Add Custom Equations", "", "All Files (*);;Visma Files (*.vis)", options=options)
        if os.path.getsize(fileName) == 0:
            return self.workSpace.warning("It's an empty file!")
        if self.workSpace.equations[0][0] == "No equations stored":
            self.workSpace.equations.pop(0)
        if fileName != '':
            with open(fileName) as fileobj:
                for line in fileobj:
                    self.workSpace.equations.insert(0, ('Equation No.' + str(len(self.workSpace.equations) + 1), line))
                self.workSpace.addEquation()


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
        self.clearButton.setStatusTip("Clear history")
        self.equationListVbox.addWidget(self.clearButton)
        return self.equationListVbox

    def clearHistory(self):
        file = open('local/eqn-list.vis', 'w')
        file.truncate()
        file.close()
        self.equations = []
        self.clearEquations()

    def clearEquations(self):
        eqn = str(self.textedit.toPlainText())
        for index, equation in self.equations:
            if equation == eqn:
                return self.equationListVbox

        for i in reversed(range(self.equationListVbox.count())):
            self.equationListVbox.itemAt(i).widget().setParent(None)

        self.equations = [('No equations stored', '')]

        file = open('local/eqn-list.vis', 'r+')
        self.myQListWidget = QtWidgets.QListWidget(self)
        i = 0
        for index, name in self.equations:
            if i != 0:
                file.write("\n")
            file.write(name)
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setTextUp(index)
            myQCustomQWidget.setTextDown(name)
            myQListWidgetItem = QtWidgets.QListWidgetItem(self.myQListWidget)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(
                myQListWidgetItem, myQCustomQWidget)
            i += 1
        file.close()
        self.myQListWidget.resize(400, 300)

        self.myQListWidget.itemClicked.connect(self.Clicked)
        self.equationListVbox.addWidget(self.myQListWidget)
        self.myQListWidget.itemClicked.connect(self.Clicked)
        self.clearButton = QtWidgets.QPushButton('Clear equations')
        self.clearButton.clicked.connect(self.clearHistory)
        self.equationListVbox.addWidget(self.clearButton)
        return self.equationListVbox

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
        else:
            self.input = str(interactionText)
            self.mode = 'interaction'
        showbuttons = True
        if len(self.input) == 0:
            self.input = '0'
            QMessageBox.warning(self, "Message", "No input given!")
            showbuttons = False
        self.tokens = tokenizer(self.input)
        # DBP: print(self.tokens)
        self.addEquation()
        lhs, rhs = getLHSandRHS(self.tokens)
        self.lTokens = lhs
        self.rTokens = rhs
        operations, self.solutionType = checkTypes(lhs, rhs)
        if isinstance(operations, list) and showbuttons:
            opButtons = []
            if len(operations) > 0:
                if len(operations) == 1:
                    if operations[0] not in ['integrate', 'differentiate', 'find roots', 'factorize']:
                        opButtons = ['simplify']
                else:
                    opButtons = ['simplify']
            for operation in operations:
                if operation == '+':
                    opButtons.append("addition")
                elif operation == '-':
                    opButtons.append("subtraction")
                elif operation == '*':
                    opButtons.append("multiplication")
                elif operation == '/':
                    opButtons.append("division")
                else:
                    opButtons.append(operation)

            if self.buttonSet:
                for i in reversed(range(self.solutionOptionsBox.count())):
                    self.solutionOptionsBox.itemAt(i).widget().setParent(None)
                for i in range(int(len(opButtons) / 2) + 1):
                    for j in range(2):
                        if len(opButtons) > (i * 2 + j):
                            self.solutionButtons[(i, j)] = QtWidgets.QPushButton(
                                opButtons[i * 2 + j])
                            self.solutionButtons[(i, j)].resize(100, 100)
                            self.solutionButtons[(i, j)].clicked.connect(
                                self.onSolvePress(opButtons[i * 2 + j]))
                            self.solutionOptionsBox.addWidget(
                                self.solutionButtons[(i, j)], i, j)
            else:
                self.bottomButton.setParent(None)
                self.solutionWidget = QWidget()
                for i in range(int(len(opButtons) / 2) + 1):
                    for j in range(2):
                        if len(opButtons) > (i * 2 + j):
                            self.solutionButtons[(i, j)] = QtWidgets.QPushButton(
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
                    if operations[0] == 'solve':
                        opButtons = ['simplify']
                else:
                    opButtons = ['simplify']
            for operation in operations:
                if operation == '+':
                    opButtons.append("addition")
                elif operation == '-':
                    opButtons.append("subtraction")
                elif operation == '*':
                    opButtons.append("multiplication")
                elif operation == '/':
                    opButtons.append("division")
                else:
                    opButtons.append(operation)
            for i in reversed(range(self.solutionOptionsBox.count())):
                self.solutionOptionsBox.itemAt(i).widget().setParent(None)
            for i in range(int(len(opButtons) / 2) + 1):
                for j in range(2):
                    if len(opButtons) > (i * 2 + j):
                        self.solutionButtons[(i, j)] = QtWidgets.QPushButton(
                            opButtons[i * 2 + j])
                        self.solutionButtons[(i, j)].resize(100, 100)
                        self.solutionButtons[(i, j)].clicked.connect(
                            self.onSolvePress(opButtons[i * 2 + j]))
                        self.solutionOptionsBox.addWidget(
                            self.solutionButtons[(i, j)], i, j)

    def clearButtons(self):
        for i in reversed(range(self.solutionOptionsBox.count())):
            self.solutionOptionsBox.itemAt(i).widget().setParent(None)

    def wrtVariableButtons(self, variables, operation):
        if isinstance(variables, list):
            varButtons = []
            if len(variables) > 0:
                for variable in variables:
                    varButtons.append(variable)
                varButtons.append("back")
                for i in reversed(range(self.solutionOptionsBox.count())):
                    self.solutionOptionsBox.itemAt(i).widget().setParent(None)
                for i in range(int(len(varButtons) / 2) + 1):
                    for j in range(2):
                        if len(varButtons) > (i * 2 + j):
                            self.solutionButtons[(i, j)] = QtWidgets.QPushButton(
                                varButtons[i * 2 + j])
                            self.solutionButtons[(i, j)].resize(100, 100)
                            self.solutionButtons[(i, j)].clicked.connect(
                                self.onWRTVariablePress(varButtons[i * 2 + j], operation))
                            self.solutionOptionsBox.addWidget(
                                self.solutionButtons[(i, j)], i, j)

    def newEquation(self):
        self.textedit.setText("")

    def saveEquation(self):
        for i in reversed(range(self.equationListVbox.count())):
            self.equationListVbox.itemAt(i).widget().setParent(None)

        eqn = str(self.textedit.toPlainText())
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
        self.myQListWidget = QtWidgets.QListWidget(self)
        i = 0
        for index, name in self.equations:
            if i != 0:
                file.write("\n")
            file.write(name)
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setTextUp(index)
            myQCustomQWidget.setTextDown(name)
            myQListWidgetItem = QtWidgets.QListWidgetItem(self.myQListWidget)
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
        eqn = str(self.textedit.toPlainText())
        for index, equation in self.equations:
            if equation == eqn:
                return self.equationListVbox

        for i in reversed(range(self.equationListVbox.count())):
            self.equationListVbox.itemAt(i).widget().setParent(None)

        if len(self.equations) == 1:
            index, name = self.equations[0]
            if index == "No equations stored":
                self.equations[0] = ("Equation No. 1", eqn)
            else:
                self.equations.append(("Equation No. 2", eqn))
        elif eqn != "":
            self.equations.append(
                ("Equation No. " + str(len(self.equations) + 1), eqn))
        file = open('local/eqn-list.vis', 'r+')
        self.myQListWidget = QtWidgets.QListWidget(self)
        i = 0
        for index, name in self.equations:
            if i != 0:
                file.write("\n")
            file.write(name)
            myQCustomQWidget = QCustomQWidget()
            myQCustomQWidget.setTextUp(index)
            myQCustomQWidget.setTextDown(name)
            myQListWidgetItem = QtWidgets.QListWidgetItem(self.myQListWidget)
            myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
            self.myQListWidget.addItem(myQListWidgetItem)
            self.myQListWidget.setItemWidget(
                myQListWidgetItem, myQCustomQWidget)
            i += 1
        file.close()
        self.myQListWidget.resize(400, 300)

        self.myQListWidget.itemClicked.connect(self.Clicked)
        self.equationListVbox.addWidget(self.myQListWidget)
        self.myQListWidget.itemClicked.connect(self.Clicked)
        self.clearButton = QtWidgets.QPushButton('Clear equations')
        self.clearButton.clicked.connect(self.clearHistory)
        self.equationListVbox.addWidget(self.clearButton)
        return self.equationListVbox

    def inputsLayout(self, loadList="Greek"):

        inputLayout = QHBoxLayout(self)
        inputWidget = QWidget()
        self.selectedCombo = str(loadList)
        for i in range(4):
            for j in range(10):
                if str(loadList) in "Greek":
                    if (i * 10 + j) < len(self.inputGreek):
                        self.buttons[(i, j)] = QtWidgets.QPushButton(
                            self.inputGreek[i * 10 + j])
                        self.buttons[(i, j)].resize(100, 100)
                        self.buttons[(i, j)].clicked.connect(
                            self.onInputPress(self.inputGreek[i * 10 + j]))
                        self.inputBox.addWidget(self.buttons[(i, j)], i, j)
                elif str(loadList) in "LaTeX":
                    if (i * 10 + j) < len(self.inputLaTeX):
                        self.buttons[(i, j)] = QtWidgets.QPushButton(
                            self.inputLaTeX[i * 10 + j])
                        self.buttons[(i, j)].resize(100, 100)
                        self.buttons[(i, j)].clicked.connect(
                            self.onInputPress(self.inputLaTeX[i * 10 + j]))
                        # (self.inputLaTeX[i * 3 + j])
                        self.inputBox.addWidget(self.buttons[(i, j)], i, j)
        inputWidget.setLayout(self.inputBox)
        # inputSplitter.addWidget(inputTypeSplitter)
        # inputSplitter.addWidget(inputWidget)
        inputLayout.addWidget(inputWidget)
        return inputLayout

    def onActivated(self, text):
        for i in reversed(range(self.inputBox.count())):
            self.inputBox.itemAt(i).widget().setParent(None)

        for i in range(4):
            for j in range(10):
                if str(text) in "Greek":
                    if (i * 10 + j) < len(self.inputGreek):
                        self.buttons[(i, j)] = QtWidgets.QPushButton(
                            self.inputGreek[i * 10 + j])
                        self.buttons[(i, j)].resize(100, 100)
                        self.buttons[(i, j)].clicked.connect(
                            self.onInputPress(self.inputGreek[i * 10 + j]))
                        self.inputBox.addWidget(self.buttons[(i, j)], i, j)
                elif str(text) in "LaTeX":
                    if (i * 10 + j) < len(self.inputLaTeX):
                        self.buttons[(i, j)] = QtWidgets.QPushButton(
                            self.inputLaTeX[i * 10 + j])
                        self.buttons[(i, j)].resize(100, 100)
                        self.buttons[(i, j)].clicked.connect(
                            self.onInputPress(self.inputLaTeX[i * 10 + j]))
                        self.inputBox.addWidget(self.buttons[(i, j)], i, j)
        self.selectedCombo = str(text)

    def onInputPress(self, name):
        def calluser():
            if name == 'C':
                self.clearAll()
            elif name == 'DEL':
                cursor = self.textedit.textCursor()
                cursor.deletePreviousChar()
            else:
                self.textedit.insertPlainText(str(name))
        return calluser

    def onSolvePress(self, name):
        def calluser():
            availableOperations = []
            tokenString = ''
            equationTokens = []
            self.resultOut = True
            if name == 'addition':
                if self.solutionType == 'expression':
                    self.tokens, availableOperations, tokenString, equationTokens, comments = addition(
                        self.tokens, True)
                else:
                    self.lTokens, self.rTokens, availableOperations, tokenString, equationTokens, comments = additionEquation(
                        self.lTokens, self.rTokens, True)
            elif name == 'subtraction':
                if self.solutionType == 'expression':
                    self.tokens, availableOperations, tokenString, equationTokens, comments = subtraction(
                        self.tokens, True)
                else:
                    self.lTokens, self.rTokens, availableOperations, tokenString, equationTokens, comments = subtractionEquation(
                        self.lTokens, self.rTokens, True)
            elif name == 'multiplication':
                if self.solutionType == 'expression':
                    self.tokens, availableOperations, tokenString, equationTokens, comments = multiplication(
                        self.tokens, True)
                else:
                    self.lTokens, self.rTokens, availableOperations, tokenString, equationTokens, comments = multiplicationEquation(
                        self.lTokens, self.rTokens, True)
            elif name == 'division':
                if self.solutionType == 'expression':
                    self.tokens, availableOperations, tokenString, equationTokens, comments = division(
                        self.tokens, True)
                else:
                    self.lTokens, self.rTokens, availableOperations, tokenString, equationTokens, comments = divisionEquation(
                        self.lTokens, self.rTokens, True)
            elif name == 'simplify':
                if self.solutionType == 'expression':
                    self.tokens, availableOperations, tokenString, equationTokens, comments = simplify(self.tokens)
                else:
                    self.lTokens, self.rTokens, availableOperations, tokenString, equationTokens, comments = simplifyEquation(self.lTokens, self.rTokens)
            elif name == 'factorize':
                self.tokens, availableOperations, tokenString, equationTokens, comments = factorize(self.tokens)
            elif name == 'find roots':
                self.lTokens, self.rTokens, availableOperations, tokenString, equationTokens, comments = quadraticRoots(self.lTokens, self.rTokens)
            elif name == 'solve':
                lhs, rhs = getLHSandRHS(self.tokens)
                variables = getVariables(lhs, rhs)
                self.wrtVariableButtons(variables, name)
                self.resultOut = False
            elif name == 'integrate':
                lhs, rhs = getLHSandRHS(self.tokens)
                variables = getVariables(lhs, rhs)
                self.wrtVariableButtons(variables, name)
                self.resultOut = False
            elif name == 'differentiate':
                lhs, rhs = getLHSandRHS(self.tokens)
                variables = getVariables(lhs, rhs)
                self.wrtVariableButtons(variables, name)
                self.resultOut = False
            if self.resultOut:
                self.eqToks = equationTokens
                self.output = resultLatex(name, equationTokens, comments)
                if len(availableOperations) == 0:
                    self.clearButtons()
                else:
                    self.refreshButtons(availableOperations)
                if self.mode == 'normal':
                    self.textedit.setText(tokenString)
                elif self.mode == 'interaction':
                    cursor = self.textedit.textCursor()
                    cursor.insertText(tokenString)
                if self.showStepByStep is True:
                    showSteps(self)
                if self.showPlotter is True:
                    plot(self)
        return calluser

    def onWRTVariablePress(self, varName, operation):

        def calluser():

            availableOperations = []
            tokenString = ''
            equationTokens = []

            if varName == 'back':
                self.input = str(self.textedit.toPlainText())
                self.tokens = tokenizer(self.input)
                # print(self.tokens)
                lhs, rhs = getLHSandRHS(self.tokens)
                operations, self.solutionType = checkTypes(
                    lhs, rhs)
                self.refreshButtons(operations)

            else:

                if operation == 'solve':
                    self.lTokens, self.rTokens, availableOperations, tokenString, equationTokens, comments = solveFor(self.lTokens, self.rTokens, varName)

                elif operation == 'integrate':
                    self.lTokens, availableOperations, tokenString, equationTokens, comments = integrate(self.lTokens, varName)

                elif operation == 'differentiate':
                    self.lTokens, availableOperations, tokenString, equationTokens, comments = differentiate(self.lTokens, varName)

                self.eqToks = equationTokens
                self.output = resultLatex(operation, equationTokens, comments, varName)

                if len(availableOperations) == 0:
                    self.clearButtons()
                else:
                    self.refreshButtons(availableOperations)
                if self.mode == 'normal':
                    self.textedit.setText(tokenString)
                elif self.mode == 'interaction':
                    cursor = self.textedit.textCursor()
                    cursor.insertText(tokenString)
                if self.showStepByStep is True:
                    showSteps(self)
                if self.showPlotter is True:
                    plot(self)

        return calluser
    def warning(self, warningstr):
        warning = QMessageBox()
        warning.setWindowTitle('WARNING')
        warning.setIcon(QMessageBox.Warning)
        warning.setText('startup failure: %s' % warningstr)
        warning.setStandardButtons(QMessageBox.Ok)
        return warning.exec_()


class QCustomQWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.textQVBoxLayout = QtWidgets.QVBoxLayout()
        self.textUpQLabel = QtWidgets.QLabel()
        self.textDownQLabel = QtWidgets.QLabel()
        self.textQVBoxLayout.addWidget(self.textUpQLabel)
        self.textQVBoxLayout.addWidget(self.textDownQLabel)
        self.allQHBoxLayout = QtWidgets.QHBoxLayout()
        self.allQHBoxLayout.addLayout(self.textQVBoxLayout, 1)
        self.setLayout(self.allQHBoxLayout)
        self.textUpQLabel.setStyleSheet('''
        color: black;
        ''')
        self.textDownQLabel.setStyleSheet('''
        color: black;
        ''')

    def setTextUp(self, text):
        self.textUpQLabel.setText(text)

    def setTextDown(self, text):
        self.textDownQLabel.setText(text)


class PicButton(QAbstractButton):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.pixmap = pixmap

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(event.rect(), self.pixmap)

    def sizeHint(self):
        return self.pixmap.size()


def initGUI():
    app = QApplication(sys.argv)
    ex = Window()
    ex.initUI()
    sys.exit(app.exec_())
