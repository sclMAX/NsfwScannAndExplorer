from src.ui.main_ui.ui_main import Ui_MainWindow
from PyQt5 import QtWidgets

from src.Nsfw.nsfw_classify import NsfwClassify

class UiMain(QtWidgets.QMainWindow, Ui_MainWindow):
    nsfw = None
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.nsfw = NsfwClassify(self)
        self.nsfw.status.connect(self.setStatus)
        self.btnScannFolder.clicked.connect(self.btnScannFolder_Click)
    
    def btnScannFolder_Click(self):
        self.nsfw.scann('Hola mundo')
    
    def setStatus(self, msg):
        self.lblOpenFolder.setText(msg.msg)
        self.lblOpenFolder.repaint()
        
