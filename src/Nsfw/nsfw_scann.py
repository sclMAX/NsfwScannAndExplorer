from PyQt5 import QtCore
from src.utils.message import Message, NORMAL, WARNING, DANGER
from src.Nsfw.vic13 import updateMediaItem, isVICValid, getMediaFormVIC, getVicCaseData
from pathlib import Path
from time import time
from src.utils.formats import secondsToHMS
import cv2 as cv


class NsfwScann(QtCore.QThread):
    # Model
    model = None
    weight_file: str = 'model/resnet_50_1by2_nsfw.caffemodel'
    model_file: str = 'model/deploy.prototxt'
    # Signals
    status: QtCore.pyqtSignal = QtCore.pyqtSignal(Message)
    statusBar: QtCore.pyqtSignal = QtCore.pyqtSignal(str)
    progressMax: QtCore.pyqtSignal = QtCore.pyqtSignal(int)
    progress: QtCore.pyqtSignal = QtCore.pyqtSignal(int)
    image: QtCore.pyqtSignal = QtCore.pyqtSignal(object, float)
    finish: QtCore.pyqtSignal = QtCore.pyqtSignal(object)

    # Scann Vars
    media: list = []
    isCanceled: bool = False
    saveFolder: str = ''
    basePath: str = ''
    minScore: float = 0
    ti: int = time()
    tip: int = 0
    currentFile: int = 0
    totalFiles: int = 0
    filesInReport: int = 0
    imageFiles: int = 0
    noImageFile: int = 0

    def __init__(self, parent=None):
        super().__init__(parent)

    @QtCore.pyqtSlot(int)
    def setMinScore(self, score):
        self.minScore = score / 100

    @QtCore.pyqtSlot()
    def stop(self):
        self.isCanceled = True
        self.exit()

    def __loadModel(self):
        try:
            self.status.emit(Message('Cargando Modelo...', True))
            from keras.preprocessing import image
            model = cv.dnn.readNetFromCaffe(prototxt=self.model_file, caffeModel=self.weight_file)
            self.status.emit(Message('Modelo Cargado!', False))
            return model
        except(FileNotFoundError):
            self.status.emit(
                Message('No se encontraron los archivos del Modelo!', False, DANGER))
            self.stop()

    def isPorno(self, img_path):
        from keras.preprocessing import image
        try:
            img = image.load_img(img_path, target_size=(256, 256))
            x = image.img_to_array(img)
            inputblob = cv.dnn.blobFromImage(
                x, 1., (224, 224), (104, 117, 123), False, False)
            self.model.setInput(inputblob)
            preds = self.model.forward()
            if(preds[0][1] >= self.minScore):
                self.image.emit(img, preds[0][1])
            return preds[0][1]
        except (ValueError, SyntaxError, OSError, TypeError):
            return -1

    def emitStatus(self):
        ct: int = time()
        ett: int = ct - self.ti
        strTT: str = secondsToHMS(ett)
        if(self.tip):
            et: int = ct - self.tip
            strTP: str = secondsToHMS(et)
            fs: float = self.currentFile / et
            eta = (self.totalFiles - self.currentFile) / (fs if fs else 1)
            strEta: str = secondsToHMS(eta)
            data = (self.currentFile, self.totalFiles, self.filesInReport,
                    self.imageFiles, self.noImageFile, strTT, strTP, strEta, fs)
            txt: str = 'A: %d de %d | Nsfw: %d de %d | NoImg: %d | TT: %s | TP: %s | ETA: %s @ %.2f A/seg' % data
            self.statusBar.emit(txt)
        else:
            txt: str = 'TT: %s @ %.2f A/seg' % (strTT, self.archivos / ett)
            self.statusBar.emit(txt)

    def scannVIC(self, VIC, basePath, saveFolder):
        self.ti = time()
        self.saveFolder = saveFolder
        if(isVICValid(VIC)):
            self.media = getMediaFormVIC(VIC)
            if(self.media):
                self.status.emit(Message(getVicCaseData(VIC)))
                self.basePath = basePath
                self.start()
            else:
                self.status.emit(Message(
                    'No se pudo recuperar los datos del Archivo VIC!', False, DANGER))
        else:
            self.status.emit(
                Message('Archivo VIC no valido!', False, DANGER))

    def run(self):
        self.isCanceled = False
        if(not self.model):
            self.model = self.__loadModel()
        self.totalFiles = len(self.media)
        self.progressMax.emit(self.totalFiles)
        self.currentFile = 0
        self.tip = time()
        self.filesInReport = 0
        self.imageFiles = 0
        self.noImageFile = 0
        for m in self.media:
            if(self.isCanceled):
                break
            img_path = str(m['RelativeFilePath']).replace('\\', '/')
            self.status.emit(
                Message('Escanenado: ' + img_path, False, NORMAL, False))
            img_path = Path(img_path)
            if(self.basePath):
                img_path = Path(self.basePath).joinpath(img_path)
            score = self.isPorno(str(img_path))
            if(score >= self.minScore):
                msg = Message('SI %2.4f - %s' %
                              (score, img_path), False, NORMAL)
                self.filesInReport += 1
                self.imageFiles += 1
            elif (score == -1):
                msg = Message('NO IMAGEN! - %s' % (img_path), False, DANGER)
                self.noImageFile += 1
            else:
                msg = Message('NO %2.4f - %s' %
                              (score, img_path), False, WARNING)
                self.imageFiles += 1
            updateMediaItem(m, {
                'Comments': ('%2.4f' % (score))
            })

            self.status.emit(msg)
            self.currentFile += 1
            self.progress.emit(self.currentFile)
            self.emitStatus()

        if(not self.isCanceled):            
            self.status.emit(Message('Escaneo Terminado!', False))
            self.status.emit(Message('Total de Archivos: %d'%(self.totalFiles)))
            self.status.emit(Message('Tiempo Total: %s'%(secondsToHMS(time() - self.ti))))
            self.status.emit(Message('Promedio por Archivo: %.4f mseg.'%(((time() - self.tip)* 1000)/self.totalFiles)))
        self.finish.emit(self.media)
