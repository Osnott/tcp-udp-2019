import sys

import cv2
from PySide2 import QtCore, QtGui, QtWidgets
import threading

class CameraDisplay(QtWidgets.QLabel):
  def __init__(self):
    super(CameraDisplay, self).__init__()

  def updateFrame(self, image):
    self.setPixmap(QtGui.QPixmap.fromImage(image))

class ControlCenter(QtWidgets.QWidget):
  up_camera_signal = QtCore.Signal(QtGui.QImage)
  up_camera = None

  def __init__(self):
    super(ControlCenter, self).__init__()
    self.up_camera = CameraDisplay()
    self.up_camera_signal.connect(self.up_camera.updateFrame)

    grid = QtWidgets.QGridLayout()
    grid.setSpacing(10)

    grid.addWidget(self.up_camera, 0, 0)

    self.setLayout(grid)

    self.setGeometry(300, 300, 350, 300)
    self.setWindowTitle('Control Center')
    self.show()

  def up_camera_callback(self, data):
    '''This function gets called by an external thread'''
    try:
      image = QtGui.QImage(data[0], data[1], data[2], data[3], QtGui.QImage.Format_RGB888)
      self.up_camera_signal.emit(image)

    except Exception as e:
      print(e)

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)
        # self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), jpeg_quality]
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        success, image = self.video.read()
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        return image.data, width, height, bytesPerLine

class AThread(threading.Thread):
  def run(self, camera):
    ControlCenter().up_camera_callback(camera.get_frame())

camera = VideoCamera()

if __name__ == "__main__":
  app = QtWidgets.QApplication(sys.argv)
  ex = ControlCenter()
  AThread().run(camera)
  sys.exit(app.exec_())