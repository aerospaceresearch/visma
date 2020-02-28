from flask import render_template, request, redirect, url_for, jsonify
from app import app
import sympy
import mpmath
import math


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html', title='home')

# Simplifying the expression
@app.route('/simplify/posts', methods=['POST'])
def simplify():
    try:
        value = request.form['expr']
        if '^' in value:
            value = value.replace('^', '**')
        print(value)
        ans = sympy.N(value)
        ans = str(ans)
        check = 0 
        for i in range(ans.index('.')+1, len(ans)):
            if ans[i] != '0': 
                check=1
        if check:
            return ans[:ans.index('.')+5]
        else:
            return ans[:ans.index('.')]
    except (ValueError, KeyError, TypeError) as error:
        print(error)
        return error

# Calculating the Factoral of given Number
@app.route('/factorial/posts', methods=['POST'])
def factorial():
    value = request.form['expr']
    ans = math.factorial(int(value))
    return str(ans)

# simplifying algebric and Trignometric expressions
@app.route('/simplify_expr/posts', methods=['POST'])
def simplify_expr():
    expr = request.form['expr']
    if '^' in expr:
        expr = expr.replace('^', '**')
    expr_result = sympy.simplify(expr)
    return str(expr_result)

# Integrating the given expression
# TODO !
@app.route('/integrate/posts', methods=['POST'])
def integrate():
    value = request.form['expr']
    return value

# Differentiatin the given expression
# TODO!
@app.route('/differentiate/posts', methods=['POST'])
def differentiate():
    value = request.form['expr']
    return value    
