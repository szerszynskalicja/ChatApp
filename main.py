import PyQt5 as Qt
import PyQt5.QtWidgets as QtW
import GUI.GenKeyWindow as GKGUI
import sys
import time
import os

if __name__ == '__main__':
    app = QtW.QApplication(sys.argv)
    win = GKGUI.GenKeyWindow()
    win.show()
    sys.exit(app.exec_())
