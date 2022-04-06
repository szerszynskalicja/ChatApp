from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QCheckBox, QRadioButton, QDialogButtonBox, \
    QPushButton


class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self.outer_layout = QVBoxLayout()
        self._create_form()
        self._create_enter_buttons()
        self.setLayout(self.outer_layout)

    def _create_form(self):
        self.__create_message_form()
        self.__create_buttons()

    def __create_buttons(self):
        self.type = ""
        options_layout = QVBoxLayout()
        button_cbc = QRadioButton("CBC")
        button_cbc.toggled.connect(lambda: self._send_type(button_cbc))
        options_layout.addWidget(button_cbc)
        button_ebc = QRadioButton("EBC")
        button_ebc.toggled.connect(lambda: self._send_type(button_ebc))
        options_layout.addWidget(button_ebc)
        self.outer_layout.addLayout(options_layout)

    def __create_message_form(self):
        top_layout = QFormLayout()
        top_layout.addRow("Message", QLineEdit())
        self.outer_layout.addLayout(top_layout)

    def _create_enter_buttons(self):
        btns = QDialogButtonBox()
        send_button = QPushButton("Send", self)
        send_button.setDefault(False)
        btns.addButton(send_button, QDialogButtonBox.ActionRole)
        send_button.clicked.connect(lambda: self.send_mess())
        self.outer_layout.addWidget(btns)

    def send_mess(self):
        if self.type == "CBC" or self.type == "EBC":
            print("Wysle")
            print("Tu będzie coś wywoływane xd")
        else:
            print("Error")

    def _send_type(self, button):
        if button.text() == "CBC":
            if button.isChecked():
                self.type = "CBC"
                print("cos")
        else:
            if button.isChecked():
                self.type = "EBC"
                print("nie")