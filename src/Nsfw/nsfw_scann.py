from pathlib import Path
from time import time
from PyQt5 import QtCore, QtGui
import cv2 as cv
import fleep
from src.utils.message import Message, NORMAL, WARNING, DANGER
from src.Nsfw.vic13 import updateMediaItem, isVICValid, getMediaFormVIC, getVicCaseData
from src.utils.formats import secondsToHMS


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
    video: QtCore.pyqtSignal = QtCore.pyqtSignal(QtGui.QImage, float)
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
            image = image
            model = cv.dnn.readNetFromCaffe(
                prototxt=self.model_file, caffeModel=self.weight_file)
            self.status.emit(Message('Modelo Cargado!', False))
            return model
        except FileNotFoundError:
            self.status.emit(
                Message('No se encontraron los archivos del Modelo!', False, DANGER))
            self.stop()

    def __getProbability(self, inputBlob):
        self.model.setInput(inputBlob)
        pred: float = self.model.forward()[0][1]
        return pred

    def __video_emit(self, frame, score):
        height, width, _ = frame.shape
        bytesPerLine = 3 * width
        cv.cvtColor(frame, cv.COLOR_BGR2RGB, frame)
        img = QtGui.QImage(frame.data, width, height,
                           bytesPerLine, QtGui.QImage.Format_RGB888)
        self.video.emit(img, score)

    def __scannVideo(self, file):
        from PIL import Image
        try:
            self.status.emit(Message('Escaneando Video...', True, NORMAL, False))
            maxScore = 0
            cap = cv.VideoCapture(file)
            fps = abs(cap.get(cv.CAP_PROP_FPS))
            fcount = abs(cap.get(cv.CAP_PROP_FRAME_COUNT))
            frameToRead = 0
            while cap.isOpened():
                frameToRead += fps if(fps > 10) else 1
                if not frameToRead < fcount:
                    frameToRead = fcount
                cap.set(1, frameToRead - 1)
                _ = cap.get(cv.CAP_PROP_POS_AVI_RATIO)
                _ = cap.get(cv.CAP_PROP_POS_MSEC)
                ok, frame = cap.read()
                if ok:
                    frame = cv.resize(frame, (256, 256))
                    pi = Image.fromarray(frame)
                    score, _ = self.__scannImage(pi, False)
                    self.__video_emit(frame, score)
                    if score > maxScore:
                        maxScore = score
                    if frameToRead >= fcount:
                        break
                else:
                    break

            return maxScore
        finally:
            cap.release()

    def __scannImage(self, img, isFile=True):
        from keras.preprocessing import image
        try:
            if isFile:
                img = image.load_img(img, target_size=(256, 256))
            img_na = image.img_to_array(img)
            inputblob = cv.dnn.blobFromImage(
                img_na, 1., (224, 224), (104, 117, 123), False, False)
            return (self.__getProbability(inputblob), img)
        except (ValueError, SyntaxError, OSError, TypeError):
            return (-1, None)

    def isPorno(self, file_path: str, file_type: str):
        try:
            file_extension = ''
            if not file_type:
                with open(file_path, "rb") as file:
                    fileInfo = fleep.get(file.read(128))
                file_type = fileInfo.type
                file_extension = fileInfo.extension
        except IOError:
            file_type = 'None'
            file_extension = ''
        if 'video' in file_type:
            probability = self.__scannVideo(file_path)
        else:
            if 'gif' in file_extension:
                probability = self.__scannVideo(file_path)
            else:
                probability, img = self.__scannImage(file_path, True)
                if((probability >= self.minScore)and(img)):
                    self.image.emit(img, probability)
        return probability

    def emitStatus(self):
        ct: int = time()
        ett: int = ct - self.ti
        strTT: str = secondsToHMS(ett)
        if self.tip:
            et: int = ct - self.tip
            strTP: str = secondsToHMS(et)
            fs: float = self.currentFile / et
            eta = (self.totalFiles - self.currentFile) / (fs if fs else 1)
            strEta: str = secondsToHMS(eta)
            data = (self.currentFile, self.totalFiles, self.filesInReport,
                    self.imageFiles, self.noImageFile, strTT, strTP, strEta, fs)
            txt = 'A: %d de %d | Nsfw: %d de %d | NoImg: %d | TT: %s | TP: %s | ETA: %s @ %.2f A/seg' % data
            self.statusBar.emit(txt)
        else:
            txt: str = 'TT: %s @ %.2f A/seg' % (strTT, self.archivos / ett)
            self.statusBar.emit(txt)

    def scannVIC(self, VIC, basePath, saveFolder):
        self.ti = time()
        self.saveFolder = saveFolder
        if isVICValid(VIC):
            self.media = getMediaFormVIC(VIC)
            if self.media:
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
        if not self.model:
            self.model = self.__loadModel()
        self.totalFiles = len(self.media)
        self.progressMax.emit(self.totalFiles)
        self.currentFile = 0
        self.tip = time()
        self.filesInReport = 0
        self.imageFiles = 0
        self.noImageFile = 0
        for m in self.media:
            if self.isCanceled:
                break
            img_path = str(m['RelativeFilePath']).replace('\\', '/')
            file_type = m.get('FileType')
            self.status.emit(
                Message('Escanenado: ' + img_path, False, NORMAL, False))
            img_path = Path(img_path)
            if self.basePath:
                img_path = Path(self.basePath).joinpath(img_path)
            score = self.isPorno(str(img_path), file_type)
            if score >= self.minScore:
                msg = Message('SI %2.4f - %s' %
                              (score, img_path), False, NORMAL)
                self.filesInReport += 1
                self.imageFiles += 1
            elif score == -1:
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

        if not self.isCanceled:
            self.status.emit(Message('Escaneo Terminado!', False))
            self.status.emit(Message('Total de Archivos: %d' %
                                     (self.totalFiles)))
            self.status.emit(Message('Tiempo Total: %s' %
                                     (secondsToHMS(time() - self.ti))))
            self.status.emit(Message('Promedio por Archivo: %.4f mseg.' % (
                ((time() - self.tip) * 1000)/self.totalFiles)))
        self.finish.emit(self.media)
