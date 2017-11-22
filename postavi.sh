#! /bin/bash
#
# Provjera nadogradnji i preuzimanje/instalacija potrebnih
# datoteka/programa za projekt "Linija pogona"
#

echo "\n"
echo "Prvo update\n"
sudo apt-get update

echo "\n"
echo "Preuzmi nadogradnje\n"
sudo apt-get -y upgrade

echo "\n"
echo "Instalacija Python biblioteka\n"
sudo apt-get install -y build-essential python3-dev
sudo apt-get install -y python3-smbus
sudo apt-get install -y python3-pip
sudo apt-get install -y openssh-server
sudo apt-get install -y python3-rpi.gpio
sudo apt-get install -y python3-picamera

echo "sada Django\n"
sudo pip3 install virtualenv
echo "\n"
echo "Instaliraj potrebne biblioteke za rad sa Django-om u venv"
sudo pip3 install -r requirements.txt

echo "\n"
echo "Kraj skripte."
