from PyQt5 import QtCore
import PyQt5.QtWidgets as QtW
import sys
#import GUI.GenKeyWindow as GKGUI
import GUI.Window as mainW

PUBLIC_KEY = None
PRIVATE_KEY = None
SESSION_KEY = b"V%u\x87\x82e\xbc>\xa0D\x07B\xf8\xaa\xec\x1c"

if __name__ == '__main__':
    app = QtW.QApplication(sys.argv)
 #   window = GKGUI.GenKeyWindow()
  #  window.show()
    main_window = mainW.Window()
    main_window.show()
    sys.exit(app.exec_())

