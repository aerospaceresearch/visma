sudo apt-get install python2.7-dev python-pip 
sudo apt-get install libxext-dev python-qt4 qt4-dev-tools build-essential
sudo apt-get install freeglut3-dev 
sudo pip install simplejson
sudo pip install pyopengl
sudo apt install libftgl-dev ftgl-dev
git clone https://github.com/umlaeute/pyftgl.git
cd pyftgl
python setup.py build
sudo python setup.py install
cd ..
rm -rf pyftgl
python main.py


