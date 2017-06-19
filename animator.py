#!/usr/bin/python

import sys
import time
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import FTGL

fonts = []
width = 600
height = 600
symbols = ['+', '-', '*', '/', '{', '}', '[',']', '^', '=']
greek = [u'\u03B1', u'\u03B2', u'\u03B3', u'\u03C0']
    
inputLaTeX = ['\\times', '\\div', '\\alpha', '\\beta', '\\gamma', '\\pi', '+', '-', '=', '^', '\\sqrt']
inputGreek = ['*', '/', u'\u03B1', u'\u03B2', u'\u03B3', u'\u03C0', '+', '-', '=', '^', 'sqrt']


def isVariable(term):
    if term in greek: 
        return True
    elif (term[0] >= 'a' and term[0] <= 'z') or (term[0] >= 'A' and term[0] <= 'Z'):
        x = 0
        while x < len(term):
            if term[x] < 'A' or (term[x] > 'Z' and term[x] < 'a') or term[x] > 'z':
                return False
            x += 1
        return True

def isNumber(term):
    x = 0
    while x < len(term):
        if term[x] < '0' or term[x] > '9':
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
    string = []
    
    string.append([{'coefficient': 1, 'type': 'variable', 'power': [1], 'value': ['x']}, {'type': 'binary', 'value': '+'}, {'coefficient': 1, 'type': 'variable', 'power': [1], 'value': ['y']}, {'type': 'binary', 'value': '='}, {'type': 'constant', 'value': 2}])
    string.append([{'coefficient': 1, 'type': 'variable', 'power': [1], 'value': ['x']}, {'type': 'binary', 'value': '+'}, {'coefficient': 1, 'type': 'variable', 'power': [1], 'value': ['y']}, {'type': 'binary', 'value': '='}, {'coefficient': 1, 'type': 'variable', 'power': [{'coefficient': 1, 'type': 'variable', 'power': [1, 2], 'value': ['x', 'y']}], 'value': [2]}])
    
    glColor3f(1.0, 1.0, 1.0)
    font = fonts[0]
    x, y = 0, 0
    i = 0
    #while  True:
    i += 1
    render_equation(x, y, string[0])
    
    glutSwapBuffers()
    time.sleep(10)
    '''
    for i, font in enumerate(fonts):
        x = 0.0
        yild = 20.0
        for j in range(0, 4):
            y = 275.0 - i * 120.0 - j * yild
            if i >= 3:
                glRasterPos(x, y)
                font.Render(string[j])
            elif i == 2:
                glEnable(GL_TEXTURE_2D)
                glEnable(GL_BLEND)
                glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
                glPushMatrix()
                glTranslatef(x, y, 0.0)
                font.Render(string[j])
                glPopMatrix()
                glDisable(GL_TEXTURE_2D)
                glDisable(GL_BLEND)
            else:
                glPushMatrix()
                glTranslatef(x, y, 0.0)
                font.Render(string[j])
                glPopMatrix()
    '''

def render_equation(x, y, string):
    

    for i, term in enumerate(string):
        if term["type"] == "variable":
            if len(term["value"])> 0:
                for j, val in enumerate(term["value"]):
                    if isVariable(val) or isNumber(str(val)):
                        glRasterPos(x, y)
                        x += 20
                        font.Render(str(val))
        elif term["type"] == "constant":
                glRasterPos(x, y)
                x += 20
                font.Render(str(term["value"]))
        elif term["type"] == "binary":
            if len(term["value"])> 0:
                glRasterPos(x, y)
                x += 20
                font.Render(term["value"])



def on_display():
    glClear(GL_COLOR_BUFFER_BIT)
    do_ortho()
    draw_scene()

def on_reshape(w, h):
    width, height = w, h

def on_key(key, x, y):
    if key == '\x1b':
        sys.exit(1)

if __name__ == '__main__':  
    glutInitWindowSize(width, height)
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA|GLUT_DOUBLE)
    glutCreateWindow("Equation")
    glClearColor(0.0, 0.0, 0.0, 0.0)
    f ="/usr/share/fonts/truetype/ubuntu-font-family/UbuntuMono-R.ttf"
    #print sys.argv[1]
    try:

        fonts = [
            #FTGL.OutlineFont(f),
            #FTGL.PolygonFont(f),
            #FTGL.TextureFont(f),
            FTGL.BitmapFont(f),
            #FTGL.PixmapFont(f),
            ]
        for font in fonts:
            font.FaceSize(24, 72)
    except Exception as e:
	print e
        print "usage:", sys.argv[0], "font_filename.ttf"
        sys.exit(0)

    glutDisplayFunc(on_display)
    glutReshapeFunc(on_reshape)
    glutKeyboardUpFunc(on_key)

    glutMainLoop()
