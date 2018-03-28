from PyQt5 import QtCore
from src.utils import constants
from src.utils.message import Message


class NsfwScann(QtCore.QThread):
    #Model 
    model = None
    weight_file = 'model/max_open_nsfw.h5'
    model_file = 'model/max_open_nsfw.json'
    #Signals
    status = QtCore.pyqtSignal(Message)

    def __init__(self, parent=None):
        super().__init__(parent)

    def loadModel(self):
        msg = Message('Cargando Backend Tensorflow...')
        self.status.emit(msg)
        from keras import backend as K
        from keras.models import model_from_json
        try:
            K.clear_session()
            msg = Message('Cargando Modelo...')
            self.status.emit(msg)
            json_file = open(self.model_file, 'r')
            loaded_model_json = json_file.read()
            msg = Message('Configurando Modelo...')
            self.status.emit(msg)
            model = model_from_json(loaded_model_json)
            model.load_weights(self.weight_file)
            msg = Message('Modelo Configurado!')
            self.status.emit(msg)
            return model
        except(FileNotFoundError):
            raise FileNotFoundError('No se encontraron los archivos del Modelo!')
        finally:
            if json_file:
                json_file.close()
    
    def scannFolder(self, folder):        
        print('IMAGE_PATH:', folder)
        self.start()
    
    def scannVIC(self, vicJsonFile):
        pass
    
    def run(self):
        if(not self.model):
            self.model = self.loadModel()
        print('START')
