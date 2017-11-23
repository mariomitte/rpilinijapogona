import time
import smbus
import RPi.GPIO as GPIO

# I2C
bus = smbus.SMBus(1)
address = 0x04

GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
pwm_out1=GPIO.PWM(12,50)
pwm_out2=GPIO.PWM(13,50)

motor_a = 8.0
motor_b = 7.0

def speed_control(speed):
    global motor_a
    global motor_b

    if (speed == "brze" and motor_a < 8.5 and motor_b > 6.5):
        motor_a = motor_a + 0.1
        motor_b = motor_b - 0.1

    if (speed == "sporije" and motor_a >7.5 and motor_b < 7.5):
        motor_a = motor_a - 0.1
        motor_b = motor_b + 0.1

    print("motor_a:{} motor_b:{}".format(motor_a,motor_b))
    print(motor_b)


def motor_control(direction):

    global motor_a
    global motor_b
    global pwm_out1
    global pwm_out2

    if (direction == "lijevo"):
        value = 1
        bus.write_byte(address, value)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)
        pwm_out1=GPIO.PWM(12,50)
        pwm_out2=GPIO.PWM(13,50)
        pwm_out1.start(motor_b)
        pwm_out2.start(motor_b)

    if (direction == "desno"):
        value = 2
        bus.write_byte(address, value)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(12, GPIO.OUT)
        GPIO.setup(13, GPIO.OUT)
        pwm_out1=GPIO.PWM(12,50)
        pwm_out2=GPIO.PWM(13,50)
        pwm_out1.start(motor_a)
        pwm_out2.start(motor_a)

    if (direction == "pauziraj"):
        value = 8
        bus.write_byte(address, value)
        pwm_out1.stop()
        pwm_out2.stop()
        GPIO.cleanup()

    if (direction == "stop"):
        value = 9
        bus.write_byte(address, value)
        GPIO.cleanup()
