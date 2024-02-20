# take photo example
# import time
# from picamera2 import Picamera2, Preview

# picam = Picamera2()

# config = picam.create_preview_configuration()
# picam.configure(config)

# picam.start_preview(Preview.QTGL)

# picam.start()
# time.sleep(2)
# picam.capture_file("test-python1.jpg")

# picam.close()

# take 10s video example
# from picamera2 import Picamera2
# from picamera2.encoders import H264Encoder
# import time

# picamera2 = Picamera2()

# video_config = picamera2.create_video_configuration()
# picamera2.configure(video_config)

# encoder = H264Encoder(10000000)
# picamera2.start_recording(encoder, "/home/pi/WAVEGO/RPi/video.h264")

# time.sleep(10)
# picamera2.stop_recording()


# example please read: github.com/raspberrypi/picamera2/tree/main/examples
# chatgpt 4.0: only contain few information about picamera2
# following opencv version: at least can be used as an example. Our opencv
#  data folder is different from the website above. Thus, some CascadeClassifier
#  path may differ. Hope you can fix the problem. I did not figure out how to
#  change the fps or other things, but it should be same as you did in PuppyPi.

#!/usr/bin/python3

import cv2

from picamera2 import Picamera2

# Grab images as numpy arrays and leave everything else to OpenCV.

# face_detector = cv2.CascadeClassifier("/home/pi/WAVEGO/RPi/opencv_data_haarcascades.xml")

cv2.startWindowThread()

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

while True:
    im = picam2.capture_array()

    grey = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    # faces = face_detector.detectMultiScale(grey, 1.1, 5)

    # for (x, y, w, h) in faces:
        # cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0))

    cv2.imshow("Camera", im)
    cv2.waitKey(1)
