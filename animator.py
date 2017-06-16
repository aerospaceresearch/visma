#!/usr/bin/python

import sys

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import FTGL

fonts = []
width = 600
height = 600

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
    chars = []
    
    chars[:] = []
    for i in range(1, 32):
        chars.append(chr(i))
    string.append("".join(chars))
    #print string
    chars[:] = []
    for i in range(32, 64):
        chars.append(chr(i))
    string.append("".join(chars))
    #print string
    chars[:] = []
    for i in range(64, 96):
        chars.append(chr(i))
    string.append("".join(chars))
    #print string
    chars[:] = []
    for i in range(96, 128):
        chars.append(chr(i))
    string.append("".join(chars))
    #print string
    chars[:] = []
    for i in range(128, 160):
        chars.append(chr(i))
    string.append("".join(chars))
    #print string
    chars[:] = []
    for i in range(160, 192):
        chars.append(chr(i))
    string.append("".join(chars))
    #print string
    chars[:] = []
    for i in range(192, 224):
        chars.append(chr(i))
    string.append("".join(chars))
    #print string
    chars[:] = []
    for i in range(224, 256):
        chars.append(chr(i))
    string.append("".join(chars))
    
    glColor3f(1.0, 1.0, 1.0)

    for i, font in enumerate(fonts):
        x = -250.0
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
            
  
def on_display():
    glClear(GL_COLOR_BUFFER_BIT)
    do_ortho()
    draw_scene()
    glutSwapBuffers()

def on_reshape(w, h):
    width, height = w, h

def on_key(key, x, y):
    if key == '\x1b':
        sys.exit(1)

if __name__ == '__main__':
    glutInitWindowSize(width, height)
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA|GLUT_DOUBLE)
    glutCreateWindow("PyFTGL Demo")
    glClearColor(0.0, 0.0, 0.0, 0.0)
    f ="/usr/share/fonts/truetype/ttf-liberation/LiberationMono-Regular.ttf"
    #print sys.argv[1]
    try:
        fonts = [
            FTGL.OutlineFont(f),
            FTGL.PolygonFont(f),
            FTGL.TextureFont(f),
            FTGL.BitmapFont(f),
            FTGL.PixmapFont(f),
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
