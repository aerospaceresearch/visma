from flask import render_template, request, redirect, url_for
from app import app
from sympy import *
from sympy.parsing.sympy_parser import parse_expr

@app.route('/')
@app.route('/index')
def index():
    if request.args.get('ans'):
        return render_template('index.html', title='sol', ans=request.args.get('ans'))
    else:
        return render_template('index.html', title='home')

@app.route('/simplify/posts',methods=['GET', 'POST'])
def simplify():
    value = request.form['expr']
    print(value)
    ans = parse_expr(value)
    ans = ans.evalf()
    return redirect(url_for('index',ans=ans))
