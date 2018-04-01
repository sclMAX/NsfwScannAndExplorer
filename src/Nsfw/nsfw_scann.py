from PyQt5 import QtCore
from src.utils.constants import NORMAL, WARNING, DANGER
from src.utils.message import Message
from src.Nsfw.vic13 import genNewMediaItem, updateMediaItem, readVICFromFile, isVICValid, getMediaFormVIC
from pathlib import Path
from imghdr import what
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

    archivos = 0
    imagenes = 0

    # Scann Vars
    media = []
    isCanceled = False
    saveFolder = ''
    basePath = ''
    isMiniatura = True
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
    
    @QtCore.pyqtSlot(int)
    def setIsMiniatura(self, isMiniatura):
        self.isMiniatura = (isMiniatura > 0)
    
    @QtCore.pyqtSlot()
    def stop(self):
        self.isCanceled = True
        self.exit()

    def searching_all_files(self, path: Path, onlyImg=True):
        try:
            dirpath = Path(path)
            assert(dirpath.is_dir())
            file_list = []
            for x in dirpath.iterdir():
                if x.is_file():
                    self.archivos += 1
                    fileType = what(x)
                    self.status.emit(Message('%d Imagenes de %d Archivos Encontrados...'%(self.imagenes, self.archivos),False,NORMAL,False))
                    self.emitStatus()
                    if(onlyImg)and(not fileType):
                        continue
                    self.imagenes += 1
                    file_list.append({
                        'file': x,
                        'type': fileType
                    })
                elif x.is_dir():
                    file_list.extend(self.searching_all_files(str(x)))
        except OSError:
            return file_list
        return file_list

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
            return (preds[0][1], img)
        except:
            return (-1, None)

    def saveMiniature(self, img, fileName):
        from PIL import Image
        self.status.emit(Message('Creando Miniatura...',True,NORMAL,False))
        basePath= Path(self.saveFolder).joinpath('miniatures')
        if(not Path(basePath).exists()):
            Path(basePath).mkdir()
        file = str(Path(basePath).joinpath(fileName))
        try:
            img.thumbnail((80,80),Image.ANTIALIAS)
            img.save(open(file, 'w'))
        except IOError:
            return

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

    def scannFolder(self, folder, saveFolder):
        self.ti = time()
        self.saveFolder = saveFolder
        self.status.emit(Message('Buscando Archivos...', True))
        self.archivos = 0
        self.imagenes = 0
        self.filesList = self.searching_all_files(folder, True)
        self.status.emit(Message('%d Archivos Encontrados!' %
                                 (len(self.filesList)), False))
        count = 0
        self.progressMax.emit(len(self.filesList))
        self.status.emit(Message('Creando Media...', True))
        self.basePath = ''
        for f in self.filesList:
            mediaItem = genNewMediaItem()
            updateMediaItem(mediaItem, {
                'MediaID': count,
                'RelativeFilePath': str(f['file']),
                'ImageType': str(f['type'])
            })
            self.media.append(mediaItem)
            count += 1
            self.progress.emit(count)
        self.status.emit(Message('Iniciando Escaneo...', False))
        self.start()

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
        for m in self.media:
            if(self.isCanceled):
                break
            img_path = str(m['RelativeFilePath']).replace('\\', '/')
            self.status.emit(
                Message('Escanenado: ' + img_path, False, NORMAL, False))
            img_path = Path(img_path)
            if(self.basePath):
                img_path = Path(self.basePath).joinpath(img_path)
            score, img = self.isPorno(str(img_path))
            minFile = ''
            if(img and self.isMiniatura):
                minFile = ('P%3d_mini_%4d.jpg' % ((score * 100), self.filesInReport)).replace(' ', '0')
                self.saveMiniature(img, minFile)
            if(score >= self.minScore):
                msg = Message('SI %2.4f - %s' %(score, img_path), False, NORMAL)
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
                    'Comments': ('%2.4f' % (score)),
                    'Miniature': 'miniatures/%s'%(minFile)
                })

            self.status.emit(msg)
            self.currentFile += 1
            self.progress.emit(self.currentFile)
            self.emitStatus()

        if(not self.isCanceled):
            self.status.emit(Message('Escaneo Terminado!', False))
        self.finish.emit(self.media)
        
