from PyQt5.QtWidgets import QWidget, QVBoxLayout, QFormLayout, QLineEdit, QCheckBox


class Widget(QWidget):
    def __init__(self, parent=None):
        super(Widget, self).__init__(parent)
        self._create_form()

    def _create_form(self):
        outerLayout = QVBoxLayout()
        # layout = QFormLayout()
        # layout.addRow("Message", QLineEdit())
        # outer_layout.addLayout(layout)

        topLayout = QFormLayout()
        # Add a label and a line edit to the form layout
        topLayout.addRow("Some Text:", QLineEdit())
        # Create a layout for the checkboxes
        optionsLayout = QVBoxLayout()
        # Add some checkboxes to the layout
        optionsLayout.addWidget(QCheckBox("Option one"))
        optionsLayout.addWidget(QCheckBox("Option two"))
        optionsLayout.addWidget(QCheckBox("Option three"))
        # Nest the inner layouts into the outer layout
        outerLayout.addLayout(topLayout)
        outerLayout.addLayout(optionsLayout)
        self.setLayout(outerLayout)
