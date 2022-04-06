from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QMainWindow, QLabel, QMenuBar, QMenu, QFormLayout, QLineEdit, QVBoxLayout, QCheckBox,
                             QStatusBar)

from ChatApp.GUI.Widget import Widget


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Chat App")
        self.resize(400, 400)
        self._create_menu_bar()
        self._widget = Widget(self)
        self.setCentralWidget(self._widget)
        self._create_status_bar()

    def _create_menu_bar(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        help_menu = menu_bar.addMenu("&Help")

    def _create_status_bar(self):
        status = QStatusBar()
        status.showMessage("Status Bar")
        self.setStatusBar(status)
