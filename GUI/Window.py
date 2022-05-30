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
        self.password = None
        self.client = Client.Client(self.password)
        self._create_menu_bar()
        self.widget = GenKeyWidget(self, self.client)
        self.setCentralWidget(self.widget)

    def create_main_widget(self):
        self.widget = Widget(self, self.client)
        self.setCentralWidget(self.widget)

    def create_s_c_widget(self):
        self.widget = ClientServerWidget(self, self.client)
        self.setCentralWidget(self.widget)

    def _create_menu_bar(self):
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)
        help_menu = menu_bar.addMenu("&Help")


