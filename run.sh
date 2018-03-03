declare -a distributions=("Manjaro" "Ubuntu" "Arch");
declare -a distpackagemgrs=("1" "0" "1");
declare -a packagemgr=("apt-get" "pacman");

dist_count=${#distributions[*]}
usable_mgr="-1"

dist_name=$(lsb_release -a);

for (( i=0; i<=$(( $dist_count -1 )); i++ ))
do
    if [ $(echo "$dist_name" | grep -c "${distributions[$i]}") -gt 0 ]; then
        usable_mgr=${distpackagemgrs[$i]}
        echo "Found Distribution ${distributions[$i]}, will use ${packagemgr[usable_mgr]}"
    fi
done

if [ $usable_mgr == "-1" ]; then
    echo "Err: Linux distibution unknown, will use apt-get"
    usable_mgr="0"
fi

case $usable_mgr in
    "0")
    echo "-- apt-get install --"

    sudo apt-get install python2.7-dev python-pip
    sudo apt-get install libxext-dev python-qt4 qt4-dev-tools build-essential
    sudo apt-get install freeglut3-dev libboost-python-dev
    sudo apt install libftgl-dev ftgl-dev

    ;;
    "1")
    echo "-- pacman installation --"

    sudo pacman -S python2 python-pip
    sudo pacman -S libxext python2-pyqt4 base-devel
    sudo pacman -S freeglut boost
    sudo pacman -S ftgl

    ;;
esac

sudo pip install simplejson
sudo pip install pyopengl

git clone https://github.com/umlaeute/pyftgl.git
cd pyftgl
python setup.py build
sudo python setup.py install
cd ..
rm -rf pyftgl
mkdir temp
chmod -R 777 temp
python main.py
