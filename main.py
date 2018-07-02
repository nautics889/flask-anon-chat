import sys
import socket

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow,QPushButton, QMessageBox, QLineEdit
from PyQt5.QtCore import pyqtSlot


def send_message(message):
    try:
        sock = socket.socket()
        sock.connect(('localhost', 3636))
        sock.send(bytes(message, 'utf-8'))
        data = sock.recv(1024)
        sock.close()
        return (data, 1)
    except Exception as msg:
        return (msg, 0)

class Root(QMainWindow):
    def __init__(self):
        super(Root, self).__init__()
        self.title = 'TCP-Client'
        self.left = 110
        self.top = 110
        self.width = 620
        self.height = 480
        self.initUi()

    def initUi(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.statusBar().showMessage('')

        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(280, 20)

        button = QPushButton('Send', self)
        button.setToolTip('Send message')
        button.move(20, 70)
        button.clicked.connect(self.send_slot)

        self.echo = QLabel(self)
        self.echo.move(20, 120)

    @pyqtSlot()
    def send_slot(self):
        message = self.textbox.text()
        status = send_message(message)

        if status[1] is 1:
            self.statusBar().showMessage('Message delivered')
            self.echo.setText('Echo: {}'.format(status[0].decode("utf-8")))
        if status[1] is 0:
            self.statusBar().showMessage('{}'.format(status[0]))

if __name__ == '__main__':
    app = QApplication(sys.argv)

    root = Root()
    root.show()

    sys.exit(app.exec_())