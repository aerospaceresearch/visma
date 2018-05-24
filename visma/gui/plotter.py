import numpy as np
import matplotlib.pyplot as plt

# TODO: Use matplotlib to plot graphs(use openGL if possible)


def graph(formula, range=range(-50, 50)):
    x = np.array(range)
    y = formula(x)  # <- note now we're calling the function 'formula' with x
    plt.plot(x, y)
    plt.grid()
    plt.show()


def my_formula(x):
    return x**2+x+1


graph(my_formula)
