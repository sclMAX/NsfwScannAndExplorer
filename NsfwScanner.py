# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from src.ui.scann_ui.UiScann import DlgScanner

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = DlgScanner()
    MainWindow.show()
    sys.exit(app.exec_())

