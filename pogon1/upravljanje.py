import time
import smbus
import RPi.GPIO as GPIO

# I2C
bus = smbus.SMBus(1)
address = 0x04

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

motor_a = 8.0
motor_b = 7.0

def speed_control(speed):
    global motor_a
    global motor_b

    if (speed == "brze" and motor_a < 8.5 and motor_b > 6.5):
        value = 3
        motor_a = motor_a + 0.1
        motor_b = motor_b - 0.1
        bus.write_byte(address, value)

    if (speed == "sporije" and motor_a >7.5 and motor_b < 7.5):
        value = 4
        motor_a = motor_a - 0.1
        motor_b = motor_b + 0.1
        bus.write_byte(address, value)

    print("motor_a:{} motor_b:{}".format(motor_a,motor_b))


def motor_control(direction):

    if (direction == "lijevo"):
        value = 1
        bus.write_byte(address, value)

    if (direction == "desno"):
        value = 2
        bus.write_byte(address, value)

    if (direction == "pauziraj"):
        value = 8
        bus.write_byte(address, value)

    if (direction == "stop"):
        value = 9
        bus.write_byte(address, value)

def readNumber():
    byte_list = []

    #arduino = bus.read_i2c_word_data(address, 0)
    arduino = bus.read_byte_data(address, 2)
    #number = bus.read_byte(address)
    #number = bus.read_byte_data(address, 1)

    # for c in range(arduino):
    #     rfid += chr(arduino[c])

    #rfid.append( (arduino << 16) )

    #print(rfid)
    #return "Arduino: %d" % int(rfid, 16)
    return arduino
