import socket
import sys
from PySide2.QtWidgets import*
from PySide2.QtGui import*
from PySide2 import QtCore

UDP_IP = "127.0.0.1"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP

sock.connect((UDP_IP, UDP_PORT))
# example event handler
def quit_app():
    global application
    print("Quit!")
    application.exit()


# base application object for our app
application = QApplication(sys.argv)

# Create a Window
window = QWidget()
window.setWindowTitle("View Image")

# button
button = QPushButton("Quit", window)

# on click handler
button.clicked.connect(quit_app)

# set up the label widget to display the pic
label = QLabel(window)
label.setPixmap(picture)
label.setGeometry(QtCore.QRect(10, 40, picture.width(), picture.height()))

# embiggen the window to correctly fit the pic
window.resize(picture.width()+20, picture.height()+100)
window.show()

# Let QT do its thing
sys.exit(application.exec_())

data, addr = sock.recvfrom(65536)
print("received message:", data)

# Load Pic
picture = QPixmap("background.png")