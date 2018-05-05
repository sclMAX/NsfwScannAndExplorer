
from time import time
import sys
import tempfile
import pickle
import shelve
from pathlib import Path
import numpy as np
from PyQt5 import QtCore
import cv2 as cv
from src.fsi.kNN import kNN
from src.utils.sort_utils import find_topk_unique
from src.utils.formats import secondsToHMS

from src.utils import Image as ImgTools


class ImageCNN(object):
    count: int = 0
    def __init__(self, mediaItem: dict, base_path: str):
        self.mediaItem = mediaItem
        self.base_path = base_path
        self.idx: int = ImageCNN.count
        ImageCNN.count += 1


    def __processImg(self):
        try:
            file_path: str = self.getFilePath()
            img = ImgTools.load_img(file_path, target_size=(224, 224))
            img_array = ImgTools.img_to_array(img)
            inputblob = cv.dnn.blobFromImage(img_array, 1., (224, 224), (104, 117, 123))
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

class ListImageCNN(object):
    

    def __init__(self, img_list_file: str):
        self.__count: int = 0
        self.__list_file = open(img_list_file, 'r+b')
        self.__count = len(self.__list_file.keys())
        self.__next_idx: int = self.__count

    def append(self, item: ImageCNN):
        self.__list_file[str(self.__next_idx)] = item
        self.__next_idx += 1

    def remove(self, index: int):
        del self.__list_file[str(index)]
        self.__count = len(self.__list_file.keys())

    def getCount(self):
        return self.__count

    def getItemsItr(self):
        for idx in range(self.__count):
            item = self.getOne(str(idx))
            yield item

    def getOne(self, index: int):
        index = str(index)
        if index in self.__list_file.keys():
            return self.__list_file[index]
        return None

    def close(self):
        self.__list_file.close()


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
        self.query_img: ImageCNN = ImageCNN({'RelativeFilePath': query_img_file}, '')
        self.VICMedia: list = media
        self.__img_list: list = []
        self.__model: object = None
        self.__knn: kNN = None
        self.tInicio = 0
        if features_file:
            self.loadFeaturesFromFile(features_file)

    def __loadModel(self):
        self.status.emit('Cargando Modelo...')
        try:
            prototxt = 'model/VGG_ILSVRC_19_layers_deploy.prototxt'
            caffeModel = 'model/VGG_ILSVRC_19_layers.caffemodel'
            model_loaded = cv.dnn.readNetFromCaffe(prototxt=prototxt, caffeModel=caffeModel)
            self.__model = model_loaded
            self.status.emit('Modelo Cargado!')
        except:
            self.status.emit('Faltan archivos para configurar el modelo VGG19!')
            raise

    def __setFeatures(self, img: ImageCNN):
        if not self.__model:
            self.__loadModel()
        self.__model.setInput(img.getData())
        pred = self.__model.forward('pool4').flatten()
        img.features = np.array(pred)

    def __loadAllImages(self):
        count: int = 0
        total: int = len(self.VICMedia)
        self.progress.emit(count, total)
        tInicioProceso = time()
        for item in self.VICMedia:
            try:
                count += 1
                self.progress.emit(count, total)
                img = ImageCNN(item, self.base_path)
                print('COUNT:', ImageCNN.count)
                print('count:', img.count)
                et = time() - tInicioProceso
                fs = count / et if et > 0 else 1
                eta: str = secondsToHMS((total - count) * (et / count))
                self.status.emit(
                    'Procesando Archivo %d de %d (ETA: %s @%.2f a/s) => %s' % (count, total, eta, fs, img.getFilePath()))
                self.__setFeatures(img)
                self.__img_list.append(img)
            except (ValueError, SyntaxError, OSError, TypeError, RuntimeError):
                print('ERROR:', img.getFilePath())
                continue

    def saveFeaturesToFile(self, file_path: str):
        with open(file_path, 'wb') as f:
            pickle.dump(self.__img_list, f)

    def loadFeaturesFromFile(self, file_path: str):
        self.status.emit('Cargando Archivo de Escaneo...')
        try:
            with open(file_path, 'rb') as f:
                self.__img_list = pickle.load(f)
            print('TAMAÑO: ', sys.getsizeof(self.__img_list))
            self.isFeaturesLoad = True
        except IOError:
            self.isFeaturesLoad = False
            self.status.emit('Error al cargar Archivo de Escaneo Previo!')
            print('Error al cargar Archivo de Escaneo Previo!')

    def __prepareKNN(self, n_neighbors: int, totalItems: int):
        self.__knn = kNN()
        self.__knn.compile(n_neighbors=n_neighbors,
                           algorithm="brute", metric="cosine")
        x_file = tempfile.TemporaryFile()
        X = np.memmap(x_file, mode='w+', shape=(totalItems,
                                                self.query_img.features.shape[0]))
        Xidx: int = 0
        for item in self.__img_list:
            X[Xidx] = item.features
            Xidx += 1
        self.__knn.fit(X)
        x_file.close()

    def __orderIndices(self, n_neighbors: int):
        distances, indices = self.__knn.predict(
            np.array([self.query_img.features]))
        distances = distances.flatten()
        indices = indices.flatten()
        indices, distances = find_topk_unique(indices, distances, n_neighbors)
        return indices

    def run(self):
        self.tInicio = time()
        self.__setFeatures(self.query_img)
        self.__img_list.append(self.query_img)
        if not self.isFeaturesLoad:
            self.__loadAllImages()
        print('TAMAÑO: ', sys.getsizeof(self.__img_list))
        totalItems = len(self.__img_list)
        n_neighbors = totalItems if totalItems < 50 else 50
        self.status.emit('Procesando Imagenes...')
        self.__prepareKNN(n_neighbors, totalItems)
        indices = self.__orderIndices(n_neighbors)
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
        self.status.emit('Proceso terminado en %s!' %
                         secondsToHMS(time() - self.tInicio))
        self.progress.emit(0, -1)
        self.finish.emit(resultMedia)
