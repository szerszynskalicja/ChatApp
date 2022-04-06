from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QCheckBox


class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self._create_form()

    def _create_form(self):
        outer_layout = QVBoxLayout()
        top_layout = QFormLayout()
        top_layout.addRow("Message", QLineEdit())
        outer_layout.addLayout(top_layout)
        options_layout = QVBoxLayout()
        options_layout.addWidget(QCheckBox("CBC"))
        options_layout.addWidget(QCheckBox("EBC"))
        outer_layout.addLayout(top_layout)
        outer_layout.addLayout(options_layout)
        self.setLayout(outer_layout)
