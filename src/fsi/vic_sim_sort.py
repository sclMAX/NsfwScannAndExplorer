
from time import time
import gc
import pickle
from pathlib import Path
from tempfile import TemporaryFile
import numpy as np
import wget
from psutil import virtual_memory
from PyQt5 import QtCore
import cv2 as cv
from src.fsi.kNN import kNN
from src.utils.sort_utils import find_topk_unique
from src.utils.formats import secondsToHMS
from src.utils import Image as ImgTools
from src.Nsfw.vic13 import updateMediaItem


def imageToCNN(file_path: str, isCaffe: bool):
    try:
        if isCaffe:
            img = ImgTools.load_img(file_path, target_size=(224, 224))
            img_array = ImgTools.img_to_array(img)
            inputblob = cv.dnn.blobFromImage(
                img_array, 1., (224, 224), (104, 117, 123))
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


class ImageCNN(object):
    def __init__(self, mediaItem: dict, base_path: str):
        self.mediaItem = mediaItem
        self.base_path = base_path
        self.features = None
        self.idx: int = 0

    def __processImg(self, isCaffe: bool):
        file_path: str = self.getFilePath()
        return imageToCNN(file_path, isCaffe)

    def getFilePath(self):
        file_path: str = self.mediaItem.get('RelativeFilePath')
        if file_path:
            file_path = file_path.replace('\\', '/')
            media_base_path = Path(file_path).parent
            if Path(self.base_path) != media_base_path.parent:
                file_path = str(Path(self.base_path).joinpath(file_path))
            return file_path
        return ''

    def getData(self, isCaffe: bool):
        return self.__processImg(isCaffe)


class VICMediaSimSort(QtCore.QThread):
    # Signals
    finish: QtCore.pyqtSignal = QtCore.pyqtSignal(list)
    saveMedia: QtCore.pyqtSignal = QtCore.pyqtSignal(list)
    progress: QtCore.pyqtSignal = QtCore.pyqtSignal(int, int)  # value, maximum
    status: QtCore.pyqtSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent: QtCore.QObject, query_img_file: str, media: list, vic_file: str, isBackendCaffe: bool):
        super().__init__(parent)
        # Files paths
        self.parent = parent
        self.isStop: bool = False
        self.base_path: str = str(Path(vic_file).parent)
        self.file_npy: str = str(
            Path(self.base_path).joinpath(Path(vic_file).stem + '.npy'))
        self.file_npy_tmp: str = str(
            Path(self.base_path).joinpath(Path(vic_file).stem + '_tmp.npy'))
        self.isBackendCaffe = isBackendCaffe
        self.setBackendCaffe(isBackendCaffe)
        self.query_img: ImageCNN = None
        self.VICMedia: list = media
        self.__model: object = None
        self.__knn: kNN = None
        self.tInicio: int = None
        self.tInicioProceso: int = None
        self.n_neighbors: int = 0
        self.setQuery_img(query_img_file)

    @QtCore.pyqtSlot(bool)
    def setBackendCaffe(self, isBackendCaffe: bool):
        self.isBackendCaffe = isBackendCaffe

    @QtCore.pyqtSlot()
    def stop(self):
        self.isStop = True

    def setQuery_img(self, query_img_file: str):
        self.query_img = ImageCNN({'RelativeFilePath': query_img_file}, '')

    def __loadModel(self):
        self.progress.emit(0, 0)
        if self.isBackendCaffe:
            try:
                self.status.emit('Cargando Modelo...')
                prototxt = 'model/VGG_ILSVRC_19_layers_deploy.prototxt'
                caffeModel = 'model/VGG_ILSVRC_19_layers.caffemodel'
                self.CaffeOutLayer = 'fc6'
                self.__model = cv.dnn.readNetFromCaffe(
                    prototxt=prototxt, caffeModel=caffeModel)
                del prototxt, caffeModel
            except cv.error:
                self.status.emit(
                    'Faltan archivos para configurar el modelo VGG19!')
                url = 'http://www.robots.ox.ac.uk/~vgg/software/very_deep/caffe/VGG_ILSVRC_19_layers.caffemodel'
                wget.download(url, caffeModel, self.__dowloadProgress)
                self.__loadModel()
        else:
            self.status.emit('Cargando Backend Tensorflow...')
            from keras.applications import VGG19
            from keras.models import Model
            self.status.emit('Cargando VGG19 Model...')
            base_model = VGG19()
            self.status.emit('Configurando VGG19 Model...')
            self.__model = Model(inputs=base_model.input,
                                 outputs=base_model.get_layer('fc1').output)
        self.status.emit('Modelo Cargado!')

    def __dowloadProgress(self, value, maximum, _):
        self.progress.emit(value, maximum)
        self.status.emit('Descargando Configuracion del Modelo... (%.2fMB de %.2fMB)' % (
            value / 1024 / 1024, maximum / 1024 / 1024))

    def __getFeatures(self, img_blob):
        if not self.__model:
            self.__loadModel()
        if self.isBackendCaffe:
            self.__model.setInput(img_blob)
            return np.array(self.__model.forward(self.CaffeOutLayer).flatten())
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

    def __emitLoadStatus(self, total, count: int, file: str, memp):
        t = time()
        if t > self.tInicioProceso:
            et = t - self.tInicioProceso
            fs = count / et
            eta: str = secondsToHMS((total - count) * (et / count))
            self.progress.emit(count, total)
            self.status.emit('Procesando Archivo %d de %d (TT:%s|ETA:%s @%.2f a/s|Mu:%.1f %%) => %s' %
                             (count, total, secondsToHMS(t - self.tInicio), eta, fs, memp, file))

    def __chkResume(self):
        X: list = []
        if Path(self.file_npy_tmp).exists():
            self.status.emit('Cargando archivo de caracteristicas...')
            self.progress.emit(0, 0)
            with open(self.file_npy_tmp, 'r+b')as file:
                X: list = pickle.load(file)
            shape_x = 0
            for _ in X:
                shape_x += 1 
            self.n_neighbors = shape_x if shape_x < 50 else 50
            return True, True, True, X, shape_x
        return True, False, False, X, 0

    def __loadAllImages(self):
        count, self.tInicioProceso = 0, time()
        file_npy_tmp = None
        isComplete, isResume, isMemmap, X, shape_x = self.__chkResume()
        save_file: str = self.file_npy
        total = len(self.VICMedia)
        for item in self.VICMedia:
            try:
                count += 1
                if isResume:
                    idKnn = item.get('IdKNN')
                    if idKnn != shape_x:
                        continue
                    else:
                        isResume = False
                if self.isStop:
                    save_file = self.file_npy_tmp
                    isComplete = False
                    break
                file_path = self.getFilePath(item)
                if not file_path:
                    continue
                mem = virtual_memory()
                self.__emitLoadStatus(total, count, file_path, mem.percent)
                img_blob = imageToCNN(file_path, self.isBackendCaffe)
                coment = item.get('Comments')
                updateMediaItem(item, {
                    'Comments': coment,
                    'IdKNN': shape_x
                })
                X.append(self.__getFeatures(img_blob))
                shape_x += 1
                if self.n_neighbors < 50:
                    self.n_neighbors += 1
                else:
                    self.n_neighbors = 50
                if mem.percent > 40 and not isMemmap:
                    print('MEMMAP ACTIVADO!')
                    self.status.emit('Activando Mapeo de Memoria...')
                    self.progress.emit(0, 0)
                    isMemmap = True
                    file_npy_tmp = TemporaryFile()
                    np.save(file_npy_tmp, X)
                    file_npy_tmp.close()
                    X: list = np.load(file_npy_tmp, mmap_mode='r+')
            except (ValueError, SyntaxError, OSError, TypeError, RuntimeError):
                item['IdKNN'] = -1
                print('IMAGEN ERROR:', file_path)
                continue
        self.__prepareKNN(X)
        self.status.emit('Guardando datos escaneados...')
        self.progress.emit(0, 0)
        if file_npy_tmp:
            file_npy_tmp.close()
        with open(save_file, 'w+b') as file:
            pickle.dump(X, file, protocol=pickle.HIGHEST_PROTOCOL)
        if isComplete and Path(self.file_npy_tmp).exists():
            Path(self.file_npy_tmp).unlink()
        print('TIEMPO ESCANEO DE IMAGENES:',
              secondsToHMS(time() - self.tInicio))

    def __prepareKNN(self, X):
        self.__knn = kNN()
        self.__knn.compile(n_neighbors=self.n_neighbors,
                           algorithm="auto", metric="cosine")
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
            return True
        return False

    def __orderIndices(self):
        self.status.emit('Analizando Media Items...')
        self.progress.emit(0, 0)
        distances, indices = self.__knn.predict(
            np.array([self.query_img.features]))
        distances = distances.flatten()
        indices = indices.flatten()
        indices, distances = find_topk_unique(
            indices, distances, self.n_neighbors)
        del distances
        gc.collect()
        return indices

    def run(self):
        self.tInicio = time()
        self.isStop = False
        self.status.emit('Escaneando Imagen de muestra...')
        self.progress.emit(0, 0)
        self.query_img.features = self.__getFeatures(
            self.query_img.getData(self.isBackendCaffe))
        if not self.__knn or Path(self.file_npy_tmp).exists():
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
                idKnn = media.get('IdKNN')
                if idKnn == idx:
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
