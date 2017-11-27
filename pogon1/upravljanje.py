# Upravljanje GPIO pinom sa I2C
# Prilagođeno za zahtjeve projekta: linija pogona
import time
import smbus
import RPi.GPIO as GPIO

# I2C
bus = smbus.SMBus(1)
address = 0x04

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Pohrani ovdje dozvoljene UID kartice
# byte_list = []

# PWM
motor_a = 8.0
motor_b = 7.0

# Promjena brzine
def speed_control(speed):
    global motor_a
    global motor_b

    if (speed == 'brze' and motor_a < 8.5 and motor_b > 6.5):
        value = 3
        motor_a = motor_a + 0.1
        motor_b = motor_b - 0.1
        bus.write_byte(address, value)

    if (speed == 'sporije' and motor_a >7.5 and motor_b < 7.5):
        value = 4
        motor_a = motor_a - 0.1
        motor_b = motor_b + 0.1
        bus.write_byte(address, value)

    print('motor_a:{} motor_b:{}'.format(motor_a,motor_b))

# Promjena smjera, pauziraj, zaustavi
def motor_control(direction):

    if (direction == 'lijevo'):
        value = 1
        bus.write_byte(address, value)

    if (direction == 'desno'):
        value = 2
        bus.write_byte(address, value)

    if (direction == 'pauziraj'):
        value = 8
        bus.write_byte(address, value)

    if (direction == 'stop'):
        value = 9
        bus.write_byte(address, value)

# Nije povezano sa čitačem kartice. Arduino sa čitačem kartice odlučuje o listi dozvoljenih korisnika/operatera
# Aktiviraj slijedeću funkciju koliko odlučuje linija pogona
# def readNumber():
#     global byte_list
#
#     arduino = bus.read_byte_data(address, 2)
#
#     if arduino not in byte_list:
#         motor_control('stop')
#         # Dodaj metode za upravljanje otvaranjem releja, svjetla, itd.
#         # Metode zatvori, ugasi
#         print('Nema pristupa. UID: {}'.format(arduino))
#     else:
#         # Dodaj metode za upravljanje otvaranjem releja, svjetla, itd.
#         # Metode otvori, upali
#         print('Pristup odobren. UID: {}'.format(arduino))
#     return arduino
