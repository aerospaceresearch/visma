sudo apt install python2.7-dev python-pip -y
sudo apt install libxext-dev python-qt4 qt4-dev-tools build-essential -y
sudo apt install freeglut3-dev libboost-python-dev -y
sudo apt install python-opengl
sudo pip2 install simplejson
sudo apt install libftgl-dev ftgl-dev -y
git clone https://github.com/umlaeute/pyftgl.git
cd pyftgl
python setup.py build
sudo python setup.py install
cd ..
rm -rf pyftgl
mkdir temp
chmod -R 777 temp
python main.py
