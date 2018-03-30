from src.ui.scann_ui.ui_nsfw_scann import Ui_dlgNsfwScanner
from PyQt5 import QtWidgets

class DlgScanner(QtWidgets.QDialog, Ui_dlgNsfwScanner):

    def __init__(self):
        super().__init__()
        self.setupUi(self)