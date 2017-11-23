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
echo "Preuzmi git\n"
sudo apt-get -y install git

#echo "\n"
#echo "Preuzmi projekt linijapogona\n"
#cd /home/pi/
#git clone https://github.com/mariomitte/rpilinijapogona.git

echo "\n"
echo "Preuzmi Python biblioteke\n"
sudo apt-get install -y build-essential
sudo apt-get install -y python3-dev
sudo apt-get install -y python3-smbus
sudo apt-get install -y python3-pip
sudo apt-get install -y openssh-server
sudo apt-get install -y python3-rpi.gpio
sudo apt-get install -y python3-picamera
sudo apt-get install -y postgresql 
sudo apt-get install -y postgresql-contrib
sudo apt-get install -y libpq-dev 
sudo apt-get install -y python3-dev
sudo apt-get install -y supervisor

echo "\n"
echo "Instaliraj potrebne biblioteke za rad sa Django-om"
cd linijapogona
sudo pip3 install -r requirements.txt

echo "\n"
echo "Kraj skripte."
