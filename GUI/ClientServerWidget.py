from PyQt5.QtWidgets import QWidget, QGridLayout, QMessageBox, QLineEdit,  QPushButton
import socket

class ClientServerWidget(QWidget):
    def __init__(self, parent=None, client=None, password=None):
        super().__init__()
        self.layout = QGridLayout()
        self._create_widgets()
        self.parent = parent
        self.client = client
        self.setLayout(self.layout)

    def _create_widgets(self):
        self.lineServer = QLineEdit()
        self.lineServer.setPlaceholderText('Please enter IP addres of the server')
        self.layout.addWidget(self.lineServer, 0, 0)
        confirm_button = QPushButton('Confirm')
        confirm_button.clicked.connect(self._find_server)
        self.layout.addWidget(confirm_button, 2, 0, 1, 2)

    def _find_server(self):
        try:
            self.client.sock.connect((self.lineServer.text(), 10000))
        except socket.error as exc:
            msg = QMessageBox()
            msg.setText("You can't connect to this server")
            msg.exec_()
        else:
            self.parent.create_main_widget()
