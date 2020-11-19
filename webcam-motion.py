import io
import os
import picamera
import time
from datetime import datetime
from PIL import Image

camera = picamera.PiCamera()

difference = 20
pixels = 50000

def compare():
        camera.resolution = (640, 480)
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
        for x in xrange(0, 640):
                for y in xrange(0, 480):
                        pixdiff = abs(buffer1[x,y][1]- buffer2[x,y][1])
                        if pixdiff > difference:
                                changedpixels += 1
        if changedpixels > pixels:
                print 'motion detected, turning on screen'
                os.system('/usr/bin/vcgencmd display_power 1')
                camera.resolution = (640, 480)
                camera.rotation = 180
                camera.capture('foo.jpg')
                os.system('gpicview foo.jpg &')
                time.sleep(5)
                os.system('pkill -f "gpicview"')
                time.sleep(10)
        if pixels > changedpixels:
                print 'no motion, turning off screen'
                os.system('/usr/bin/vcgencmd display_power 0')
        image1 = image2
        buffer1 = buffer2
