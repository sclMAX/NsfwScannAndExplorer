from pathlib import Path
from time import time
from PyQt5 import QtCore, QtGui
from PIL import Image
import imageio
import cv2 as cv
import fleep
from src.utils.message import Message, NORMAL, WARNING, DANGER
from src.utils import Image as ImgTools
from src.Nsfw.vic13 import updateMediaItem, isVICValid, getMediaFormVIC, getVicCaseData
from src.utils.formats import secondsToHMS


class ImageNsfw():
    score: int
    file: str

    def __init__(self, score: float, file: str):
        self.file = file
        self.score = round(score * 100)


class NsfwScann(QtCore.QThread):

    # Model
    model: object = None
    weight_file: str = 'model/resnet_50_1by2_nsfw.caffemodel'
    model_file: str = 'model/deploy.prototxt'
    # Signals
    status: QtCore.pyqtSignal = QtCore.pyqtSignal(Message)
    statusBar: QtCore.pyqtSignal = QtCore.pyqtSignal(str)
    progressMax: QtCore.pyqtSignal = QtCore.pyqtSignal(int)
    progress: QtCore.pyqtSignal = QtCore.pyqtSignal(int)
    image: QtCore.pyqtSignal = QtCore.pyqtSignal(ImageNsfw)
    video: QtCore.pyqtSignal = QtCore.pyqtSignal(QtGui.QImage, float)
    video_progress: QtCore.pyqtSignal = QtCore.pyqtSignal(int, int)
    video_scann: QtCore.pyqtSignal = QtCore.pyqtSignal(bool)
    finish: QtCore.pyqtSignal = QtCore.pyqtSignal(object)

    # Scann Vars
    media: list = []
    isCanceled: bool = False
    isInPause: bool = False
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
    gif_as_frame: bool = True
    isPauseEmit: bool = False

    def __init__(self, parent=None):
        super().__init__(parent)
        self.isScannVideos: bool = True

    @QtCore.pyqtSlot(int)
    def setMinScore(self, score):
        self.minScore = score / 100

    @QtCore.pyqtSlot(int)
    def setGif_as_frame(self, chkState: int):
        self.gif_as_frame = chkState > 0

    @QtCore.pyqtSlot(int)
    def setIsScannVideos(self, chkState: int):
        self.isScannVideos = chkState > 0

    @QtCore.pyqtSlot()
    def stop(self):
        self.isCanceled = True
        self.exit()

    @QtCore.pyqtSlot()
    def pause(self):
        self.isInPause = not self.isInPause

    def __loadModel(self):
        try:
            self.status.emit(Message('Cargando Modelo...', True, NORMAL, False))
            model_loaded = cv.dnn.readNetFromCaffe(prototxt=self.model_file, caffeModel=self.weight_file)
            self.status.emit(Message('Modelo Cargado!', False, NORMAL, False))
            return model_loaded
        except FileNotFoundError:
            self.status.emit(Message('No se encontraron los archivos del Modelo!', False, DANGER))
            self.stop()

    def __getScore(self, inputBlob):
        self.model.setInput(inputBlob)
        return self.model.forward()[0][1]

    def __video_emit(self, frame, score):
        height, width, _ = frame.shape
        bytesPerLine = 3 * width
        cv.cvtColor(frame, cv.COLOR_BGR2RGB, frame)
        img = QtGui.QImage(frame.data, width, height,
                           bytesPerLine, QtGui.QImage.Format_RGB888)
        self.video.emit(img, score)

    def __scannGif(self, file: str):
        try:
            self.status.emit(Message(file + ' - Gif...', True, NORMAL, False))
            self.video_scann.emit(True)
            cap = None
            maxScore = 0
            n = imageio.mimread(file)
            cap = cv.VideoCapture(file)
            if isinstance(n, list):
                totalFrames = len(n)
            else:
                totalFrames = int(n)
            self.video_progress.emit(0, totalFrames)
            frame_nro: int = 0
            while cap.isOpened():
                ok, frame = cap.read()
                if ok:
                    frame = cv.resize(frame, (256, 256))
                    pi = ImgTools.array_to_img(frame)
                    score, _ = self.__scannImage(pi)
                    if score > maxScore:
                        maxScore = score
                    frame_nro += 1
                    self.__video_emit(frame, score)
                    self.video_progress.emit(frame_nro, -1)
                    if frame_nro >= totalFrames:
                        break
                else:
                    break
            return maxScore
        except (SystemError, RuntimeError, ValueError, OSError, Image.DecompressionBombError):
            score, img = self.__scannImage(file)
            if (score >= self.minScore)and(img):
                self.image.emit(ImageNsfw(score, file))
            return score
        finally:
            if cap:
                cap.release()
            self.video_scann.emit(False)

    def __scannVideo(self, file: str):
        try:
            self.status.emit(
                Message(file + ' - Video...', True, NORMAL, False))
            self.video_scann.emit(True)
            maxScore = 0
            isOneSend = False
            cap = None
            cap = cv.VideoCapture(file)
            fps = abs(cap.get(cv.CAP_PROP_FPS))
            fcount = abs(cap.get(cv.CAP_PROP_FRAME_COUNT))
            self.video_progress.emit(0, fcount)
            frameToRead = 0
            while cap.isOpened():
                frameToRead += fps
                if not frameToRead < fcount:
                    frameToRead = fcount
                cap.set(1, frameToRead - 1)
                ok, frame = cap.read()
                if ok:
                    frame = cv.resize(frame, (256, 256))
                    pi = Image.fromarray(frame)
                    score, _ = self.__scannImage(pi)
                    if score >= self.minScore or not isOneSend:
                        self.__video_emit(frame, score)
                        isOneSend = True
                    if score > maxScore:
                        maxScore = score
                        if fcount > (fps * 60 * 5):
                            if (self.minScore < 0.50 and maxScore > (self.minScore * 1.3)) or (self.minScore >= 0.50 and maxScore >= self.minScore):
                                break
                    self.video_progress.emit(frameToRead, -1)
                    if frameToRead >= fcount:
                        break
                else:
                    break
            return maxScore
        except (SystemError, IOError):
            return -1
        finally:
            if cap:
                cap.release()
            self.video_scann.emit(False)

    def __scannImage(self, img):
        try:
            if isinstance(img, str):
                img = ImgTools.load_img(img, target_size=(256, 256))
            img_na = ImgTools.img_to_array(img)
            inputblob = cv.dnn.blobFromImage(
                img_na, 1., (224, 224), (104, 117, 123), False, False)
            return (self.__getScore(inputblob), img)
        except (ValueError, SyntaxError, OSError, TypeError, RuntimeError, Image.DecompressionBombError):
            return (-1, None)
        except ImportError:
            self.status.emit(Message('PILLOW no instalado!', False, DANGER, True))
            self.stop()

    def getScore(self, file_path: str):
        try:
            with open(file_path, "rb") as file:
                fileInfo = fleep.get(file.read(128))
                file.close()
            file_type = fileInfo.type
            file_extension = fileInfo.extension
        except IOError:
            file_type = ['']
            file_extension = ['']
        if 'video' in file_type:
            if self.isScannVideos:
                score = self.__scannVideo(file_path)
            else:
                score = -10
        elif ('gif' in file_extension) and self.gif_as_frame:
            score = self.__scannGif(file_path)
        else:
            score, img = self.__scannImage(file_path)
            if((score >= self.minScore)and(img)):
                self.image.emit(ImageNsfw(score, file_path))
        return (score, file_type[0] if file_type else file_type, file_extension[0] if file_extension else file_extension)

    def __emitStatus(self):
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
                self.start(priority=QtCore.QThread.HighestPriority)
            else:
                self.status.emit(Message(
                    'No se pudo recuperar los datos del Archivo VIC!', False, DANGER))
        else:
            self.status.emit(Message('Archivo VIC no valido!', False, DANGER))

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
            while self.isInPause:
                if not self.isPauseEmit:
                    self.status.emit(Message('PAUSADO!', False, NORMAL, False))
                    self.isPauseEmit = True
            self.isPauseEmit = False
            isScannedNsfw = m.get('isScannedNsfw')
            img_path = str(m['RelativeFilePath']).replace('\\', '/')
            self.status.emit(
                Message('Escanenado: ' + img_path, False, NORMAL, False))
            if not isScannedNsfw:
                isScannedNsfw = True
                img_path = Path(img_path)
                if self.basePath:
                    img_path = Path(self.basePath).joinpath(img_path)
                score, file_type, file_extension = self.getScore(str(img_path))
                if score >= self.minScore:
                    msg = Message('SI %2.4f - %s' %(score, img_path), False, NORMAL)
                    self.filesInReport += 1
                    self.imageFiles += 1
                elif score == -1:
                    msg = Message('NO IMAGEN! - %s' % (img_path), False, DANGER)
                    self.noImageFile += 1
                elif score == -10:
                    msg = Message('')
                    isScannedNsfw = False
                else:
                    msg = Message('NO %2.4f - %s' % (score, img_path), False, WARNING)
                    self.imageFiles += 1
                updateMediaItem(m, {
                    'Comments': ('%2.4f' % (score)),
                    'FileType': file_type,
                    'FileExtension': file_extension,
                    'isScannedNsfw': isScannedNsfw
                })
                self.status.emit(msg)
                self.__emitStatus()
            self.currentFile += 1
            self.progress.emit(self.currentFile)
            

        if not self.isCanceled:
            self.status.emit(Message('\nEscaneo Terminado!', False))
            self.status.emit(Message('Total de Archivos: %d' %
                                     (self.totalFiles)))
            self.status.emit(Message('Tiempo Total: %s' %
                                     (secondsToHMS(time() - self.ti))))
            self.status.emit(Message('Promedio por Archivo: %.4f mseg.' % (
                ((time() - self.tip) * 1000)/self.totalFiles)))
        self.finish.emit(self.media)
