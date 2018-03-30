from PyQt5 import QtCore
from src.utils import constants
from src.utils.message import Message
from src.utils.files import searching_all_files
from src.Nsfw.vic13 import genNewMediaItem, updateMediaItem, readVICFromFile, isVICValid, getMediaFormVIC

class NsfwScann(QtCore.QThread):
    # Model
    model = None
    weight_file = 'model/max_open_nsfw.h5'
    model_file = 'model/max_open_nsfw.json'
    # Signals
    status = QtCore.pyqtSignal(Message)
    progressMax = QtCore.pyqtSignal(int)
    progress = QtCore.pyqtSignal(int)

    # Scann Vars
    media = []

    def __init__(self, parent=None):
        super().__init__(parent)

    def loadModel(self):
        self.progressMax.emit(0)
        msg = Message('Cargando Backend Tensorflow...', True)
        self.status.emit(msg)
        from keras import backend as K
        from keras.models import model_from_json
        try:
            K.clear_session()
            msg = Message('Cargando Modelo...', True)
            self.status.emit(msg)
            json_file = open(self.model_file, 'r')
            loaded_model_json = json_file.read()
            msg = Message('Configurando Modelo...', True)
            self.status.emit(msg)
            model = model_from_json(loaded_model_json)
            model.load_weights(self.weight_file)
            msg = Message('Modelo Configurado!')
            self.status.emit(msg)
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

        img = image.load_img(img_path, target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        preds = self.model.predict(x)
        return preds[0][1]

    def scannFolder(self, folder):
        self.status.emit(Message('Buscando Archivos...', True))
        self.filesList = searching_all_files(folder)
        count = 0
        self.progressMax.emit(len(self.filesList))
        self.status.emit(Message('Creando Media...', True))
        for f in self.filesList:
            mediaItem = genNewMediaItem()
            updateMediaItem(mediaItem, {
                'MediaID': count,
                'RelativeFilePath': f
            })
            self.media.append(mediaItem)
            count += 1
            self.progress.emit(count)
        self.status.emit(Message('Iniciando Escaneo...', False))
        self.start()

    def scannVIC(self, VIC={}):
        if(isVICValid(VIC)):
            self.media = getMediaFormVIC(VIC)
            if(self.media):
                self.start()
            else:
                self.status.emit(Message('No se pudo recuperar los datos del Archivo VIC!',False, constants.DANGER))
        else:
            self.status.emit(
                Message('Archivo VIC no valido!', False, constants.DANGER))

    def run(self):
        if(not self.model):
            self.model = self.loadModel()
        self.progressMax.emit(len(self.media))
        count = 0
        for m in self.media:
            self.status.emit(Message('Escanenado: ' + str(m['RelativeFilePath']), False))
            #TODO scann code 
            count += 1
            self.progress.emit(count)
        self.status.emit(Message('Escaneo Terminado!', False))
