from PyQt5 import QtWidgets
from src.ui.main_ui.UiMain import UiMain

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = UiMain()
    MainWindow.show()
    sys.exit(app.exec_())

