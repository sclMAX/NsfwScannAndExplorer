from pathlib import Path
import json
from src.ui.main_ui.ui_main import Ui_MainWindow
from src.ui.scann_ui.UiScann import DlgScanner, QtWidgets, QtCore, QtGui
from src.Nsfw.vic13 import readVICFromFile, getMediaFormVIC, updateMedia
from src.ui.main_ui.NsfwCard import NsfwCard

class UiMain(QtWidgets.QMainWindow, Ui_MainWindow):
    resized: QtCore.pyqtSignal = QtCore.pyqtSignal()
    dlgScann: DlgScanner
    vic_file: str
    save_file: str
    VIC: dict = None
    #Media Vars
    media: list = []
    filter_media: list = []
    undo_media: list = []
    isChanged: bool = False
    #Filter Vars
    isFilterChange: bool = True
    filter_value: float = 0.15
    isFiltered: bool = False
    isFilterInvert: bool = False

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
        self.btnFiltro_Invertir.clicked.connect(self.setInvertFilter)
        self.btnScanner.clicked.connect(self.btnScanner_Click)
        self.btnOpen.clicked.connect(self.btnOpen_Click)
        self.btnSave.clicked.connect(self.btnSave_click)
        self.btnUndo.clicked.connect(self.undo)
        self.resized.connect(self.__updateView)

    oldDir = 0
    whellCount = 0
    def wheelEvent(self, event: QtGui.QWheelEvent):
        direction = event.angleDelta().y()
        if direction != self.oldDir:
            self.oldDir = direction
            self.whellCount = 0
        self.whellCount += 1
        if self.VIC and self.whellCount > 2:
            page: int = self.oldDir // 120
            if self.setCurrentPage(self.current_page - page):
                self.__updateView()
            self.whellCount = 0

    def resizeEvent(self, event):
        self.setCurrentPage(1)
        self.resized.emit()
        return super().resizeEvent(event)

    def changeFilterScore(self):
        fv = self.pgbFiltro.value()
        self.filter_value = fv /100
        tf = '< ' if self.isFilterInvert else '> '
        self.lblFiltro.setText('%s%d%s' % (tf, fv, '%'))
        self.isFilterChange = True

    def setInvertFilter(self):
        self.isFilterInvert = not self.isFilterInvert
        self.btnFiltro_Invertir.setChecked(self.isFilterInvert)
        self.changeFilterScore()
        if self.isFiltered:
            self.isFilterChange = True
            self.__updateView()

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

    def undo(self):
        if self.undo_media:
            data = self.undo_media.pop()
            if not data in self.media:
                self.media.append(data)
            if self.isFiltered and not data in self.filter_media:
                self.filter_media.append(data)
            if not self.undo_media:
                self.isChanged = False
                self.btnSave.setEnabled(self.isChanged)
            self.__updateView()
        self.btnUndo.setEnabled(len(self.undo_media) > 0)

    def update_lbls(self):
        self.lblPages.setText('%d/%d' % (self.current_page, self.total_pages))
        self.lblSelCount.setText('%d/%d' % (self.viewCards, len(self.filter_media)) + (' [F]' if self.isFiltered else ''))

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

    def btnSave_click(self):
        self.save_file, _ = QtWidgets.QFileDialog.getSaveFileName(self, caption='Gardar Reporte...', filter='*.json')
        self.saveReport()

    def setStatus(self, msg):
        self.lblOpenFolder.setText(msg.msg)
        self.lblOpenFolder.repaint()

    def setProgressStatus(self, txt: str):
        self.lblProgress.setText(txt)
        self.lblProgress.repaint()

    def __filterMedia(self):
        if not self.isFiltered:
            self.filter_media = self.media.copy()
            self.isFilterChange = True
            return
        if self.isFilterChange:
            self.filter_media = []
            count: int = 0
            total: int = len(self.media)
            self.progressBar.setVisible(True)
            self.progressBar.setMaximum(total)
            for media in self.media:
                self.setProgressStatus('Analizando %d de %d...' % (count, total))
                count += 1
                self.progressBar.setValue(count)
                try:
                    score = float(media['Comments'])
                    if (self.isFilterInvert and score <= self.filter_value) or (not self.isFilterInvert and score >= self.filter_value):
                        self.filter_media.append(media)
                except ValueError:
                    continue
            self.progressBar.setVisible(False)
            self.setProgressStatus('')
            self.setCurrentPage(1)
            self.isFilterChange = False

    def clearCardList(self):
        while self.cards.count() > 0:
            item = self.cards.takeAt(0)
            if not item:
                continue
            w = item.widget()
            if w:
                w.deleteLater()
        self.cards_list.clear()
        self.cards_list = []

    def removeCard(self, card: NsfwCard):
        c = self.cards.takeAt(self.cards.indexOf(card))
        print(c)
        if card in self.cards_list:
            self.cards_list.remove(card)
        card.deleteLater()

    def card_remove_me(self, card: NsfwCard):
        if card.data in self.media:
            self.media.remove(card.data)
        if card.data in self.filter_media:
            self.filter_media.remove(card.data)
        self.undo_media.append(card.data)
        self.isChanged = True
        self.btnSave.setEnabled(self.isChanged)
        self.btnUndo.setEnabled(len(self.undo_media) > 0)
        self.__updateView()

    def getPageMedia(self, cards_for_page: int):
        page_media: list = []
        start: int = (self.current_page - 1) * cards_for_page
        end: int = start + cards_for_page
        if end > len(self.filter_media):
            end = len(self.filter_media)
        self.progressBar.setVisible(True)
        self.progressBar.setMaximum(end)
        self.progressBar.setMinimum(start)
        for idx in range(start, end):
            page_media.append(self.filter_media[idx])
            self.progressBar.setValue(idx)
        self.progressBar.setVisible(False)
        return page_media

    def __updateView(self):
        if not self.VIC:
            self.clearCardList()
            return
        try:
            self.__filterMedia()
            if not self.filter_media:
                self.clearCardList()
                return
            self.listView.setEnabled(False)
            col, row, cardW, cardH = (0, 0, 200, 200)
            width, height = (self.listView.width(), self.listView.height())
            colums, rows = (round(width / (cardW + 10)), round(height / (cardH + 10)))
            cards_for_page = colums * rows
            complet_pages, incomplet_page = divmod(len(self.filter_media), cards_for_page)
            self.total_pages = complet_pages + 1 if(incomplet_page > 0)else 0
            page_media = self.getPageMedia(cards_for_page)
            self.clearCardList()
            base_path = str(Path(self.vic_file).parent)
            self.progressBar.setVisible(True)
            total: int = len(page_media)
            self.progressBar.setMaximum(total)
            count: int = 0
            for item in page_media:
                count += 1
                self.setProgressStatus('Creando muestra %d de %d...' % (count, total))
                item = NsfwCard(self.listView, item, cardW, cardH, base_path)
                item.remove_me.connect(self.card_remove_me)
                self.cards_list.append(item)
                if col >= colums:
                    col = 0
                    row += 1
                self.cards.addWidget(item, row, col)
                col += 1
                self.progressBar.setValue(count)
            self.progressBar.setVisible(False)
            self.setProgressStatus('')
            self.viewCards = self.current_page * cards_for_page
            if self.viewCards > len(self.filter_media):
                self.viewCards = len(self.filter_media)
            self.update_lbls()
        finally:
            self.listView.setEnabled(True)

    def __loadReportFile(self):
        if self.vic_file:
            self.lblStatus.setText(self.vic_file)
            self.VIC = readVICFromFile(self.vic_file)
            self.media = getMediaFormVIC(self.VIC)
            self.__updateView()

    def saveReport(self):
        if self.save_file:
            try:
                self.setEnabled(False)
                self.setProgressStatus('Guardando Reporte...')
                newVIC = self.VIC.copy()
                updateMedia(newVIC, self.media)
                json.dump(newVIC, open(self.save_file, 'w'))
                self.setProgressStatus('Reporte guardado en %s' % self.save_file)
            finally:
                self.setEnabled(True)
