from pathlib import Path
from src.ui.main_ui.ui_main import Ui_MainWindow
from src.ui.scann_ui.UiScann import DlgScanner, QtWidgets, QtCore
from src.Nsfw.vic13 import readVICFromFile, getMediaFormVIC
from src.ui.main_ui.NsfwCard import NsfwCard

class UiMain(QtWidgets.QMainWindow, Ui_MainWindow):
    resized: QtCore.pyqtSignal = QtCore.pyqtSignal()
    dlgScann: DlgScanner
    vic_file: str = ''
    VIC: dict = None
    media: list = []
    #Filter Vars
    isFilterChange: bool = True
    filter_media: list = []
    filter_value: float = 0.15
    isFiltered: bool = False

    #Cards Vars
    cards_list: list = []
    current_page: int = 1
    total_pages: int = 0
    viewCards: int = 0

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.progressBar.setVisible(False)
        self.btnListUp.clicked.connect(self.btnListUp_click)
        self.btnListDown.clicked.connect(self.btnListDown_click)
        self.slrFiltro.valueChanged.connect(self.pgbFiltro.setValue)
        self.pgbFiltro.valueChanged.connect(self.changeFilterScore)
        self.btnFiltro.clicked.connect(self.setFilterOnOff)
        self.btnScanner.clicked.connect(self.btnScanner_Click)
        self.btnOpen.clicked.connect(self.btnOpen_Click)
        self.resized.connect(self.__updateView)

    def resizeEvent(self, event):
        self.setCurrentPage(1)
        self.resized.emit()
        return super().resizeEvent(event)

    def changeFilterScore(self):
        fv = self.pgbFiltro.value()
        self.filter_value = fv /100
        self.lblFiltro.setText('%d' % (fv) + '%')
        self.isFilterChange = True

    def setFilterOnOff(self):
        self.isFiltered = not self.isFiltered
        self.slrFiltro.setEnabled(not self.isFiltered)
        self.__updateView()

    def setCurrentPage(self, page: int):
        if (page <= self.total_pages) and (page > 0):
            self.current_page = page
            self.btnListUp.setEnabled(self.current_page > 1)
            self.btnListDown.setEnabled(self.current_page < self.total_pages)
            self.update_lbls()
            return True
        return False

    def update_lbls(self):
        self.lblPages.setText('%d/%d' % (self.current_page, self.total_pages))
        self.lblSelCount.setText('%d/%d' % (self.viewCards, len(self.filter_media)) + ('-[F]' if self.isFiltered else ''))

    def btnListUp_click(self):
        if self.setCurrentPage(self.current_page - 1):
            self.__updateView()

    def btnListDown_click(self):
        if self.setCurrentPage(self.current_page + 1):
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
        if not self.isFiltered:
            self.filter_media = self.media
            self.isFilterChange = True
            return
        if self.isFilterChange:
            self.filter_media = []
            for media in self.media:
                if float(media['Comments']) >= self.filter_value:
                    self.filter_media.append(media)
            self.isFilterChange = False

    def clearCardList(self):
        for card in self.cards_list:
            self.removeCard(card)
        self.cards_list.clear()

    def removeCard(self, card: NsfwCard):
        self.cards.removeWidget(card)
        self.cards_list.remove(card)
        card.deleteLater()
        del card

    def card_remove_me(self, card: NsfwCard):
        self.media.remove(card.data)
        if self.isFiltered:
            self.filter_media.remove(card.data)
        self.removeCard(card)
        self.update_lbls()

    def getPageMedia(self, cards_for_page: int):
        page_media: list = []
        start: int = (self.current_page - 1) * cards_for_page
        end: int = start + cards_for_page
        if end > len(self.filter_media):
            end = len(self.filter_media)
        for idx in range(start, end):
            page_media.append(self.filter_media[idx])
        return page_media

    def __updateView(self):
        if not self.VIC:
            return
        self.__filterMedia()
        if not self.filter_media:
            return
        col, row, cardW, cardH = (0, 0, 200, 200)
        width, height = (self.listView.width(), self.listView.height())
        colums, rows = (round(width / (cardW + 10)), round(height / (cardH + 10)))
        cards_for_page = colums * rows
        complet_pages, incomplet_page = divmod(len(self.filter_media), cards_for_page)
        self.total_pages = complet_pages + 1 if(incomplet_page > 0)else 0
        page_media = self.getPageMedia(cards_for_page)
        self.clearCardList()
        base_path = str(Path(self.vic_file).parent)
        for item in page_media:
            item = NsfwCard(self.listView, item, cardW, cardH, base_path)
            item.remove_me.connect(self.card_remove_me)
            self.cards_list.append(item)
            if col >= colums:
                col = 0
                row += 1
            self.cards.addWidget(item, row, col)
            col += 1
        self.viewCards = self.current_page * cards_for_page
        if self.viewCards > len(self.filter_media):
            self.viewCards = len(self.filter_media)
        self.update_lbls()

    def __loadReportFile(self):
        if self.vic_file:
            self.lblStatus.setText(self.vic_file)
            self.VIC = readVICFromFile(self.vic_file)
            self.media = getMediaFormVIC(self.VIC)
            self.__updateView()
