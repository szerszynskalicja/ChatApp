import PyQt5 as Qt
import PyQt5.QtWidgets as QtW
import GUI.Window as GUI
import sys

app = QtW.QApplication(sys.argv)
window = GUI.Window()
window.show()
sys.exit(app.exec_())
