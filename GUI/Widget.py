from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QRadioButton, QDialogButtonBox, \
    QPushButton, QTextEdit, QFileDialog, QProgressBar
import os
import time

import Logic


class Widget(QWidget):
    def __init__(self, parent=None, client=None):
        super().__init__()
        self.outer_layout = QVBoxLayout()
        self._create_form()
        self.client = client
        self.client.set_widget(self)
        self.client.run()
        self._create_enter_buttons()
        self.__create_progress_bar()
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
        button_cbc.setChecked(True)
        button_ebc = QRadioButton("ECB")
        button_ebc.toggled.connect(lambda: self._send_type(button_ebc))
        options_layout.addWidget(button_ebc)
        button_file = QPushButton("Add Files")
        self.file_path = ""
        button_file.clicked.connect(self.__browse_file)
        options_layout.addWidget(button_file)
        self.outer_layout.addLayout(options_layout)

    def __browse_file(self):
        file_path = os.path.abspath(os.getcwd())
        file_window = QFileDialog.getOpenFileName(self, "Open File", file_path, 'Images (*.png *.jpg);;Text files (*.txt *.pdf);; Videos (*.avi)')
        previous_path = self.file_path
        self.file_path = file_window[0]
        if self.file_path:
            if previous_path:
                self.text_box.append("Changed file to: " + self.file_path)
            else:
                self.text_box.append("You have chosen: " + self.file_path + " file")

    def __create_message_form(self):
        top_layout = QFormLayout()
        self.text_box = QTextEdit()
        self.text_box.setReadOnly(True)
        self.text_box.append("message")
        top_layout.addWidget(self.text_box)
        self.message = QLineEdit()
        top_layout.addRow("Message", self.message)
        self.outer_layout.addLayout(top_layout)

    def _create_enter_buttons(self):
        btns = QDialogButtonBox()
        send_button = QPushButton("Send", self)
        send_button.setDefault(False)
        btns.addButton(send_button, QDialogButtonBox.ActionRole)
        send_button.clicked.connect(lambda: self.send_mess())
        self.outer_layout.addWidget(btns)

    def send_mess(self):
        # message or text to sent is chosen
        if self.message.text() or self.file_path:
            self.__progress_bar_actualization()
            if self.message.text():
                self.text_box.append("you: "+self.message.text())
                Logic.send_message(self.message.text(), self.type, self.client)
                #self.client.send(self.message.text())
            if self.file_path:
                self.text_box.append("you: send a file " + str(self.file_path))
                self.file_path = ""
        else:
            self.text_box.append("Please choose a file or message to send")

    def _send_type(self, button):
        if button.isChecked():
            if button.text() == "CBC":
                self.type = "CBC"
            else:
                self.type = "ECB"

    def __create_progress_bar(self):
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setGeometry(10, 340, 200, 25)

    def __progress_bar_actualization(self):
        for i in range(101):
            time.sleep(0.01)
            self.progress_bar.setValue(i)
