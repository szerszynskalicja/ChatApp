from PyQt5 import QtCore
import PyQt5.QtWidgets as QtW
import sys
#import GUI.GenKeyWindow as GKGUI
import GUI.Window as mainW

PUBLIC_KEY = None
PRIVATE_KEY = None
SESSION_KEY = None

if __name__ == '__main__':
    app = QtW.QApplication(sys.argv)
 #   window = GKGUI.GenKeyWindow()
  #  window.show()
    main_window = mainW.Window()
    main_window.show()
    sys.exit(app.exec_())

