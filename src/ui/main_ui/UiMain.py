from src.ui.main_ui.ui_main import Ui_MainWindow
from PyQt5 import QtWidgets
from src.ui.scann_ui.UiScann import DlgScanner



class UiMain(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.progressBar.setVisible(False)
        self.btnScannFolder.clicked.connect(self.btnScannFolder_Click)
        self.btnOpenFolder.clicked.connect(self.btnOpenFolder_Click)
    
    def btnScannFolder_Click(self):
        self.dlgScann = DlgScanner(self) 
        self.dlgScann.exec_()
    
    def btnOpenFolder_Click(self):
        pass
    
    def setStatus(self, msg):
        self.lblOpenFolder.setText(msg.msg)
        self.lblOpenFolder.repaint()
        
