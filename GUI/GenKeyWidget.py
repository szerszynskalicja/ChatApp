import time
from PyQt5.QtWidgets import QWidget, QGridLayout, QMessageBox,QLabel,QVBoxLayout, QFormLayout, QLineEdit, QRadioButton, QDialogButtonBox, \
    QPushButton, QTextEdit, QFileDialog, QProgressBar
import os

import GUI.Window as mainGUI
import Server


class GenKeyWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.layout = QGridLayout()
        self._create_widgets()
        self.setLayout(self.layout)

    def _create_widgets(self):
        if os.path.isfile('./privateKey.pem') and os.path.isfile('./publicKey.pem'):
            self.lineEdit_password = QLineEdit()
            self.lineEdit_password.setPlaceholderText('Please enter your Password')
            self.layout.addWidget(self.lineEdit_password, 0, 0)
            confirm_button = QPushButton('Confirm')
            confirm_button.clicked.connect(self._login)
            self.layout.addWidget(confirm_button, 2, 0, 1, 2)
        else:
            self.lineEdit_password = QLineEdit()
            self.lineEdit_password.setPlaceholderText('Please enter your Password')
            self.layout.addWidget(self.lineEdit_password, 0, 0)

            self.lineEdit_password2 = QLineEdit()
            self.lineEdit_password2.setPlaceholderText('Confirm password')
            self.layout.addWidget(self.lineEdit_password2, 1, 0)
            confirm_button = QPushButton('Confirm password for RSA keys')
            confirm_button.clicked.connect(self._check_password)
            self.layout.addWidget(confirm_button, 2, 0, 1, 2)

    def _check_password(self):
        if self.lineEdit_password.text() == self.lineEdit_password2.text():
            self.logged = True
            Server.create_keys(self.lineEdit_password.text())
            # switch to message window
            print("switch")
            window = mainGUI.Window()
            window.show()
            self.close()
        else:
            self.logged = False
            msg = QMessageBox()
            msg.setText('Passwords are not the same, try again!')
            msg.exec_()

    def _login(self):
        self.logged = Server.check_password(self.lineEdit_password)
