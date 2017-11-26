import socket
import time
import picamera
import sys
from django.conf import settings
import telebot

from linijapogona.settings_local import (
    ADRESA,
    TOKEN_BOT,
    KORISNIK_ID,
)

telegrambot = telebot.TeleBot(TOKEN_BOT)

class CameraNetwork:
  def __init__(self):
    self.camera = None
    self.server_socket = None
    self.connection = None

  def stop(self):
    self.server_socket.close()
    self.camera.close()
    self.connection.close()
    telegrambot.send_message(KORISNIK_ID, "Zaustavi video stream")

  def record(self):
    self.camera = picamera.PiCamera()
    self.camera.resolution = (640, 480)

    self.camera.framerate = 24
    self.camera.vflip = False

    telegrambot.send_message(KORISNIK_ID, "Aktivan video stream")

    self.server_socket = socket.socket()

    self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.server_socket.bind(('0.0.0.0', 8001))
    self.server_socket.listen(0)

    # Accept a single connection and make a file-like object out of it
    self.connection = self.server_socket.accept()[0].makefile('wb')
    self.camera.start_recording(self.connection, format='h264')

  def photo(self):
    ime = "linija-%s.jpg" % time.strftime("%Y-%m-%d-%H-%M-%S")
    self.camera = picamera.PiCamera()
    self.camera.resolution = (2592, 1944)
    filename = settings.MEDIA_ROOT + '/' + 'camera/' + ime
    self.camera.capture(filename)
    self.camera.close()
    photo_dir = '/home/pi/media/camera/' + ime
    telegrambot.send_photo(KORISNIK_ID, photo=open(photo_dir, 'rb'))
    telegrambot.send_message(KORISNIK_ID, photo_dir)
