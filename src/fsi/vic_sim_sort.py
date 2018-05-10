
from time import time
import gc
from pathlib import Path
import numpy as np
import wget
from PyQt5 import QtCore
import cv2 as cv
from src.fsi.kNN import kNN
from src.utils.sort_utils import find_topk_unique
from src.utils.formats import secondsToHMS
from src.utils import Image as ImgTools

isCaffe: bool = True

class ImageCNN(object):
    def __init__(self, mediaItem: dict, base_path: str):
        self.mediaItem = mediaItem
        self.base_path = base_path
        self.features = None
        self.idx: int = 0

    def __processImg(self):
        file_path: str = self.getFilePath()
        return imageToCNN(file_path)

    def getFilePath(self):
        file_path: str = self.mediaItem.get('RelativeFilePath')
        if file_path:
            file_path = file_path.replace('\\', '/')
            media_base_path = Path(file_path).parent
            if Path(self.base_path) != media_base_path.parent:
                file_path = str(Path(self.base_path).joinpath(file_path))
            return file_path
        return ''

    def getData(self):
        return self.__processImg()

def imageToCNN(file_path: str):
    try:
        if isCaffe:
            img = ImgTools.load_img(file_path, target_size=(224, 224))
            img_array = ImgTools.img_to_array(img)
            inputblob = cv.dnn.blobFromImage(
                img_array, 1., (224, 224), (104, 117, 123))
            del img, img_array
            return inputblob
        else:
            from keras.preprocessing import image
            from src.utils.imagenet_utils import preprocess_input
            img = image.load_img(file_path, target_size=(224, 224))
            img = image.img_to_array(img)
            img = np.expand_dims(img, axis=0)
            img = preprocess_input(img)
            return img
    except:
        raise

class VICMediaSimSort(QtCore.QThread):
    # Signals
    finish: QtCore.pyqtSignal = QtCore.pyqtSignal(list)
    saveMedia: QtCore.pyqtSignal = QtCore.pyqtSignal(list)
    progress: QtCore.pyqtSignal = QtCore.pyqtSignal(int, int)  # value, maximum
    status: QtCore.pyqtSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent: QtCore.QObject, query_img_file: str, media: list, vic_file: str):
        super().__init__(parent)
        #Files paths
        self.base_path: str = str(Path(vic_file).parent)
        self.file_csv: str = str(Path(self.base_path).joinpath(Path(vic_file).stem + '.csv'))
        self.file_knn: str = str(Path(self.base_path).joinpath(Path(vic_file).stem + '.knn'))
        self.file_npy: str = str(Path(self.base_path).joinpath(Path(vic_file).stem + '.npy'))
        self.query_img: ImageCNN = None
        self.VICMedia: list = media
        self.__model: object = None
        self.__knn: kNN = None
        self.tInicio: int = None
        self.tInicioProceso: int = None
        self.n_neighbors: int = 0
        self.setQuery_img(query_img_file)

    def setQuery_img(self, query_img_file: str):
        self.query_img = ImageCNN({'RelativeFilePath': query_img_file}, '')

    def __loadModel(self):
        self.progress.emit(0, 0)
        if isCaffe:
            try:
                self.status.emit('Cargando Modelo...')
                prototxt = 'model/VGG_ILSVRC_19_layers_deploy.prototxt'
                caffeModel = 'model/VGG_ILSVRC_19_layers.caffemodel'
                self.__model = cv.dnn.readNetFromCaffe(prototxt=prototxt, caffeModel=caffeModel)
                del prototxt, caffeModel
            except cv.error:
                self.status.emit(
                    'Faltan archivos para configurar el modelo VGG19!')
                url = 'http://www.robots.ox.ac.uk/~vgg/software/very_deep/caffe/VGG_ILSVRC_19_layers.caffemodel'
                wget.download(url, caffeModel, self.__dowloadProgress)
                self.__loadModel()
        else:
            self.status.emit('Cargando Backend Tensorflow...')
            from src.fsi.vgg19 import VGG19
            from keras.models import Model
            self.status.emit('Cargando VGG19 Model...')
            base_model = VGG19(weights='imagenet')
            self.status.emit('Configurando VGG19 Model...')
            #self.__model = Model(inputs=base_model.input, outputs=base_model.get_layer('block3_pool').output)
            #self.__model = Model(inputs=base_model.input, outputs=base_model.get_layer('block4_pool').output)
            #self.__model = Model(inputs=base_model.input, outputs=base_model.get_layer('block5_pool').output)
            self.__model = Model(inputs=base_model.input, outputs=base_model.get_layer('fc1').output)
        self.status.emit('Modelo Cargado!')

    def __dowloadProgress(self, value, maximum, _):
        self.progress.emit(value, maximum)
        self.status.emit('Descargando Configuracion del Modelo... (%.2fMB de %.2fMB)' % (
            value / 1024 / 1024, maximum / 1024 / 1024))

    def __getFeatures(self, img_blob):
        if not self.__model:
            self.__loadModel()
        if isCaffe:
            self.__model.setInput(img_blob)
            # return np.array(self.__model.forward('pool3').flatten())
            # return np.array(self.__model.forward('pool4').flatten())
            # return np.array(self.__model.forward('pool5').flatten())
            return np.array(self.__model.forward('fc6').flatten())
        else:
            return np.array(self.__model.predict(img_blob).flatten())

    def getFilePath(self, mediaItem: dict):
        file_path: str = mediaItem.get('RelativeFilePath')
        if file_path:
            file_path = file_path.replace('\\', '/')
            media_base_path = Path(file_path).parent
            if Path(self.base_path) != media_base_path.parent:
                file_path = str(Path(self.base_path).joinpath(file_path))
            return file_path
        return ''

    def __emitLoadStatus(self, count: int, file: str):
        total, t = len(self.VICMedia), time()
        et = t - self.tInicioProceso
        fs = count / et if et > 0 else 1
        eta: str = secondsToHMS((total - count) * (et / count))
        self.progress.emit(count, total)
        self.status.emit('Procesando Archivo %d de %d (%s | ETA: %s @%.2f a/s) => %s' % (count, total, secondsToHMS(t - self.tInicio), eta, fs, file))
        del total, t, et, fs, eta

    def __loadAllImages(self):
        count, self.tInicioProceso = 0, time()
        # np.save(self.file_npy, np.array([], dtype='float'))
        # X = np.load(self.file_npy, mmap_mode='w+')
        from tempfile import TemporaryFile
        f = TemporaryFile()
        X = np.memmap(f, mode='w+', dtype='float', shape=(1, 1))
        shape_x = 0
        for item in self.VICMedia:
            try:
                count += 1
                file_path = self.getFilePath(item)
                if not file_path:
                    continue
                self.__emitLoadStatus(count, file_path)
                img_blob = imageToCNN(file_path)
                idxStr = str(shape_x)
                item['IdKNN'] = shape_x
                shape_x += 1
                X = np.resize(X, (shape_x, self.query_img.features.shape[0]))
                X[int(idxStr)] = self.__getFeatures(img_blob)
                if self.n_neighbors < 50:
                    self.n_neighbors += 1
                else:
                    self.n_neighbors = 50
                gc.collect()
            except (ValueError, SyntaxError, OSError, TypeError, RuntimeError):
                item['IdKNN'] = -1
                print('IMAGEN ERROR:', file_path)
                continue
        self.__prepareKNN(X)
        self.status.emit('Guardando datos KNN Net...')
        self.progress.emit(0, 0)
        f.close()
        np.save(self.file_npy, X)
        print('TIEMPO ESCANEO DE IMAGENES:', secondsToHMS(time() - self.tInicio))
        del count, X, shape_x, file_path
        gc.collect()

    def __prepareKNN(self, X):
        self.__knn = kNN()
        self.__knn.compile(n_neighbors=self.n_neighbors, algorithm="auto", metric="cosine")
        self.status.emit('Entrenando KNN Net...')
        self.progress.emit(0, 0)
        self.__knn.fit(X)

    def setN_neighbors(self):
        count: int = 0
        total: int = len(self.VICMedia)
        for item in self.VICMedia:
            count += 1
            self.progress.emit(count, total)
            idKNN = item.get('IdKNN')
            if idKNN and idKNN >= 0:
                if self.n_neighbors < 50:
                    self.n_neighbors += 1
                else:
                    break

    def __loadKNN(self):
        if Path(self.file_npy).exists():
            self.status.emit('Cargando archivo de caracteristicas...')
            self.progress.emit(0, 0)
            X = np.load(self.file_npy, mmap_mode='r+')
            self.setN_neighbors()
            self.__prepareKNN(X)
            del X
            gc.collect()
            return True
        return False

    def __orderIndices(self):
        self.status.emit('Analizando Media Items...')
        self.progress.emit(0, 0)
        distances, indices = self.__knn.predict(np.array([self.query_img.features]))
        distances = distances.flatten()
        indices = indices.flatten()
        indices, distances = find_topk_unique(indices, distances, self.n_neighbors)
        del distances
        gc.collect()
        return indices

    def run(self):
        self.tInicio = time()
        self.status.emit('Escaneando Imagen de muestra...')
        self.progress.emit(0, 0)
        self.query_img.features = self.__getFeatures(self.query_img.getData())
        if not self.__knn:
            idKNN = self.VICMedia[0].get('IdKNN')
            if not self.__loadKNN() or not isinstance(idKNN, int):
                self.__loadAllImages()
                self.saveMedia.emit(self.VICMedia)
            else:
                self.status.emit('Calculando Media Items...')
                self.setN_neighbors()
        indices = self.__orderIndices()
        resultMedia: list = []
        imgs = indices[0]
        count: int = 0
        total: int = len(imgs)
        for idx in imgs:
            count += 1
            self.status.emit('Reordenando Imagen %d de %d...' % (count, total))
            self.progress.emit(count, total)
            for media in self.VICMedia:
                if media['IdKNN'] == idx:
                    self.VICMedia.remove(media)
                    resultMedia.append(media)
                    break
        resultMedia.extend(self.VICMedia)
        self.VICMedia = resultMedia
        self.status.emit('Proceso terminado en %s!' %
                         secondsToHMS(time() - self.tInicio))
        self.progress.emit(0, -1)
        self.finish.emit(resultMedia)
        del indices, resultMedia
        gc.collect()
