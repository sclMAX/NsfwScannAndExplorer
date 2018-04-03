from PyQt5 import QtCore
from src.utils.message import Message, NORMAL, WARNING, DANGER
from src.Nsfw.vic13 import updateMediaItem, isVICValid, getMediaFormVIC
from pathlib import Path
from time import time
from src.utils.formats import secondsToHMS


class NsfwScann(QtCore.QThread):
    # Model
    model = None
    weight_file: str = 'model/max_open_nsfw.h5'
    model_file: str = 'model/max_open_nsfw.json'
    # Signals
    status: QtCore.pyqtSignal = QtCore.pyqtSignal(Message)
    statusBar: QtCore.pyqtSignal = QtCore.pyqtSignal(str)
    progressMax: QtCore.pyqtSignal = QtCore.pyqtSignal(int)
    progress: QtCore.pyqtSignal = QtCore.pyqtSignal(int)
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

    def loadModel(self):
        self.progressMax.emit(0)
        self.status.emit(Message('Cargando Backend Tensorflow...', True))
        from keras import backend as K
        from keras.models import model_from_json
        self.status.emit(Message('Backend Tensorflow Cargado!'))
        try:
            K.clear_session()
            self.status.emit(Message('Cargando Modelo...', True))
            json_file = open(self.model_file, 'r')
            loaded_model_json = json_file.read()
            self.status.emit(Message('Modelo Cargado!'))
            self.status.emit(Message('Configurando Modelo...', True))
            model = model_from_json(loaded_model_json)
            model.load_weights(self.weight_file)
            self.status.emit(Message('Modelo Configurado!'))
            return model
        except(FileNotFoundError):
            raise FileNotFoundError(
                'No se encontraron los archivos del Modelo!')
        finally:
            if json_file:
                json_file.close()

    def isPorno(self, img_path):
        from keras.preprocessing import image
        import numpy as np
        from keras.applications.imagenet_utils import preprocess_input
        try:
            img = image.load_img(img_path, target_size=(224, 224))
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            preds = self.model.predict(x)
            return preds[0][1]
        except:
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
            txt: str = 'A: %d de %d | Img In: %d de %d | NoImg: %d | TT: %s | TP: %s | ETA: %s @ %.2f A/seg' % data
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
            self.model = self.loadModel()
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
        self.finish.emit(self.media)
