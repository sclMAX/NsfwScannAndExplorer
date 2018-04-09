from pathlib import Path
import webbrowser
from src.ui.main_ui.ui_main import Ui_MainWindow
from src.ui.scann_ui.UiScann import DlgScanner, QtWidgets, QtGui
from src.Nsfw.vic13 import readVICFromFile, getMediaFormVIC

class VicMediaListItem(QtWidgets.QListWidgetItem):
    __media_item: dict
    def __init__(self, media_item: dict):
        super().__init__()
        self.__media_item = media_item
        self.__setup()

    def __setup(self):
        score = float(self.__media_item.get('Comments'))
        file_path = self.__media_item.get('RelativeFilePath')
        miniature = self.__media_item.get('Miniature')
        self.setText('{}%'.format(round(score * 100)))
        self.setToolTip(file_path)
        if miniature:
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(str(Path(miniature))), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.setIcon(icon)
    
    def getMedia(self):
        return self.__media_item
    
    


class UiMain(QtWidgets.QMainWindow, Ui_MainWindow):
    dlgScann: DlgScanner
    vic_file: str = ''
    VIC: dict = None
    media: list = []
    #Filter Vars
    filter_value: float = 0.15
    isFiltered: bool = False

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.progressBar.setVisible(False)
        self.btnGrid.clicked.connect(self.changeViewMode)
        self.btnList.clicked.connect(self.changeViewMode)
        self.slrFiltro.valueChanged.connect(self.pgbFiltro.setValue)
        self.pgbFiltro.valueChanged.connect(self.changeFilterScore)
        self.btnFiltro.clicked.connect(self.setFilterOnOff)
        self.btnScanner.clicked.connect(self.btnScanner_Click)
        self.btnOpen.clicked.connect(self.btnOpen_Click)
        self.listReporte.itemDoubleClicked.connect(self.openImage)

    def changeViewMode(self):
        vs: bool = self.listReporte.isWrapping()
        self.btnList.setEnabled(not vs)
        self.btnGrid.setEnabled(vs)
        self.listReporte.setWrapping(not vs)

    def changeFilterScore(self):
        fv = self.pgbFiltro.value()
        self.filter_value = fv /100
        self.lblFiltro.setText('%d' % (fv) + '%')

    def setFilterOnOff(self):
        self.isFiltered = not self.isFiltered
        self.slrFiltro.setEnabled(not self.isFiltered)
        self.__updateView()

    def btnScanner_Click(self):
        self.dlgScann = DlgScanner(self)
        self.dlgScann.exec_()

    def btnOpen_Click(self):
        self.vic_file, _ = QtWidgets.QFileDialog.getOpenFileName(self, caption='Abrir Reporte...', filter='*.json')
        self.__loadReportFile()

    def setStatus(self, msg):
        self.lblOpenFolder.setText(msg.msg)
        self.lblOpenFolder.repaint()

    def __filterMedia(self):
        filter_media = self.media
        ff = lambda media: (float(media['Comments']) >= self.filter_value) if self.isFiltered else True
        return filter(ff, filter_media)

    def __updateView(self):
        self.listReporte.clear()
        for media_item in self.__filterMedia():
            item = VicMediaListItem(media_item)
            self.listReporte.addItem(item)

    def __loadReportFile(self):
        if self.vic_file:
            self.lblStatus.setText(self.vic_file)
            self.VIC = readVICFromFile(self.vic_file)
            self.media = getMediaFormVIC(self.VIC)
            self.__updateView()

    def openImage(self, item):
        imagePath =item.toolTip()
        webbrowser.open_new_tab(imagePath)