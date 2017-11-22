# Linija pogona

# Koraci do konačnog projekta
- HTML/CSS izrada korisničkog sučelja
- REST API login za korisnika linije
- RPi server na kojemu je instaliran
- Web kamera za učitavanje radnog naloga
- mbed i RPi komunikacija pomoću I2C

# Upute za RPi model 3
1. Debian Linux, RASPBIAN JESSIE LITE
   - Instalacija na sdcard, min 8GB
       unzip -p 2017-04-10-raspbian-jessie.zip | sudo dd of=/dev/sdX bs=4096 status=progress
   - Spoji se na RPi sa PC preko HDMI i tipkovnice ili UTP kabelom
2. Podesiti na headless
   - Postavi na sdcard datoteku ssh za spajanje sa RPi UTP kabelom
   - Opcija sa HDMI i tipkovnicom je jednostavnija i potrebno je samo jednom napraviti
       - u RPi je potrebno unijeti sdcard sa raspbian OS
       - login podaci: username:pi, password:raspberry(pazi na US-keyboard)
       - sudo raspi-config(1.proširi sdcard na maxsize, 2. promijeni lozinku, 3.uključi kameru, ssh, I2C)
       - sudo vim.tiny /etc/wpa_supplicant/wpa_supplicant.conf i dodati
            network={
              ssid="SSID"
              psk="PASSWORD"
            }
       - sudo reboot
   - Spoji se sa RPi preko WIFI
       - ssh pi@raspberrypi
3. Pokreni skriptu za instalaciju
   - preuzmi datoteku "linija-pogona-vX" sa "https://github.com/mariomitte/"
       - preporuka je staviti datoteku u mapu "workspace" ili nešto slično tome
   - raspakiraj i pokreni skriptu "postavi.sh"
       - sudo bash
       - chmod 777 postavi.sh
       - ./postavi.sh

# Upute za Kameru
1. Gumb PLAY je za pokretanje video streama,
2. Gumb STOP zaustavlja video stream,
3. Za snimanje dokumenta dovoljno je pritisnuti gumb KAMERA,

- za reprodukciju VIDEO streama preporučuje se koristiti "VLC media player" i
koristiti opciju iz "File/Mrežne veze" gdje se unosi "Mrežni URL"
- koristi se slijedeći format za "Mrežni URL"
        tcp/h264://moja_RPi_adresa:8001/
- dokumentacija potrebna za rad sa RPi kamerom
"http://picamera.readthedocs.io/en/release-1.10/recipes1.html#recording-to-a-network-stream"

# Upute za Django
1. source myenv/bin/activate
2. cd workspace/linija-pogona-vX/linija_pogona_vX/
3. migracije za bazu podataka i izradu administratorskog racuna
   - python server/manage.py makemigrations pogon
   - python server/manage.py makemigrations api
   - python server/manage.py migrate
   - python server/manage.py createsuperuser
   - python server/manage.py runserver 0.0.0.0:8000
4. otvori u browseru na "localhost:8000" ili "IP.adresa"

