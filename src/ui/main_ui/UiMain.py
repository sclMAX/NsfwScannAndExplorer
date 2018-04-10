import webbrowser
from src.ui.main_ui.ui_main import Ui_MainWindow
from src.ui.scann_ui.UiScann import DlgScanner, QtWidgets
from src.Nsfw.vic13 import readVICFromFile, getMediaFormVIC
from src.ui.main_ui.NsfwCard import NsfwCard

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
        self.btnList.clicked.connect(self.__updateView)
        self.slrFiltro.valueChanged.connect(self.pgbFiltro.setValue)
        self.pgbFiltro.valueChanged.connect(self.changeFilterScore)
        self.btnFiltro.clicked.connect(self.setFilterOnOff)
        self.btnScanner.clicked.connect(self.btnScanner_Click)
        self.btnOpen.clicked.connect(self.btnOpen_Click)

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
        col, row = (0, 0)
        for _ in range(10):
            media_item = self.__filterMedia().next()
            print(media_item)
            if not media_item:
                break
            if col > 3:
                col = 0
                row += 1    
            item = NsfwCard(self.listView, media_item)
            self.cards.addWidget(item, col, row)
            col += 1

    def __loadReportFile(self):
        if self.vic_file:
            self.lblStatus.setText(self.vic_file)
            self.VIC = readVICFromFile(self.vic_file)
            self.media = getMediaFormVIC(self.VIC)
            self.__updateView()

    def openImage(self, item):
        imagePath = item.toolTip()
        webbrowser.open_new_tab(imagePath)
