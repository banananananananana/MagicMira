import io
import os
import picamera
import time
from datetime import datetime
from PIL import Image

camera = picamera.PiCamera()

difference = 20
pixels = 100

width = 1280
height = 960

def compare():
        camera.resolution = (100, 75)
        stream = io.BytesIO()
        camera.capture(stream, format = 'bmp')
        stream.seek(0)
        im = Image.open(stream)
        buffer = im.load()
        stream.close()
        return im, buffer
image1, buffer1 = compare()

timestamp = time.time()

while (True):
        image2, buffer2 = compare()

        changedpixels = 0
        for x in xrange(0, 100):
                for y in xrange(0, 75):
                        pixdiff = abs(buffer1[x,y][1]- buffer2[x,y][1])
                        if pixdiff > difference:
                                changedpixels += 1
        if changedpixels > pixels:
                print 'motion detected, turning on screen'
                os.system('echo 0 > /sys/class/backlight/rpi_backlight/bl_power')
                time.sleep(10)
        if pixels > changedpixels:
                print 'no motion, turning off screen'
                os.system('echo 1 > /sys/class/backlight/rpi_backlight/bl_power')
        image1 = image2
        buffer1 = buffer2
