from src.ui.main_ui.ui_main import Ui_MainWindow
from PyQt5 import QtWidgets
from src.utils.constants import NORMAL, DANGER, WARNING
from src.Nsfw.nsfw_scann import NsfwScann
from src.Nsfw.vic13 import readVICFromFile, genNewVic



class UiMain(QtWidgets.QMainWindow, Ui_MainWindow):
    nsfw = None
    VIC = {}
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.progressBar.setVisible(False)
        self.nsfw = NsfwScann(self)
        self.nsfw.status.connect(self.setStatus)
        self.nsfw.progressMax.connect(self.progressBar.setMaximum)
        self.nsfw.progress.connect(self.progressBar.setValue)
        self.btnScannFolder.clicked.connect(self.btnScannFolder_Click)
        self.btnOpenFolder.clicked.connect(self.btnOpenFolder_Click)
    
    def btnScannFolder_Click(self):
        
        #TODO codigo para abrir Directorio
        self.VIC = genNewVic()
        self.nsfw.scannFolder('icons') #TODO dummy
    
    def btnOpenFolder_Click(self):
        #TODO Codigo para abrir archivo VIC
        self.VIC = readVICFromFile('/home/max/Documentos/Proyectos/Forense/DatosPara Pruebas/Export/Export.json')#TODO dummy
        self.nsfw.scannVIC(self.VIC)
    
    def setStatus(self, msg):
        self.lblOpenFolder.setText(msg.msg)
        self.lblOpenFolder.repaint()
        
