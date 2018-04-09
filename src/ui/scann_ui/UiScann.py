from pathlib import Path
from src.ui.scann_ui.ui_nsfw_scann import Ui_dlgNsfwScanner, QtWidgets
from src.ui.scann_ui.nsfw_log_item import NsfwLogItem
from src.Nsfw.nsfw_scann import NsfwScann, ImageNsfw, QtGui, QtCore
from src.utils.message import Message, NORMAL, WARNING, DANGER
from src.utils.files import ImagesFinder
from src.Nsfw.vic13 import readVICFromFile, genNewVic, updateMedia


class DlgScanner(QtWidgets.QDialog, Ui_dlgNsfwScanner):

    nsfw: NsfwScann = None
    imgFinder: ImagesFinder = None
    scannFolder: str = ''
    vicFile: str = ''
    saveFile: str = ''
    saveFolder: str = ''
    VIC = None

    isInScann: bool = False
    isScannFinish: bool = False

    timer: QtCore.QTimer = QtCore.QTimer()
    charId: int = 0
    currentTxt: str = ''
    #Nsfw Log Vars
    nsfw_log_list: list = []
    next_udate_item: int = 0
    nro_items: int = 5

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.showProsess(False)
        self.video_viewer.setVisible(False)
        self.logImages.setVisible(False)
        self.resize(self.groupBox.size())
        self.nsfw = NsfwScann(self)
        self.nsfw.progressMax.connect(self.progressBar.setMaximum)
        self.nsfw.progress.connect(self.progressBar.setValue)
        self.nsfw.statusBar.connect(self.setStatusBar)
        self.nsfw.status.connect(self.setStatus)
        self.nsfw.image.connect(self.mostrarImagen)
        self.nsfw.video.connect(self.mostrarVideo)
        self.nsfw.video_progress.connect(self.video_progress_set)
        self.nsfw.video_scann.connect(self.video_scann)
        self.nsfw.finish.connect(self.nsfw_finish)
        self.selScore.valueChanged.connect(self.progressBarScore.setValue)
        self.progressBarScore.valueChanged.connect(self.nsfw.setMinScore)
        self.nsfw.setMinScore(self.selScore.value())
        self.btnClose.clicked.connect(self.btnClose_Click)
        self.btnAceptar.clicked.connect(self.btnAceptar_Click)
        self.btnStart.clicked.connect(self.btnStart_Click)
        self.btnScannFolder.clicked.connect(self.btnScannFolder_Click)
        self.btnVIC.clicked.connect(self.btnVIC_Click)
        self.btnSave.clicked.connect(self.btnSave_Click)
        self.btnPause.clicked.connect(self.nsfw.pause)
        self.chkShowImage.stateChanged.connect(self.showImage)
        self.chkGif_as_frame.stateChanged.connect(self.nsfw.setGif_as_frame)

    def showProsess(self, isShow=False):
        self.progressBar.setVisible(isShow)
        self.lblScannStatus.setVisible(isShow)
        self.lblProgressBar.setVisible(isShow)
        self.txtLog.setVisible(isShow)
        self.repaint()

    def showImage(self):
        if not self.chkShowImage.isChecked() > 0:
            self.logImages.setVisible(False)
            self.video_viewer.setVisible(False)
        elif self.nsfw_log_list:
            self.logImages.setVisible(True)

    def video_scann(self, value: bool):
        self.video_viewer.setVisible(value and self.chkShowImage.isChecked())

    def timerTimeOut(self):
        c: list = [' |', ' /', ' -', ' \\']
        self.charId += 1
        if not self.charId < len(c):
            self.charId = 0
        txt: str = self.currentTxt + c[self.charId]
        self.lblProgressBar.setText(txt)
        self.lblProgressBar.repaint()

    def setStatus(self, msg=Message('')):
        if msg.isAnimate:
            self.timer.stop()
            self.currentTxt = msg.msg
            self.timer.setInterval(100)
            self.timer.timeout.connect(self.timerTimeOut)
            self.timer.start()
        else:
            self.timer.stop()
            self.lblProgressBar.setText(msg.msg)
            self.lblProgressBar.repaint()

        if msg.tipo == DANGER:
            color = QtGui.QColor('red')
        elif msg.tipo == WARNING:
            color = QtGui.QColor('silver')
        else:
            color = QtGui.QColor('green')
        self.txtLog.setTextColor(color)
        if msg.isLog:
            self.txtLog.append(msg.msg)
            self.txtLog.verticalScrollBar().setValue(self.txtLog.verticalScrollBar().maximum())
            self.txtLog.repaint()

    def setStatusBar(self, txt):
        self.lblScannStatus.setText(txt)
        self.lblScannStatus.repaint()

    def mostrarImagen(self, img_nsfw: ImageNsfw):
        if len(self.nsfw_log_list) < self.nro_items:
            item = NsfwLogItem(self.logImages)
            item.setAll(img_nsfw.file, img_nsfw.score)
            self.nsfw_log_list.append(item)
            self.logImagenes_hLayout.addWidget(self.nsfw_log_list[self.next_udate_item])
            self.next_udate_item += 1
        else:
            self.next_udate_item += 1
            if self.next_udate_item >= self.nro_items:
                self.next_udate_item = 0
            self.nsfw_log_list[self.next_udate_item].setAll(img_nsfw.file, img_nsfw.score)
        if self.chkShowImage.isChecked():
            if not self.logImages.isVisible():
                self.logImages.setVisible(True)
                self.logImages.repaint()

    def mostrarVideo(self, frame: QtGui.QImage, score):
        if self.chkShowImage.isChecked():
            pix = QtGui.QPixmap.fromImage(frame)
            self.video_score.setValue(score * 100)
            self.video_frame.setPixmap(pix)
            self.video_frame.repaint()
            if not self.video_viewer.isVisible():
                self.video_viewer.setVisible(True)
                self.video_viewer.repaint()

    def video_progress_set(self, value: int, maximum: int):
        if self.chkShowImage.isChecked():
            if maximum >= 0:
                self.video_progress.setMaximum(maximum)
            self.video_progress.setValue(value)

    def setBtnsEnabled(self, isEnable: bool):
        self.btnScannFolder.setEnabled(isEnable)
        self.btnStart.setEnabled(isEnable)
        self.btnSave.setEnabled(isEnable)
        self.btnVIC.setEnabled(isEnable)
        self.btnPause.setEnabled(not isEnable)

    def nsfw_finish(self, media):
        try:
            if((media) and (not self.nsfw.isCanceled)):
                updateMedia(self.VIC, media)
                import json
                self.setStatus(
                    Message('Guardando Reporte..', True, NORMAL, False))
                json.dump(self.VIC, open(self.saveFile, 'w'))
                self.setStatus(Message('Reporte Guardado en: %s' %
                                       (self.saveFile), False))
                self.setStatus(Message('Guardando Log..', True, NORMAL, False))
                logFilePath = Path(self.saveFolder).joinpath('log.txt')
                with open(str(logFilePath), 'w') as logFile:
                    logFile.write(str(self.txtLog.toPlainText()))
                self.setStatus(Message('Log Guardado en: %s' %
                                       (logFilePath), False))
                self.isScannFinish = True
                self.isInScann = False
                self.btnAceptar.setEnabled(True)
            else:
                self.setStatus(Message('Proceso Cancelado!', False, DANGER))
                self.isInScann = False
        finally:
            self.setBtnsEnabled(True)

    def btnClose_Click(self):
        if self.isInScann:
            q = QtWidgets.QMessageBox.question(
                self, 'Escaneo en Curso!', 'Desea detener en escaneo en curso?')
            if q == QtWidgets.QMessageBox.No:
                return
            if self.nsfw:
                self.nsfw.stop()
            if self.imgFinder:
                self.imgFinder.stop()
            self.isInScann = False
            self.setBtnsEnabled(True)
        else:
            self.close()

    def btnAceptar_Click(self):
        self.accept()

    def btnStart_Click(self):
        if self.isScannFinish:
            q = QtWidgets.QMessageBox.question(
                self, 'Reporte Existente!', 'Existe un reporte guardado recientemente si continua se perdera!.\nDesea continuar de todos modos?')
            if q == QtWidgets.QMessageBox.No:
                return
            self.isScannFinish = False
        self.showProsess(True)
        self.txtLog.clear()
        self.btnAceptar.setEnabled(False)
        self.isInScann = True
        self.setBtnsEnabled(False)
        if self.scannFolder:
            self.VIC = genNewVic()
            self.scannFolder_Start()
        elif self.vicFile:
            self.VIC = readVICFromFile(self.vicFile)
            basePath = Path(self.vicFile).parent
            self.nsfw.scannVIC(self.VIC, str(basePath), self.saveFolder)
        else:
            self.showProsess(False)

    def btnScannFolder_Click(self):
        self.scannFolder = QtWidgets.QFileDialog.getExistingDirectory(self,
                                                                      caption='Directorio a Escanear?')
        if self.scannFolder:
            self.vicFile = ''
            self.lblScannFolder.setText(str(self.scannFolder))
            self.btnSave.setEnabled(True)
        else:
            self.lblScannFolder.setText('Seleccione el directorio a escanear!')
            self.btnSave.setEnabled(False)

    def btnVIC_Click(self):
        self.vicFile, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                                caption='Reporte VIC a Escanear?', filter='*.json')
        if self.vicFile:
            self.isScannFinish = False
            self.scannFolder = ''
            self.lblScannFolder.setText(str(self.vicFile))
            self.btnSave.setEnabled(True)
        else:
            self.lblScannFolder.setText('Seleccione el directorio a escanear!')
            self.btnSave.setEnabled(False)

    def btnSave_Click(self):
        self.saveFile, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, caption='Archivo para guardar el Reporte?', filter='*.json')
        if self.saveFile:
            self.lblSaveFolder.setText(str(self.saveFile))
            self.saveFolder = str(Path(self.saveFile).parent)
            self.btnStart.setEnabled(True)
        else:
            self.saveFolder = ''
            self.lblSaveFolder.setText('Directorio para guardar reporte.')
            self.btnStart.setEnabled(False)

    def scannFolder_Start(self):
        self.imgFinder = ImagesFinder(self, self.scannFolder)
        self.imgFinder.status.connect(self.setStatus)
        self.imgFinder.statusBar.connect(self.setStatusBar)
        self.imgFinder.finish.connect(self.ImagesFinder_Finish)
        self.imgFinder.progressMax.connect(self.progressBar.setMaximum)
        self.imgFinder.progress.connect(self.progressBar.setValue)
        self.imgFinder.find()

    def ImagesFinder_Finish(self, media: list):
        if media:
            updateMedia(self.VIC, media)
            self.nsfw.scannVIC(self.VIC, '', self.saveFolder)
