
from time import time
import pickle
import numpy as np
from PyQt5 import QtCore
from keras.models import Model
from keras.preprocessing import image
import keras.backend as K
from src.utils.imagenet_utils import preprocess_input
from src.fsi.vgg19 import VGG19
from src.fsi.kNN import kNN
from src.utils.sort_utils import find_topk_unique
from src.utils.formats import secondsToHMS


class ImageCNN(object):
    def __init__(self, img_file: str, target_size: tuple):
        self.__file_path: str = img_file
        self.__cnn_img = None
        self.mediaItem = None
        self.width, self.height = target_size
        self.__processImg()
        self.features = None

    def __processImg(self):
        __img = image.load_img(self.__file_path, target_size=(self.width, self.height))
        __img = image.img_to_array(__img)
        __img = np.expand_dims(__img, axis=0)
        self.__cnn_img = preprocess_input(__img)

    def getFilePath(self):
        return self.__file_path

    def getData(self):
        return self.__cnn_img


class VICMediaSimSort(QtCore.QThread):
    #Signals
    finish: QtCore.pyqtSignal = QtCore.pyqtSignal(list)
    progress: QtCore.pyqtSignal = QtCore.pyqtSignal(int, int) #value, maximum
    status: QtCore.pyqtSignal = QtCore.pyqtSignal(str)

    isFeaturesLoad: bool = False

    def __init__(self, parent: QtCore.QObject, query_img_file: str, media: list, features_file: str = None):
        super().__init__(parent)
        self.status.emit('INICIANDO PROCESO...')
        self.__X = []
        self.query_img: ImageCNN = ImageCNN(query_img_file, (224, 224))
        self.VICMedia: list = media
        self.__img_list: list = []
        self.__model: Model = None
        self.__knn: kNN = None
        self.tInicio = 0
        self.__setFeatures(self.query_img)
        self.__X.append(self.query_img.features)
        if features_file:
            self.loadFeaturesFromFile(features_file)

    def __loadModel(self):
        self.status.emit('Cargando Modelo...')
        K.clear_session()
        base_model = VGG19(weights='imagenet')
        self.__model = Model(inputs=base_model.input,
                             outputs=base_model.get_layer('block4_pool').output)
        self.status.emit('Modelo Cargado!')

    def __setFeatures(self, img: ImageCNN):
        if not self.__model:
            self.__loadModel()
        img.features = np.array(self.__model.predict(img.getData()).flatten())

    def __loadAllImages(self):
        count: int = 0
        total: int = len(self.VICMedia)
        self.progress.emit(count, total)
        tInicioProceso = time()
        for item in self.VICMedia:
            try:
                count += 1
                self.progress.emit(count, total)
                img_file = str(item['RelativeFilePath']).replace('\\', '/')
                et = time() - tInicioProceso
                fs = count / et if et > 0 else 1
                eta: str = secondsToHMS((total - count) * (et / count))
                self.status.emit('Procesando Archivo %d de %d (ETA: %s @%.2f a/s) => %s' % (count, total, eta, fs, img_file))
                img = ImageCNN(img_file, (224, 224))
                self.__setFeatures(img)
                img.mediaItem = item
                self.__X.append(img.features)
                self.__img_list.append(img)
            except (ValueError, OSError):
                continue
        self.__X = np.array(self.__X)

    def __loadKNN(self, n_neighbors: int):
        self.__knn = kNN()
        self.__knn.compile(n_neighbors=n_neighbors,
                           algorithm="brute", metric="cosine")
        self.__knn.fit(self.__X)

    def saveFeaturesToFile(self, file_path: str):
        with open(file_path, 'wb') as f:
            pickle.dump(self.__img_list, f)

    def loadFeaturesFromFile(self, file_path: str):
        self.status.emit('Cargando Archivo de Escaneo...')
        try:
            with open(file_path, 'rb') as f:
                self.__img_list = pickle.load(f)
                self.__X = []
            total: int = len(self.__img_list)
            count: int = 0
            for img in self.__img_list:
                count += 1
                self.__X.append(img.features)
                self.progress.emit(count, total)
            self.__X = np.array(self.__X)
            self.isFeaturesLoad = True
        except IOError:
            self.isFeaturesLoad = False
            self.status.emit('Error al cargar Archivo de Escaneo Previo!')
            print('Error al cargar Archivo de Escaneo Previo!')


    def run(self):
        self.tInicio = time()
        self.__img_list.append(self.query_img)
        if not self.isFeaturesLoad:
            self.__loadAllImages()
        n_neighbors = len(self.__X)
        self.status.emit('Procesando Imagenes...')
        self.__loadKNN(n_neighbors)
        distances, indices = self.__knn.predict(np.array([self.query_img.features]))
        distances = distances.flatten()
        indices = indices.flatten()
        indices, distances = find_topk_unique(indices, distances, n_neighbors)
        resultMedia: list = []
        imgs = indices[0]
        count: int = 0
        total: int = len(imgs)
        self.progress.emit(count, total)
        for idx in imgs:
            img = self.__img_list[idx]
            count += 1
            self.status.emit('Reordenando Imagen %d de %d...' % (count, total))
            self.progress.emit(count, total)
            if img.mediaItem in self.VICMedia:
                self.VICMedia.remove(img.mediaItem)
                resultMedia.append(img.mediaItem)
        resultMedia.extend(self.VICMedia)
        self.__img_list.remove(self.query_img)
        self.status.emit('Proceso terminado en %s!' % secondsToHMS(time() - self.tInicio))
        self.progress.emit(0, -1)
        self.finish.emit(resultMedia)
