from PyQt5.QtWidgets import QWidget, QGridLayout, QMessageBox, QLineEdit,  QPushButton
import os
import Logic


class GenKeyWidget(QWidget):
    def __init__(self, parent=None, client=None):
        super().__init__()
        self.layout = QGridLayout()
        self._create_widgets()
        self.parent = parent
        self.client = client
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
            Logic.create_keys(self.lineEdit_password.text(), './')
            # switch to message window
            #self.window().hide()
            self.parent.client.password = self.lineEdit_password.text()
            self.parent.create_s_c_widget()
        else:
            msg = QMessageBox()
            msg.setText('Passwords are not the same, try again!')
            msg.exec_()

    def _login(self):
        Logic.check_password(self.lineEdit_password.text())
        #self.window().hide()
        self.parent.client.password = self.lineEdit_password.text()
        self.parent.create_s_c_widget()
