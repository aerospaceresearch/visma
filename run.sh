#!/bin/bash
if [ $(uname -s) == "Linux" ]; then
  declare -a distributions=("Manjaro" "Ubuntu" "Arch");
  declare -a distpackagemgrs=("1" "0" "1");
  declare -a packagemgr=("apt-get" "pacman");

  dist_count=${#distributions[*]}
  usable_mgr="-1"

  dist_name=$(lsb_release -a);

  for (( i=0; i<=$(( dist_count -1 )); i++ ))
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
      sudo apt-get install python3.6-dev python-pip -y
      sudo apt-get install libxext-dev python3-qt5 qtdeclarative5-dev build-essential  -y
      sudo apt-get install freeglut3-dev libboost-python-dev -y
      sudo apt install libftgl-dev ftgl-dev -y
      sudo apt install python-opengl -y
      ;;
      "1")
      echo "-- pacman installation --"
      sudo pacman -S python3 python-pip -y
      sudo pacman -S libxext python3-pyqt5 base-devel -y
      sudo pacman -S freeglut boost -y
      sudo pacman -S ftgl -y
      sudo pacman -S python-opengl -y
      ;;
  esac
fi

if [ $(uname -s) == "Darwin" ]; then
  sudo easy_install pip
  sudo brew install qt5 -y
  sudo brew install sip --with-python3.6 -y
  sudo brew install pyqt5 --with-python3.6 -y
  sudo brew install freeglut -y
  sudo brew install ftgl -y
fi

sudo pip install simplejson
sudo pip install pyopengl
sudo pip install matplotlib

mkdir local
chmod -R 777 local
