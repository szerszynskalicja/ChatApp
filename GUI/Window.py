from PyQt5 import QtCore
from PyQt5.QtWidgets import (QMainWindow, QLabel, QMenuBar)

from GUI.Widget import Widget
from GUI.GenKeyWidget import GenKeyWidget
from GUI.ClientServerWidget import ClientServerWidget
import Client

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Chat App")
        self.resize(400, 400)
        self.client = Client.Client()
        self._create_menu_bar()
        self._widget = GenKeyWidget(self, self.client)
        self.setCentralWidget(self._widget)

    def create_main_widget(self):
        self._widget = Widget(self, self.client)
        self.setCentralWidget(self._widget)

    def create_s_c_widget(self):
        self._widget = ClientServerWidget(self, self.client)
        self.setCentralWidget(self._widget)

    def _create_menu_bar(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        help_menu = menu_bar.addMenu("&Help")


