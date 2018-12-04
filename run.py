#! /usr/bin/env python

from __future__ import print_function
import sys
import subprocess
import threading
import glob


def Str(value):
    if isinstance(value, list):
        return " ".join(value)
    if isinstance(value, basestring):
        return value
    return str(value)


def Glob(value):
    ret = glob.glob(value)
    if(len(ret) < 1):
        ret = [value]
    return ret


if(str(sys.argv[1]) == str()):
    print("")
    print("Enter command arguments with run")
    print("    run.py install - Install all dependencies for visma")
    print("    run.py visma - Open visma GUI")
    print("    run.py test - Run all the tests and generates coverage report")
    print("    run.py test path/to/test_file.py - Runs all tests and shows coverage for given file")
    print("    run.py test syntax - Run syntax test using pylama")
    print("    run.py test modules - Run tests using pytest for all modules")
    print("    run.py test coverage - After running all the tests, open coverage report")
    print("    run.py pack - Generate builds for visma package")
    print("    run.py pack upload - Generate builds and then upload to test.pypi.org")
    print("    run.py pack final - Generate builds and upload final build to pypi.org")
    print("    run.py clean - Clean all cache, reports and builds")
    print("")
elif (str(sys.argv[1]) == "install"):
    subprocess.call(["python3 -m pip install -r requirements.txt"], shell=True)
elif (str(sys.argv[1]) == "visma"):
    subprocess.call(["python3 main.py"], shell=True)

elif str(sys.argv[1]) == "test":
    if str(sys.argv[2]) == "syntax" or str(sys.argv[2]) == str():
        print("Python Syntax Test ...")
        subprocess.call(["pylama"], shell=True)
    elif (str(sys.argv[2]) == "modules"):
        print("Python Modules Test ...")
        subprocess.call(["pytest"], shell=True)

    if str(sys.argv[2]) != str() and str(sys.argv[2]) != "coverage" and str(sys.argv[2]) != "syntax" and str(sys.argv[2]) != "modules" :
        print("Python Test for " + str(sys.argv[2]) + " ...")
        subprocess.call(["coverage run --source ./ -m pytest " + str(sys.argv[2]) + " -v"], shell=True)
    elif str(sys.argv[2]) == str():
        print("Python Modules Test with Coverage ...")
        subprocess.call(["coverage run --source ./ -m pytest -v"], shell=True)

    if str(sys.argv[2]) == str() or str(sys.argv[2]) == "coverage" or str(sys.argv[3]) == "coverage":
        subprocess.call(["coverage report"], shell=True)
        subprocess.call(["coverage html"], shell=True)

    if str(sys.argv[2]) == "coverage" or str(sys.argv[3]) == "coverage":
        def thread1():
            subprocess.call(["nohup xdg-open ./htmlcov/index.html"], shell=True)
            threading.Thread(target=thread1).start()

elif str(sys.argv[1]) == "pack":
    subprocess.call(["mv main.py visma"], shell=True)
    subprocess.call(["python3 setup.py sdist bdist_wheel"], shell=True)
    subprocess.call(["mv ./visma/main.py ./"], shell=True)

    if str(sys.argv[2]) == "upload":
        subprocess.call(["twine upload --repository-url https://test.pypi.org/legacy/", Str(Glob("dist/*"))],shell=True)
    elif str(sys.argv[2]) == "final":
        subprocess.call(["twine upload",Str(Glob("dist/*"))], shell=True)

elif str(sys.argv[1]) == "clean":
    subprocess.call(["git clean -xdf"], shell=True)
else:
    print("Invalid arguments")
