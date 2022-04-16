from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QLabel, QMenuBar, QMenu, QFormLayout, QLineEdit, QVBoxLayout, QCheckBox,
                             QStatusBar, QProgressBar)

from GUI.GenKeyWidget import GenKeyWidget


class GenKeyWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Generate Key")
        self.resize(400, 400)
        self._widget = GenKeyWidget(self)
        self.setCentralWidget(self._widget)


