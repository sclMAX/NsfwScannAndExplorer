
from time import time
import gc
import tempfile
from pathlib import Path
import pickle
import numpy as np
import klepto
import wget
from PyQt5 import QtCore
import cv2 as cv
from src.fsi.kNN import kNN
from src.utils.sort_utils import find_topk_unique
from src.utils.formats import secondsToHMS
from src.utils import Image as ImgTools


class ImageCNN(object):
    def __init__(self, mediaItem: dict, base_path: str):
        self.mediaItem = mediaItem
        self.base_path = base_path
        self.features = None
        self.idx: int = 0

    def __processImg(self):
        try:
            file_path: str = self.getFilePath()
            img = ImgTools.load_img(file_path, target_size=(224, 224))
            img_array = ImgTools.img_to_array(img)
            inputblob = cv.dnn.blobFromImage(
                img_array, 1., (224, 224), (104, 117, 123))
            return inputblob
        except:
            print('ERROR read image:', file_path)
            raise

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


class VICMediaSimSort(QtCore.QThread):
    # Signals
    finish: QtCore.pyqtSignal = QtCore.pyqtSignal(list)
    progress: QtCore.pyqtSignal = QtCore.pyqtSignal(int, int)  # value, maximum
    status: QtCore.pyqtSignal = QtCore.pyqtSignal(str)

    isFeaturesLoad: bool = False

    def __init__(self, parent: QtCore.QObject, query_img_file: str, media: list, features_file: str = None, base_path: str = ''):
        super().__init__(parent)
        self.status.emit('INICIANDO PROCESO...')
        self.base_path = base_path
        self.query_img: ImageCNN = ImageCNN(
            {'RelativeFilePath': query_img_file}, '')
        self.VICMedia: list = media
        self.features_file = features_file
        self.img_list = None
        self.__model: object = None
        self.__knn: kNN = None
        self.tInicio = 0

    def __loadModel(self):
        self.status.emit('Cargando Modelo...')
        try:
            prototxt = 'model/VGG_ILSVRC_19_layers_deploy.prototxt'
            caffeModel = 'model/VGG_ILSVRC_19_layers.caffemodel'
            self.__model = cv.dnn.readNetFromCaffe(
                prototxt=prototxt, caffeModel=caffeModel)
            self.status.emit('Modelo Cargado!')
        except:
            self.status.emit(
                'Faltan archivos para configurar el modelo VGG19!')
            url = 'http://www.robots.ox.ac.uk/~vgg/software/very_deep/caffe/VGG_ILSVRC_19_layers.caffemodel'
            wget.download(url, caffeModel, self.__dowloadProgress)
            self.__loadModel()

    def __dowloadProgress(self, value, maximum, width):
        self.progress.emit(value, maximum)
        self.status.emit('Descargando Configuracion del Modelo... (%.2fMB de %.2fMB)' % (
            value / 1024 / 1024, maximum / 1024 / 1024))

    def __setFeatures(self, img: ImageCNN):
        if not self.__model:
            self.__loadModel()
        self.__model.setInput(img.getData())
        pred = self.__model.forward('pool4').flatten()
        img.features = np.array(pred)
        del pred
        gc.collect()

    def __loadAllImages(self):
        count: int = 0
        total: int = len(self.VICMedia)
        self.progress.emit(count, total)
        tInicioProceso = time()
        img_idx: int = 0
        dump_count: int = 0
        for item in self.VICMedia:
            try:
                count += 1
                self.progress.emit(count, total)
                img = ImageCNN(item, self.base_path)
                et = time() - tInicioProceso
                fs = count / et if et > 0 else 1
                eta: str = secondsToHMS((total - count) * (et / count))
                self.status.emit(
                    'Procesando Archivo %d de %d (ETA: %s @%.2f a/s) => %s' % (count, total, eta, fs, img.getFilePath()))
                self.__setFeatures(img)
                img.idx = img_idx
                img_idx += 1
                self.img_list[str(img.idx)] = img
                dump_count += 1
                if dump_count > 100:
                    self.status.emit('Volcando cache de memoria al disco...')
                    self.img_list.dump()
                    dump_count = 0
            except (ValueError, SyntaxError, OSError, TypeError, RuntimeError):
                print('ERROR:', img.getFilePath())
                continue
        self.img_list.dump()

    def __prepareKNN(self, n_neighbors: int, totalItems: int):
        self.__knn = kNN()
        self.__knn.compile(n_neighbors=n_neighbors,
                           algorithm="brute", metric="cosine")
        x_file = tempfile.TemporaryFile()
        X = np.memmap(x_file, mode='w+', shape=(totalItems,
                                                self.query_img.features.shape[0]))
        Xidx: int = 0
        total: int = len(self.img_list.keys())
        count: int = 0
        self.status.emit('Cargando caracteristicas...')
        for item in self.img_list.keys():
            X[Xidx] = self.img_list.get(item).features
            Xidx += 1
            count += 1
            self.progress.emit(count, total)
        self.__knn.fit(X)
        x_file.close()
        del Xidx
        del count
        del total
        del X
        del x_file
        gc.collect()

    def __orderIndices(self, n_neighbors: int):
        distances, indices = self.__knn.predict(
            np.array([self.query_img.features]))
        distances = distances.flatten()
        indices = indices.flatten()
        indices, distances = find_topk_unique(indices, distances, n_neighbors)
        del distances
        gc.collect()
        return indices

    def freeMem(self):
        del self.__knn
        del self.__model
        del self.query_img
        gc.collect()

    def run(self):
        self.tInicio = time()
        self.status.emit('Cargando datos de escaneo previo...')
        self.img_list = klepto.archives.file_archive(
            self.features_file,
            serialized=True,
            cached=False,
            protocol=pickle.HIGHEST_PROTOCOL
        )
        self.__setFeatures(self.query_img)
        data = self.img_list.get('0')
        if data:
            self.isFeaturesLoad = True
        if not self.isFeaturesLoad:
            self.__loadAllImages()
        totalItems = len(self.img_list.keys())
        n_neighbors = totalItems if totalItems < 50 else 50
        self.status.emit('Procesando Imagenes...')
        self.__prepareKNN(n_neighbors, totalItems)
        indices = self.__orderIndices(n_neighbors)
        self.freeMem()
        resultMedia: list = []
        imgs = indices[0]
        count: int = 0
        total: int = len(imgs)
        self.progress.emit(count, total)
        for idx in imgs:
            img = self.img_list.get(str(idx))
            count += 1
            self.status.emit('Reordenando Imagen %d de %d...' % (count, total))
            self.progress.emit(count, total)
            if img.mediaItem in self.VICMedia:
                self.VICMedia.remove(img.mediaItem)
                resultMedia.append(img.mediaItem)
        resultMedia.extend(self.VICMedia)
        self.status.emit('Proceso terminado en %s!' %
                         secondsToHMS(time() - self.tInicio))
        self.progress.emit(0, -1)
        self.finish.emit(resultMedia)
        del indices
        del resultMedia
        del self.img_list
        del self.VICMedia
        gc.collect()
