from PyQt5 import QtCore
from src.utils.constants import NORMAL, WARNING, DANGER
from src.utils.message import Message
from src.Nsfw.vic13 import genNewMediaItem, updateMediaItem, readVICFromFile, isVICValid, getMediaFormVIC
from pathlib import Path
from time import time
from src.utils.formats import secondsToHMS


class NsfwScann(QtCore.QThread):
    # Model
    model = None
    weight_file = 'model/max_open_nsfw.h5'
    model_file = 'model/max_open_nsfw.json'
    # Signals
    status = QtCore.pyqtSignal(Message)
    statusBar = QtCore.pyqtSignal(str)
    progressMax = QtCore.pyqtSignal(int)
    progress = QtCore.pyqtSignal(int)
    finish = QtCore.pyqtSignal(object)

    # Scann Vars
    media = []
    isCanceled = False
    saveFolder = ''
    basePath = ''
    minScore = 0
    ti = time()
    tip = 0
    currentFile = 0
    totalFiles = 0
    filesInReport = 0
    imageFiles = 0
    noImageFile = 0

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
        ct = time()
        ett = ct - self.ti
        strTT = secondsToHMS(ett)
        if(self.tip):
            et = ct - self.tip
            strTP = secondsToHMS(et)
            fs = self.currentFile / et
            eta = (self.totalFiles - self.currentFile) / (fs if fs else 1)
            strEta = secondsToHMS(eta)
            data = (self.currentFile, self.totalFiles, self.filesInReport,
                    self.imageFiles, self.noImageFile, strTT, strTP, strEta, fs)
            txt = 'A: %d de %d | Img In: %d de %d | NoImg: %d | TT: %s | TP: %s | ETA: %s @ %.2f A/seg' % data
            self.statusBar.emit(txt)
        else:
            txt = 'TT: %s @ %.2f A/seg' % (strTT, self.archivos / ett)
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


class NsfwScannManager(QtCore.QObject):

    mutex: QtCore.QMutex = QtCore.QMutex()
    # Model
    model = None
    weight_file = 'model/max_open_nsfw.h5'
    model_file = 'model/max_open_nsfw.json'
    # Signals
    sendMinScore: QtCore.pyqtSignal = QtCore.pyqtSignal(int)
    stopAll: QtCore.pyqtSignal = QtCore.pyqtSignal()
    status = QtCore.pyqtSignal(Message)
    statusBar = QtCore.pyqtSignal(str)
    progressMax = QtCore.pyqtSignal(int)
    progress = QtCore.pyqtSignal(int)
    finish = QtCore.pyqtSignal(object)
    # Thread Vars
    runThreads: list = []
    maxThreads: int = 1 #QtCore.QThread.idealThreadCount()
    basePath: str = ''
    # Process Stats Vars
    tInicio: int
    tInicioScann: int
    isCanceled: bool = False
    minScore: float = 0
    totalFiles: int = 0
    filesScanned: int = 0
    filesImage: int = 0
    filesImageNsfw: int = 0
    filesNoImage: int = 0
    # medida
    media: list = []

    def __init__(self, parent: QtCore.QObject):
        super().__init__(parent)

    @QtCore.pyqtSlot()
    def setFilesScanned(self):
        _ = QtCore.QMutexLocker(self.mutex)
        self.filesScanned += 1
        self.__emitStatusBar()

    @QtCore.pyqtSlot()
    def setFilesImage(self):
        _ = QtCore.QMutexLocker(self.mutex)
        self.filesImage += 1
        

    @QtCore.pyqtSlot()
    def setFilesImageNsfw(self):
        _ = QtCore.QMutexLocker(self.mutex)
        self.filesImageNsfw += 1

    @QtCore.pyqtSlot()
    def setFilesNoImage(self):
        _ = QtCore.QMutexLocker(self.mutex)
        self.filesNoImage += 1

    @QtCore.pyqtSlot(int)
    def setMinScore(self, score):
        _ = QtCore.QMutexLocker(self.mutex)
        self.minScore = score / 100
        self.sendMinScore.emit(score)

    @QtCore.pyqtSlot()
    def stop(self):
        _ = QtCore.QMutexLocker(self.mutex)
        self.isCanceled = True
        self.stopAll.emit()
        self.status.emit(Message('Proceso Cancelado!', False, DANGER, True))
        self.finish.emit(None)

    def __emitStatusBar(self):
        _ = QtCore.QMutexLocker(self.mutex)
        ct = time()
        ett = ct - self.tInicio
        strTT = secondsToHMS(ett)
        et = ct - self.tInicioScann
        strTP = secondsToHMS(et)
        fs = self.filesScanned / et
        eta = (self.totalFiles - self.filesScanned) / (fs if fs else 1)
        strEta = secondsToHMS(eta)
        data = (self.filesScanned, self.totalFiles, self.filesImageNsfw,
                self.filesImage, self.filesNoImage, strTT, strTP, strEta, fs, len(self.runThreads), self.maxThreads)
        txt = 'A: %d de %d | Nsfw: %d de %d | NoImg: %d | TT: %s | TP: %s | ETA: %s @ %.2f A/seg | W: %d de %d' % data
        self.statusBar.emit(txt)

    # def __loadModel(self):
    #     self.progressMax.emit(0)
    #     self.status.emit(Message('Cargando Backend Tensorflow...', True))
    #     from keras import backend as K
    #     from keras.models import model_from_json
    #     self.status.emit(Message('Backend Tensorflow Cargado!'))
    #     try:
    #        # K.clear_session()
    #         K.get_session()
    #         self.status.emit(Message('Cargando Modelo...', True))
    #         json_file = open(self.model_file, 'r')
    #         loaded_model_json = json_file.read()
    #         self.status.emit(Message('Modelo Cargado!'))
    #         self.status.emit(Message('Configurando Modelo...', True))
    #         model = model_from_json(loaded_model_json)
    #         model.load_weights(self.weight_file)
    #         self.status.emit(Message('Modelo Configurado!'))
    #         return model
    #     except(FileNotFoundError):
    #         raise FileNotFoundError(
    #             'No se encontraron los archivos del Modelo!')
    #     finally:
    #         if json_file:
    #             json_file.close()

    def __createWorker(self, media: list):
        # TODO Agregar control de Errores
        worker: NsfwScannManager = NsfwScannWorker(self, self.model)
        worker.status.connect(self.status)
        worker.fileScanned.connect(self.setFilesScanned)
        worker.fileImage.connect(self.setFilesImage)
        worker.fileImageNsfw.connect(self.setFilesImageNsfw)
        worker.fileNoImage.connect(self.setFilesNoImage)
        worker.finish.connect(self.__worker_finish)
        worker.setMinScore(int(self.minScore * 100))
        worker.scann(media, self.basePath)
        self.runThreads.append(worker)
        return True

    def __worker_finish(self, worker: QtCore.QThread, subMedia: list):
        _ = QtCore.QMutexLocker(self.mutex)
        self.media.extend(subMedia)
        self.runThreads.remove(worker)
        if(not len(self.runThreads))and(not self.isCanceled):
            self.finish.emit(self.media)

    def start(self, inMedia: list, tInicio: int, basePath: str):
        # Chequear que media contenga items
        self.tInicio = tInicio
        self.basePath = basePath
        self.totalFiles = len(inMedia)
        if(not self.totalFiles):
            return
        # Cargar modelo
        # if(not self.model):
        #     self.model = self.__loadModel()
        # Set contadores to 0
        self.totalFiles = 0
        self.filesScanned = 0
        self.filesImage = 0
        self.filesImageNsfw = 0
        self.filesNoImage = 0
        # Dividir media para los workers
        mediasForWorkers: list = []
        mediasInItem: int = round(len(inMedia) / self.maxThreads)
        for w in range(self.maxThreads):
            self.status.emit(Message('Configurando Worker %d de %d...' % (
                w, self.maxThreads), True, NORMAL, False))
            self.progressMax.emit(mediasInItem)
            itemCount: int = 0
            subMedia: list = []
            for m in inMedia:
                if(itemCount < mediasInItem):
                    subMedia.append(m)
                    inMedia.remove(m)
                    itemCount += 1
                    self.progress.emit(itemCount)
                else:
                    break
            mediasForWorkers.append(subMedia)
        mediasForWorkers[0].extend(inMedia)
        # Crear workers
        self.tInicioScann = time()
        _ = QtCore.QMutexLocker(self.mutex)
        for mw in mediasForWorkers:
            if(not self.__createWorker(mw)):
                self.status.emit(
                    Message('Error al crear Workers!', False, DANGER, True))
        for worker in self.runThreads:
            worker.iniciar()


class NsfwScannWorker(QtCore.QThread):
    # Model
    model = None
    weight_file = 'model/max_open_nsfw.h5'
    model_file = 'model/max_open_nsfw.json'
   # Signals
    status: QtCore.pyqtSignal = QtCore.pyqtSignal(Message)
    fileScanned: QtCore.pyqtSignal = QtCore.pyqtSignal()
    fileImage: QtCore.pyqtSignal = QtCore.pyqtSignal()
    fileImageNsfw: QtCore.pyqtSignal = QtCore.pyqtSignal()
    fileNoImage: QtCore.pyqtSignal = QtCore.pyqtSignal()
    finish: QtCore.pyqtSignal = QtCore.pyqtSignal(QtCore.QThread, list)

    # Scann Vars
    media: list = []
    isCanceled: bool = False
    basePath: str = ''
    minScore: float = 0

    def __init__(self, parent: NsfwScannManager, model: object):
        super().__init__(parent)
        self.model = model
        parent.stopAll.connect(self.stop)
        parent.sendMinScore.connect(self.setMinScore)

    @QtCore.pyqtSlot(int)
    def setMinScore(self, score):
        self.minScore = score / 100

    @QtCore.pyqtSlot()
    def stop(self):
        self.isCanceled = True
        self.exit()

    def __isPorno(self, img_path):
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
        except (ValueError, OSError, SyntaxError):
            return -1

    def __loadModel(self):
        self.status.emit(Message('Cargando Backend Tensorflow...', True))
        from keras import backend as K
        from keras.models import model_from_json
        self.status.emit(Message('Backend Tensorflow Cargado!'))
        try:
           # K.clear_session()
            K.get_session()
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

    def scann(self, media: list, basePath: str):
        self.media = media
        self.basePath = basePath
        
    def iniciar(self):
        if(not self.model):
            self.model = self.__loadModel()    
        self.start()

    def run(self):
        self.isCanceled = False
        for m in self.media:
            if(self.isCanceled):
                break
            img_path = str(m['RelativeFilePath']).replace('\\', '/')
            self.status.emit(
                Message('Escanenado: ' + img_path, False, NORMAL, False))
            img_path = Path(img_path)
            if(self.basePath):
                img_path = Path(self.basePath).joinpath(img_path)
            score = self.__isPorno(str(img_path))
            if(score >= self.minScore):
                msg = Message('SI %2.4f - %s' %
                              (score, img_path), False, NORMAL)
                self.fileImageNsfw.emit()
                self.fileImage.emit()
            elif (score == -1):
                msg = Message('NO IMAGEN! - %s' % (img_path), False, DANGER)
                self.fileNoImage.emit()
            else:
                msg = Message('NO %2.4f - %s' %
                              (score, img_path), False, WARNING)
                self.fileImage.emit()
            updateMediaItem(m, {
                'Comments': ('%2.4f' % (score))
            })
            self.status.emit(msg)
            self.fileScanned.emit()
        if(not self.isCanceled):
            self.finish.emit(self, self.media)
