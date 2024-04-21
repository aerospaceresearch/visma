This is a brief guide on using **visma(VISualMAth)** and for making any contributions to the repo. Since visma is in its early stage, there are many features which can be implemented and many places where it can be improved/optimized.

**NOTE:** VISualMAth is supported for **python3** and above only.

### Currently, visma supports the following features

* **Simplify** - simplify the whole expression/equation or perform sub-simplifications i.e. addition, subtraction, multiplication and division
* **Find roots** - find roots for a quadratic equation
* **Factorize** - factorize a given polynomial
* **Solve** - solve the equation wrt a variable from a given equation, e.g. x^2 + y = 1, solve for x or y gives x = (1 - y)^0.5 or y = 1 - x^2
* **Integration** - integrate a polynomial expression wrt a chosen variable
* **Differentiation** - differentiate a polynomial expression wrt a chosen variable
* **Plot** - plots an interactive 2D or 3D graph
* **Matrix Operations** -  This feature will allow you to add, subtract, and multiply two matrices. Can also perform various simplifications on an individual matrix.

![visma](https://raw.githubusercontent.com/wiki/aerospaceresearch/visma/assets/demo.gif)

### If interested in making any contributions make sure to go through these steps

- Clone/fork the **dev** branch of the repo.
- Before [building from source](https://github.com/aerospaceresearch/visma/wiki/Beginner's-Guide#To-build-from-source) make sure to install all [dependencies](https://github.com/aerospaceresearch/visma/wiki/Beginner's-Guide#Dependencies)
- Make necessary changes(follow the [syntax guide](https://github.com/aerospaceresearch/visma/wiki/Beginner's-Guide#Syntax-guide))
- Before making a PR or commit, run [all modules test](https://github.com/aerospaceresearch/visma/wiki/Beginner's-Guide#Make-sure-all-tests-pass-before-making-a-PR)
- If all tests pass, make a PR or merge to **dev** branch

### How to contribute

Go through the source code, use visma and checkout the io, simplify and solver modules to get an idea of its working.
- Look for **TODOs**(simple tasks/features) and **FIXMEs**(mostly failing edge cases) throughout the code and try to strike them off
- Fix already raised [issues](https://github.com/aerospaceresearch/visma/wiki/Install)
- Add test cases to the relevant test modules for increasing code coverage through unit tests(coverage report can be viewed in htmlcov/index.html folder after running `./run test`)
- Try adding support for new functions and extend the existing modules(calculus, matrix etc)
- Add new modules(for ex, multivariable linear equation solver)

### To build from source

- [Download](https://github.com/aerospaceresearch/visma/archive/dev.zip) the source code zip
- Extract files
- From project folder, do `$ ./run install` or `$ pip install -r requirements.txt`(make sure to check if the pip exists in python3 library by checking the pip version, use `$ pip --version`)
- For launching visma do
    ```bash
    $ python main.py
    >>> gui
    ```

### Dependencies

- The following packages are required for using visma:
    - PyQt5
    - matplotlib
    - numpy
- The following packages are required for testing visma:
    - pytest
    - pylama
    - coverage

### Syntax guide

- Follow **_camelCase_** for naming variables, functions etc. For example:
    - variables: _symTokens_, _axisRange_ etc
    - functions: _tokenizer_, _getLevelVariables_ etc
    - classes: _Function_, _SquareMatrix_ etc
- Use 4 spaces for tabs
- Add relevant code to the respective modules

### Make sure all tests pass before making a PR

- To run all tests do `./run test`
- To run only linter/syntax test(pylama) do `./run test syntax`
- To test all modules(pytest) do `./run test modules`

PRs are welcomed. If there are any issues or ideas they can be addressed through the [issues](https://github.com/aerospaceresearch/visma/issues) or in [chat room](https://gitter.im/aerospaceresearch/visma).
