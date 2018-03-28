"""
Initial Author: Siddharth Kothiyal (sidkothiyal, https://github.com/sidkothiyal)
Other Authors:
Owner: AerospaceResearch.net
About: This module is created to handle the GUI of the project, this module interacts with solve initially to check for all the available functions, and then according
	to the event selected by the user, it interacts with solve, or find_roots module.
	Invokes animator module as a seperate subprocess using Popen, and passes the equations/expressions to be animated and comments which go along with them in the
	json format as arguements.
Note: Please try to maintain proper documentation
Logic Description:
"""

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4 import QtGui
import tokenize
import solve
import find_roots
import json
from subprocess import Popen
import os

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

	#inputLaTeX = ['7', '8', '9', '4', '5', '6', '1', '2', '3', '0', '+', '-', '\\times', '\\div',  '=', 'x', 'y', 'z', '\\alpha', '\\beta', '\\gamma', '\\pi', '^{}', '\\sqrt[n]{}']
	#inputGreek = ['7', '8', '9', '4', '5', '6', '1', '2', '3', '0', '+', '-', '*', '/', '=', 'x', 'y', 'z', u'\u03B1', u'\u03B2', u'\u03B3', u'\u03C0', '^{}', 'sqrt[n]{}']
	inputLaTeX = ['\\times', '\\div', '+', '-', '=', '^', '\\sqrt']
	inputGreek = ['*', '/', '+', '-', '=', '^', 'sqrt']

	mode = 'interaction'
	buttons = {}
	solutionOptionsBox = QGridLayout()
	solutionButtons = {}
	inputBox = QGridLayout()
	selectedCombo = "LaTeX"
	equations = []
	try:
		with open('tmp/eqn-list.vis', 'r+') as fp:
			for line in fp:
				if not line.isspace():
					fp.write(line)
					equations.insert(0, ('Equation No.' + str(len(equations) + 1), line))
			fp.close()
	except IOError:
		if not os.path.exists('tmp'):
			os.mkdir('tmp')
		file = open('tmp/eqn-list.vis', 'w')
		file.close()

	if len(equations) == 0:
		equations =[('No equations stored', '')]

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

		eqautionList = QWidget()
		eqautionList.setLayout(self.equationsLayout())
		eqautionList.setStatusTip("Track of old equations")

		inputList = QWidget()
		inputList.setLayout(self.inputsLayout())
		inputList.setStatusTip("Input characters")

		buttonSpace = QWidget()
		buttonSpace.setLayout(self.buttonsLayout())

		self.textedit = QTextEdit()
		self.textedit.textChanged.connect(self.textChangeTrigger)
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

	def textChangeTrigger(self):
		pass
		#print self.textedit.toPlainText()

	def equationsLayout(self):
		self.myQListWidget = QtGui.QListWidget(self)
		for index, name in self.equations:
			myQCustomQWidget = QCustomQWidget()
			myQCustomQWidget.setTextUp(index)
			myQCustomQWidget.setTextDown(name)
			myQListWidgetItem = QtGui.QListWidgetItem(self.myQListWidget)
			myQListWidgetItem.setSizeHint(myQCustomQWidget.sizeHint())
			self.myQListWidget.addItem(myQListWidgetItem)
			self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)

		self.myQListWidget.resize(400,300)

		self.myQListWidget.itemClicked.connect(self.Clicked)
		self.equationListVbox.addWidget(self.myQListWidget)
		return self.equationListVbox


	def Clicked(self,item):
		index, name = self.equations[self.myQListWidget.currentRow()]
		self.textedit.setText(name)


	def buttonsLayout(self):
		vbox = QVBoxLayout()

		interactionModeWidget = QWidget(self)
		interactionModeLayout = QVBoxLayout()
		interactionModeButton = QPushButton("Interaction Mode")
		interactionModeButton.resize(30, 70)
		interactionModeButton.clicked.connect(self.interactionMode)
		interactionModeLayout.addWidget(interactionModeButton)
		interactionModeWidget.setLayout(interactionModeLayout)
		topButtonSplitter = QSplitter(Qt.Horizontal)
		topButtonSplitter.addWidget(interactionModeWidget)
		permanentButtons = QWidget(self)
		documentButtonsLayout = QHBoxLayout()
		newButton = PicButton(QPixmap("resources/new.png"))
		saveButton = PicButton(QPixmap("resources/save.png"))
		newButton.setToolTip('Add New Equation')
		saveButton.setToolTip('Save Equation')
		documentButtonsLayout.addWidget(newButton)
		documentButtonsLayout.addWidget(saveButton)
		newButton.clicked.connect(self.newEquation)
		saveButton.clicked.connect(self.saveEquation)
		permanentButtons.setLayout(documentButtonsLayout)
		topButtonSplitter.addWidget(permanentButtons)
		topButtonSplitter.setSizes([10000, 2])

		self.bottomButton = QFrame()
		self.buttonSplitter = QSplitter(Qt.Vertical)
		self.buttonSplitter.addWidget(topButtonSplitter)
		self.buttonSplitter.addWidget(self.bottomButton)
		self.buttonSplitter.setSizes([1, 1000])
		vbox.addWidget(self.buttonSplitter)
		return vbox

	def interactionMode(self):
		#cursor = self.textedit.textCursor()
		#textSelected = cursor.selectedText()
		cursor = self.textedit.textCursor()
		interactionText = cursor.selectedText()
		if str(interactionText) == '':
			self.mode = 'normal'
			textSelected = str(self.textedit.toPlainText())
		else:
			textSelected = str(interactionText)
			self.mode = 'interaction'
		self.tokens = tokenize.tokenizer(textSelected)
		#print self.tokens
		self.addEquation()
		lhs, rhs = tokenize.get_lhs_rhs(self.tokens)
		self.lTokens = lhs
		self.rTokens = rhs
		operations, self.solutionType = solve.check_types(lhs, rhs)
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

			if self.buttonSet:
				for i in reversed(range(self.solutionOptionsBox.count())):
					self.solutionOptionsBox.itemAt(i).widget().setParent(None)
				for i in xrange(int(len(opButtons)/3) + 1):
					for j in range(3):
						if len(opButtons) > (i * 3 + j):
							self.solutionButtons[(i,j)] = QtGui.QPushButton(opButtons[i*3 + j])
							self.solutionButtons[(i,j)].resize(100, 100)
							self.solutionButtons[(i,j)].clicked.connect(self.onSolvePress(opButtons[i*3+j]))
							self.solutionOptionsBox.addWidget(self.solutionButtons[(i,j)], i, j)
			else:
				self.bottomButton.setParent(None)
				self.solutionWidget = QWidget()
				for i in xrange(int(len(opButtons)/3) + 1):
					for j in range(3):
						if len(opButtons) > (i * 3 + j):
							self.solutionButtons[(i,j)] = QtGui.QPushButton(opButtons[i*3 + j])
							self.solutionButtons[(i,j)].resize(100, 100)
							self.solutionButtons[(i,j)].clicked.connect(self.onSolvePress(opButtons[i*3+j]))
							self.solutionOptionsBox.addWidget(self.solutionButtons[(i,j)], i, j)
				self.solutionWidget.setLayout(self.solutionOptionsBox)
				self.buttonSplitter.addWidget(self.solutionWidget)
				self.buttonSet = True
				self.buttonSplitter.setSizes([01, 1000])

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
			for i in reversed(range(self.solutionOptionsBox.count())):
				self.solutionOptionsBox.itemAt(i).widget().setParent(None)
			for i in xrange(int(len(opButtons)/3) + 1):
				for j in range(3):
					if len(opButtons) > (i * 3 + j):
						self.solutionButtons[(i,j)] = QtGui.QPushButton(opButtons[i*3 + j])
						self.solutionButtons[(i,j)].resize(100, 100)
						self.solutionButtons[(i,j)].clicked.connect(self.onSolvePress(opButtons[i*3+j]))
						self.solutionOptionsBox.addWidget(self.solutionButtons[(i,j)], i, j)

	def clearButtons(self):
		for i in reversed(range(self.solutionOptionsBox.count())):
			self.solutionOptionsBox.itemAt(i).widget().setParent(None)

	def solveForButtons(self, variables):
		if isinstance(variables, list):
			varButtons = []
			if len(variables) > 0:
				for variable in variables:
					varButtons.append(variable)
				varButtons.append("Back")
				for i in reversed(range(self.solutionOptionsBox.count())):
					self.solutionOptionsBox.itemAt(i).widget().setParent(None)
				for i in xrange(int(len(varButtons)/3) + 1):
					for j in range(3):
						if len(varButtons) > (i * 3 + j):
							self.solutionButtons[(i,j)] = QtGui.QPushButton(varButtons[i*3 + j])
							self.solutionButtons[(i,j)].resize(100, 100)
							self.solutionButtons[(i,j)].clicked.connect(self.onSolveForPress(varButtons[i*3+j]))
							self.solutionOptionsBox.addWidget(self.solutionButtons[(i,j)], i, j)

	def newEquation(self):
		self.textedit.setText("")

	def saveEquation(self):
		for i in reversed(range(self.equationListVbox.count())):
			self.equationListVbox.itemAt(i).widget().setParent(None)

		eqn = unicode(self.textedit.toPlainText())
		if len(self.equations) ==  1:
			index, name = self.equations[0]
			if index == "No equations stored":
				self.equations[0] = ("Equation No. 1", eqn)
			else:
				self.equations.append(("Equation No. 2", eqn))
		else:
			self.equations.append(("Equation No. " + str(len(self.equations) + 1), eqn))

		self.textedit.setText('')
		file = open('tmp/eqn-list.vis', 'r+')
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
			self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
			i += 1
		file.close()
		self.myQListWidget.resize(400,300)

		self.myQListWidget.itemClicked.connect(self.Clicked)
		self.equationListVbox.addWidget(self.myQListWidget)
		return self.equationListVbox

	def addEquation(self):
		eqn = unicode(self.textedit.toPlainText())
        	for index, equation in self.equations:
			if equation == eqn:
				return self.equationListVbox

		for i in reversed(range(self.equationListVbox.count())):
			self.equationListVbox.itemAt(i).widget().setParent(None)

		if len(self.equations) ==  1:
			index, name = self.equations[0]
			if index == "No equations stored":
				self.equations[0] = ("Equation No. 1", eqn)
			else:
				self.equations.append(("Equation No. 2", eqn))
		else:
			self.equations.append(("Equation No. " + str(len(self.equations) + 1), eqn))
		file = open('tmp/eqn-list.vis', 'r+')
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
			self.myQListWidget.setItemWidget(myQListWidgetItem, myQCustomQWidget)
			i += 1
		file.close()
		self.myQListWidget.resize(400,300)

		self.myQListWidget.itemClicked.connect(self.Clicked)
		self.equationListVbox.addWidget(self.myQListWidget)
		return self.equationListVbox

	def inputsLayout(self, loadList="LaTeX"):
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
						self.buttons[(i, j)].clicked.connect(self.onInputPress(self.inputGreek[i * 3 + j]))
						self.inputBox.addWidget(self.buttons[(i, j)], i, j)
				elif str(loadList) in "LaTeX":
					if (i*3 + j) < len(self.inputLaTeX):
						self.buttons[(i, j)] = QtGui.QPushButton(self.inputLaTeX[i * 3 + j])
						self.buttons[(i, j)].resize(100, 100)
						self.buttons[(i, j)].clicked.connect(self.onInputPress(self.inputLaTeX[i * 3 + j]))
						#(self.inputLaTeX[i * 3 + j])
						self.inputBox.addWidget(self.buttons[(i, j)], i, j)
		inputWidget.setLayout(self.inputBox)
		inputSplitter.addWidget(topSplitter)
		inputSplitter.addWidget(inputWidget)
		inputSplitter.setSizes([10, 1000])
		inputLayout.addWidget(inputSplitter)
		return inputLayout

	def onActivated(self, text):
		for i in reversed(range(self.inputBox.count())):
			self.inputBox.itemAt(i).widget().setParent(None)

		for i in range(10):
			for j in range(3):
				if str(text) in "Greek":
					if (i*3 + j) < len(self.inputGreek):
						self.buttons[(i, j)] = QtGui.QPushButton(self.inputGreek[i * 3 + j])
						self.buttons[(i, j)].resize(100, 100)
						self.buttons[(i, j)].clicked.connect(self.onInputPress(self.inputGreek[i * 3 + j]))
						self.inputBox.addWidget(self.buttons[(i, j)], i, j)
				elif str(text) in "LaTeX":
					if (i*3 + j) < len(self.inputLaTeX):
						self.buttons[(i, j)] = QtGui.QPushButton(self.inputLaTeX[i * 3 + j])
						self.buttons[(i, j)].resize(100, 100)
						self.buttons[(i, j)].clicked.connect(self.onInputPress(self.inputLaTeX[i * 3 + j]))
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
			animation = []
			if name == 'Addition':
				if self.solutionType == 'expression':
					self.tokens, availableOperations, token_string, animation, comments = solve.addition(self.tokens, True)
				else:
					self.lTokens, self.rTokens, availableOperations, token_string, animation, comments = solve.addition_equation(self.lTokens, self.rTokens, True)
				Popen(['python', 'animator.py', json.dumps(animation), json.dumps(comments)])
				if len(availableOperations) == 0:
					self.clearButtons()
				else:
					self.refreshButtons(availableOperations)
				if self.mode == 'normal':
					self.textedit.setText(token_string)
				elif self.mode == 'interaction':
					cursor = self.textedit.textCursor()
					cursor.insertText(token_string)
			elif name == 'Subtraction':
				if self.solutionType == 'expression':
					self.tokens, availableOperations, token_string, animation, comments = solve.subtraction(self.tokens, True)
				else:
					self.lTokens, self.rTokens, availableOperations, token_string, animation, comments = solve.subtraction_equation(self.lTokens, self.rTokens, True)
				Popen(['python', 'animator.py', json.dumps(animation), json.dumps(comments)])
				if len(availableOperations) == 0:
					self.clearButtons()
				else:
					self.refreshButtons(availableOperations)
				if self.mode == 'normal':
					self.textedit.setText(token_string)
				elif self.mode == 'interaction':
					cursor = self.textedit.textCursor()
					cursor.insertText(token_string)
			elif name == 'Multiplication':
				if self.solutionType == 'expression':
					self.tokens, availableOperations, token_string, animation, comments = solve.multiplication(self.tokens, True)
				else:
					self.lTokens, self.rTokens, availableOperations, token_string, animation, comments = solve.multiplication_equation(self.lTokens, self.rTokens, True)
				Popen(['python', 'animator.py', json.dumps(animation), json.dumps(comments)])
				if len(availableOperations) == 0:
					self.clearButtons()
				else:
					self.refreshButtons(availableOperations)
				if self.mode == 'normal':
					self.textedit.setText(token_string)
				elif self.mode == 'interaction':
					cursor = self.textedit.textCursor()
					cursor.insertText(token_string)
			elif name == 'Division':
				if self.solutionType == 'expression':
					self.tokens, availableOperations, token_string, animation, comments = solve.division(self.tokens, True)
				else:
					self.lTokens, self.rTokens, availableOperations, token_string, animation, comments = solve.division_equation(self.lTokens, self.rTokens, True)
				Popen(['python', 'animator.py', json.dumps(animation), json.dumps(comments)])
				if len(availableOperations) == 0:
					self.clearButtons()
				else:
					self.refreshButtons(availableOperations)
				if self.mode == 'normal':
					self.textedit.setText(token_string)
				elif self.mode == 'interaction':
					cursor = self.textedit.textCursor()
					cursor.insertText(token_string)
			elif name == 'Simplify':
				if self.solutionType == 'expression':
					self.tokens, availableOperations, token_string, animation, comments = solve.simplify(self.tokens)
				else:
					self.lTokens, self.rTokens, availableOperations, token_string, animation, comments = solve.simplify_equation(self.lTokens, self.rTokens)
				Popen(['python', 'animator.py', json.dumps(animation), json.dumps(comments)])
				if len(availableOperations) == 0:
					self.clearButtons()
				else:
					self.refreshButtons(availableOperations)
				if self.mode == 'normal':
					self.textedit.setText(token_string)
				elif self.mode == 'interaction':
					cursor = self.textedit.textCursor()
					cursor.insertText(token_string)
			elif name == 'Solve For':
				lhs, rhs = tokenize.get_lhs_rhs(self.tokens)
				variables = solve.find_solve_for(lhs, rhs)
				self.solveForButtons(variables)
			elif name == 'Find Roots':
				self.lTokens, self.rTokens, availableOperations, token_string, animation, comments = find_roots.quadratic_roots(self.lTokens, self.rTokens)
				Popen(['python', 'animator.py', json.dumps(animation), json.dumps(comments)])
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

	def onSolveForPress(self, name):
		def calluser():
			availableOperations = []
			token_string = ''
			animation = []
			if name == 'Back':
				textSelected = str(self.textedit.toPlainText())
				self.tokens = tokenize.tokenizer(textSelected)
				#print self.tokens
				lhs, rhs = tokenize.get_lhs_rhs(self.tokens)
				operations, self.solutionType = solve.check_types(lhs, rhs)
				self.refreshButtons(operations)

			else:
				print name
				self.lTokens, self.rTokens, availableOperations, token_string, animation, comments = solve.solve_for(self.lTokens, self.rTokens, name)
				Popen(['python', 'animator.py', json.dumps(animation), json.dumps(comments)])
				self.refreshButtons(availableOperations)
				if self.mode == 'normal':
					self.textedit.setText(token_string)
				elif self.mode == 'interaction':
					cursor = self.textedit.textCursor()
					cursor.insertText(token_string)

		return calluser

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
