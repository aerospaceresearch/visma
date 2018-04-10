#!/usr/bin/python

"""
Initial Author: Siddharth Kothiyal (sidkothiyal, https://github.com/sidkothiyal)
Other Authors:
Owner: AerospaceResearch.net
About: This module is aimed at creating a one function call animator. The developer will only need to make a function call with the list of
	equations that were achieved while solving the problem, and this module will do the rest.
	The module is invoked as a subprocess from main.py, when animation event is triggered. It takes json format which are passed as program arguements, and converts
	them from json format to list and dict format in python.
Note: Please try to maintain proper documentation
Logic Description:
"""

import sys
import time
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import json

import FTGL

fontStyle = "/usr/share/fonts/truetype/ubuntu-font-family/UbuntuMono-R.ttf"
font = FTGL.BitmapFont(fontStyle)
width = 800
height = 800
symbols = ['+', '-', '*', '/', '{', '}', '[',']', '^', '=']
greek = [u'\u03B1', u'\u03B2', u'\u03B3', u'\u03C0']

inputLaTeX = ['\\times', '\\div', '\\alpha', '\\beta', '\\gamma', '\\pi', '+', '-', '=', '^', '\\sqrt']
inputGreek = ['*', '/', u'\u03B1', u'\u03B2', u'\u03B3', u'\u03C0', '+', '-', '=', '^', 'sqrt']

string = []
comments = []
first_time = False

def is_number(term):

	if isinstance(term, int) or isinstance(term, float):
		return True
	else:
		x = 0
		dot = 0
		if term[0] == '-':
			x += 1
			while x < len(term):
				if (term[x] < '0' or term[x] > '9') and (dot!= 0 or term[x] != '.'):
					return False
				if term[x] == '.':
					dot += 1
				x += 1
			if x >= 2:
				return True
			else:
				return False
		else:
			while x < len(term):
				if (term[x] < '0' or term[x] > '9') and (dot!= 0 or term[x] != '.'):
					return False
				if term[x] == '.':
					dot += 1
				x += 1
		return True

def number_of_digits(number):
	num = number
	l = 0
	if num < 0:
		l += 1
		num = 0 - num
	while num >= 1:
		num /= 10
		l += 1
	return l

def get_num(term):
	return float(term)

def is_variable(term):
	if term in greek:
		return True
	elif (term[0] >= 'a' and term[0] <= 'z') or (term[0] >= 'A' and term[0] <= 'Z'):
		x = 0
		while x < len(term):
			if term[x] < 'A' or (term[x] > 'Z' and term[x] < 'a') or term[x] > 'z':
				return False
			x += 1
		return True

def do_ortho():
	w, h = width, height
	glViewport(0, 0, w, h)

	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()

	size = max(w, h) / 2.0
	aspect = float(w) / float(h)
	if w <= h:
		aspect = float(h) / float(w)
		glOrtho(-size, size, -size*aspect, size*aspect, -100000.0, 100000.0)
	else:
		glOrtho(-size*aspect, size*aspect, -size, size, -100000.0, 100000.0)
	glScaled(aspect, aspect, 1.0)

	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()



def draw_scene():
	glColor3f(1.0, 1.0, 1.0)
	i = 0
	x, y = -50, -200
	global comments
	global first_time
	if not first_time:
		first_time = True
		while i < len(string):
			glClear(GL_COLOR_BUFFER_BIT)
			i += 1
			j = 0
			tempY = y
			while j < i:
				for comment in comments[j]:
					l = len(comment)
					render_comment(-l * 5, tempY, comment)
					tempY -= 50
				l = calc_equation_size(string[j])
				render_equation(-l/2, tempY, string[j])
				tempY -= 50
				j += 1
			y += 50 + (len(comments[j-1]) * 30)
			glutSwapBuffers()
			time.sleep(2)
	else:
		while i < len(string):
			glClear(GL_COLOR_BUFFER_BIT)
			i += 1
			j = 0
			tempY = y
			while j < i:
				for comment in comments[j]:
					l = len(comment)
					render_comment(-l * 5, tempY, comment)
					tempY -= 50
				l = calc_equation_size(string[j])
				render_equation(-l/2, tempY, string[j])
				tempY -= 50
				j += 1
			y += 50 + (len(comments[j-1]) * 30)
			glutSwapBuffers()

def render_comment(x, y, comment):
	glRasterPos(x, y)
	font.FaceSize(18)
	font.Render(str(comment.encode('utf-8')))


def calc_variable_size(term):
	size = 0
	if term["coefficient"] == 1:
		pass
	elif term["coefficient"] < 0:
		if term["coefficient"] == -1:
			size += 20
		else:
			l = number_of_digits(term["coefficient"])
			size += (l * 15 + 20)
	else:
		l = number_of_digits(term["coefficient"])
		size += (l *15 + 20)
	if len(term["value"])> 0:
		for j, val in enumerate(term["value"]):
			if type(val) == dict:
				if val["type"] == 'variable':
					size += render_variable(val)
				elif val["type"] == 'expression':
					size += render_equation(val)
				else:
					pass
			if is_number(str(val)):
				l = number_of_digits(val)
				size += (15 * l)
			else:
				size += 20
			if type(term["power"][j]) == dict:
				if term["power"][j]["type"] == 'variable':
					size += calc_variable_size(term["power"][j])
				elif term["power"][j]["type"] == 'expression':
					size += calc_equation_size(term["power"][j])
				else:
					pass
			elif is_variable(str(term["power"][j])):
				size += (15 * len(term["power"][j]) + 15)
			elif is_number(str(term["power"][j])):
				if term["power"][j] == 1:
					size += 15
					pass
				else:
					if is_number(term["power"][j]):
						l = number_of_digits(term["power"][j])
						size += (15 * l + 15)
					else:
						size += (15 * len(term["power"][j]) + 15)
	return size


def calc_equation_size(string):
	size = 0
	for i, term in enumerate(string):
		if term["type"] == "variable":
			size += calc_variable_size(term)
		elif term["type"] == "constant":
			l = number_of_digits(term["value"])
			if l == 0:
				size += 50
			else:
				size += (15 *l) + 20
		elif term["type"] == "binary":
			if len(term["value"])> 0:
				size += 20
		elif term["type"] == "expression":
			size += 15
			size += calc_equation_size(term["tokens"])
			size += 15
		elif term["type"] == "sqrt":
			if term["power"]["type"] == 'constant':
				l = number_of_digits(term["power"]["value"])
				size += (7 * l + 10)
			elif term["power"]["type"] == 'variable':
				size += calc_variable_size(term["power"])
			elif term["power"]["type"] == 'expression':
				size += calc_equation_size(term["power"])
			size += 25
			if term["expression"]["type"] == 'constant':
				l = number_of_digits(term["expression"]["value"])
				size += (20 + 15 * l)
			elif term["expression"]["type"] == 'variable':
				size += calc_variable_size(term["expression"])
			elif term["expression"]["type"] == 'expression':
				size += calc_equation_size(term["expression"])
	return size

def render_variable(x, y, term, level=1, fontSize=24):
	glRasterPos(x, y)
	font.FaceSize(24)
	if term["coefficient"] == 1:
		pass
	elif term["coefficient"] < 0:
		if term["coefficient"] == -1:
			font.Render(str('-'))
			x += 20
		else:
			font.Render(str(term["coefficient"]))
			l = number_of_digits(term["coefficient"])
			x += (l * 15 + 20)
	else:
		font.Render(str(term["coefficient"]))
		l = number_of_digits(term["coefficient"])
		x += (l *15 + 20)
	if len(term["value"])> 0:
		for j, val in enumerate(term["value"]):
			if type(val) == dict:
				if val["type"] == 'variable':
					x, y = render_variable(x, y, val, level+1)
				elif val["type"] == 'expression':
					x, y = render_equation(x, y, val, level)
				else:
					pass
			elif is_variable(str(val)) or is_number(str(val)):
				glRasterPos(x, y)
				font.FaceSize(fontSize)
				if val in greek:
					font.Render(str(val.encode('utf-8')))
				else:
					font.Render(str(val))
			if is_number(str(val)):
				l = number_of_digits(val)
				x += (15 * l)
			else:
				x += 20
			if type(term["power"][j]) == dict:
				if term["power"][j]["type"] == 'variable':
					x, y = render_variable(x, y+10, term["power"][j], level + 1, 2*fontSize/3)
				elif term["power"][j]["type"] == 'expression':
					x, y = render_equation(x, y+10, term["power"][j], level + 1, 2*fontSize/3)
				else:
					pass
			elif is_variable(str(term["power"][j])):
				glRasterPos(x, y + 10)
				font.FaceSize(2  * fontSize/3)
				if term["power"][j] in greek:
					font.Render(str(term["power"][j].encode('utf-8')))
				else:
					font.Render(str(term["power"][j]))
				x += (15 * len(term["power"][j]) + 15)
			elif is_number(str(term["power"][j])):
				if term["power"][j] == 1:
					x += 15
					pass
				else:
					glRasterPos(x, y + 10)
					font.FaceSize(2  * fontSize/3)
					if term["power"][j] in greek:
						font.Render(str(term["power"][j].encode('utf-8')))
					else:
						font.Render(str(term["power"][j]))
					if is_number(term["power"][j]):
						l = number_of_digits(term["power"][j])
						x += (15 * l + 15)
					else:
						x += (15 * len(term["power"][j]) + 15)
	return x, y

def render_equation(x, y, string, level=1, fontSize=24):
	for i, term in enumerate(string):
		if term["type"] == "variable":
			x, y = render_variable(x, y, term)
		elif term["type"] == "constant":
			glRasterPos(x, y)
			font.FaceSize(fontSize)
			font.Render(str(term["value"]))
			l = number_of_digits(term["value"])
			if l == 0:
				x += 50
			else:
				x += (25 * l) + 25
		elif term["type"] == "binary":
			if len(term["value"])> 0:
				glRasterPos(x, y)
				x += 20
				font.FaceSize(fontSize)
				font.Render(term["value"].encode("utf-8"))
		elif term["type"] == "expression":
			glRasterPos(x, y)
			font.FaceSize(fontSize)
			font.Render('{')
			x += 15
			x, y = render_equation(x, y, term["tokens"], level+1)
			font.FaceSize(fontSize)
			x += 15
			glRasterPos(x, y)
			font.Render('}')
			x += 10
			glRasterPos(x, y+10)
			font.FaceSize(2 * fontSize /3)
			font.Render(str(term["power"]))
			l = number_of_digits(term["power"])
			x += (15*l)
			x += 15
			glRasterPos(x, y)
		elif term["type"] == "sqrt":
			if term["power"]["type"] == 'constant':
				glRasterPos(x, y + 5)
				font.FaceSize(fontSize/2)
				font.Render(str(term["power"]["value"]))
				l = number_of_digits(term["power"]["value"])
				x += (10 + l * 7)
			elif term["power"]["type"] == 'variable':
				x, y = render_variable(x, y+5, term["power"], level+1, fontSize/2)
			elif term["power"]["type"] == 'expression':
				x, y = render_equation(x, y+5, term["power"], level+1, fontSize/2)
			glRasterPos(x, y)
			font.FaceSize(fontSize)
			x += 25
			font.Render(u"\u221A".encode("utf-8"))
			if term["expression"]["type"] == 'constant':
				glRasterPos(x, y)
				font.FaceSize(fontSize)
				font.Render(str(term["expression"]["value"]))
				x += (30 + 15 * l)
			elif term["expression"]["type"] == 'variable':
				x, y = render_variable(x, y, term["expression"], level+1, fontSize)
			elif term["expression"]["type"] == 'expression':
				x, y = render_equation(x, y, term["expression"], level+1, fontSize)

	return x, y


def on_display():
	glClear(GL_COLOR_BUFFER_BIT)
	do_ortho()
	draw_scene()

def on_reshape(w, h):
	width, height = w, h

def on_key(key, x, y):
	if key == '\x1b':
		sys.exit(1)

def main():
    #print string
	glutInitWindowSize(width, height)
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_RGBA|GLUT_DOUBLE)
	glutCreateWindow("Equation")
	glClearColor(0.0, 0.0, 0.0, 0.0)
	font.FaceSize(24, 72)

	glutDisplayFunc(on_display)
	glutReshapeFunc(on_reshape)
	glutKeyboardUpFunc(on_key)
	glutMainLoop()


def animate(tokens):
	global string
	string = tokens
	main()

if __name__ == '__main__':
	tokens = sys.argv[1]
	coms = sys.argv[2]
	comments = json.loads(coms)
	#print tokens
	animate(json.loads(tokens))
	#main()
