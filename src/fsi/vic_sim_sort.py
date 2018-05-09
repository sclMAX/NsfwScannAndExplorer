
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
        file_path: str = self.getFilePath()
        img = ImgTools.load_img(file_path, target_size=(224, 224))
        img_array = ImgTools.img_to_array(img)
        inputblob = cv.dnn.blobFromImage(
            img_array, 1., (224, 224), (104, 117, 123))
        del file_path, img, img_array
        gc.collect()
        return inputblob

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

    def getSize(self):
        import sys
        tam_item: int = sys.getsizeof(self.mediaItem)
        tam_item += sys.getsizeof(self.base_path)
        tam_item += sys.getsizeof(self.idx)
        tam_item += sys.getsizeof(self.features)
        tam_item += sys.getsizeof(self)
        return tam_item


class VICMediaSimSort(QtCore.QThread):
    # Signals
    finish: QtCore.pyqtSignal = QtCore.pyqtSignal(list)
    progress: QtCore.pyqtSignal = QtCore.pyqtSignal(int, int)  # value, maximum
    status: QtCore.pyqtSignal = QtCore.pyqtSignal(str)

    def __init__(self, parent: QtCore.QObject, query_img_file: str, media: list, features_file: str = None, base_path: str = ''):
        super().__init__(parent)
        self.base_path = base_path
        self.query_img: ImageCNN = ImageCNN({'RelativeFilePath': query_img_file}, '')
        self.VICMedia: list = media
        self.features_file = features_file
        self.img_list = None
        self.__model: object = None
        self.__knn: kNN = None
        self.tInicio = 0
        self.n_neighbors: int = 0

    def __loadModel(self):
        try:
            self.status.emit('Cargando Modelo...')
            prototxt = 'model/VGG_ILSVRC_19_layers_deploy.prototxt'
            caffeModel = 'model/VGG_ILSVRC_19_layers.caffemodel'
            self.__model = cv.dnn.readNetFromCaffe(prototxt=prototxt, caffeModel=caffeModel)
            self.status.emit('Modelo Cargado!')
        except cv.error:
            self.status.emit(
                'Faltan archivos para configurar el modelo VGG19!')
            url = 'http://www.robots.ox.ac.uk/~vgg/software/very_deep/caffe/VGG_ILSVRC_19_layers.caffemodel'
            wget.download(url, caffeModel, self.__dowloadProgress)
            self.__loadModel()

    def __dowloadProgress(self, value, maximum, _):
        self.progress.emit(value, maximum)
        self.status.emit('Descargando Configuracion del Modelo... (%.2fMB de %.2fMB)' % (
            value / 1024 / 1024, maximum / 1024 / 1024))

    def __getFeatures(self, img: ImageCNN):
        if not self.__model:
            self.__loadModel()
        self.__model.setInput(img.getData())
        return np.array(self.__model.forward('pool4').flatten())

    def __calcMemCache(self):
        from psutil import virtual_memory
        mem = virtual_memory()
        tam_item: int = self.query_img.getSize()
        dump_limit: int = (mem.available // 1.2) // tam_item
        print('Mem.available', mem.available)
        print('Tam Image:', tam_item)
        print('Dump_limit:', dump_limit)
        return dump_limit

    def __loadAllImages(self):
        #TODO Ver usar JSON para optimiazar recurso
        tInicioProceso = time()
        count, total = 0, len(self.VICMedia)
        dump_idxs: list = []
        dump_limit: int = self.__calcMemCache()
        tdump, cdump = 0, 0
        x_file = tempfile.TemporaryFile()
        X = np.memmap(x_file, mode='w+', dtype='float16', shape=(1, 1))
        img_idx, shape_y = 0, self.query_img.features.shape[0]
        for item in self.VICMedia:
            try:
                count += 1
                self.progress.emit(count, total)
                img = ImageCNN(item, self.base_path)
                et = time() - tInicioProceso
                tt = secondsToHMS(time() - self.tInicio)
                fs = count / et if et > 0 else 1
                eta: str = secondsToHMS((total - count) * (et / count))
                self.status.emit(
                    'Procesando Archivo %d de %d (ETA: %s @%.2f a/s | %s) => %s' % (count, total, eta, fs, tt, img.getFilePath()))
                feature = self.__getFeatures(img)
                img.idx = img_idx
                img_idx += 1
                X = np.resize(X, (img_idx, shape_y))
                X[img.idx] = feature
                dump_idxs.append(str(img.idx))
                self.img_list[str(img.idx)] = img
                if self.n_neighbors < 50:
                    self.n_neighbors += 1
                tdump = len(dump_idxs)
                if tdump >= dump_limit:
                    self.status.emit('Volcando cache de memoria al disco...')
                    for dId in dump_idxs:
                        self.progress.emit(cdump, tdump)
                        self.img_list.dump(dId)
                        self.img_list.pop(dId)
                        cdump += 1
                    dump_idxs.clear()
                    cdump = 0
            except (ValueError, SyntaxError, OSError, TypeError, RuntimeError):
                print('IMAGEN ERROR:', img.getFilePath())
                continue
        self.status.emit('Volcando cache a disco...')
        for dId in dump_idxs:
            self.progress.emit(cdump, tdump)
            self.img_list.dump(dId)
            self.img_list.pop(dId)
            cdump += 1
        self.__prepareKNN(X)
        x_file.close()
        print('TIEMPO ESCANEO DE IMAGENES:', secondsToHMS(time() - self.tInicio))
        del count, total, tInicioProceso, img_idx, dump_idxs
        del et, fs, eta, tdump, cdump
        del x_file, X
        gc.collect()

    def __prepareKNN(self, X):
        self.__knn = kNN()
        self.__knn.compile(n_neighbors=self.n_neighbors, algorithm="auto", metric="cosine")
        self.status.emit('Preparando KNN net...')
        self.__knn.fit(X)
        self.status.emit('Guardando net KNN...')
        with open(self.features_file + '.knn', 'w+b') as f_knn:
            pickle.dump(self.__knn, f_knn)

    def __loadKNN(self):
        if Path(self.features_file + '.knn').exists():
            with open(self.features_file + '.knn', 'r+b') as f_knn:
                try:
                    self.status.emit('Cargando net KNN...')
                    self.__knn = pickle.load(f_knn)
                    return True
                except EOFError:
                    return False
        return False

    def __orderIndices(self):
        distances, indices = self.__knn.predict(np.array([self.query_img.features]))
        distances = distances.flatten()
        indices = indices.flatten()
        indices, distances = find_topk_unique(indices, distances, self.n_neighbors)
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
        self.status.emit('Escaneando Imagen de muestra...')
        self.query_img.features = self.__getFeatures(self.query_img)
        self.img_list = klepto.archives.file_archive(
            self.features_file,
            serialized=True,
            cached=True,
            protocol=pickle.HIGHEST_PROTOCOL
        )
        self.img_list.archived(True)
        if not self.__loadKNN() or not isinstance(self.img_list.archive.get('0'), ImageCNN):
            self.__loadAllImages()
            self.img_list.archived(True)
        else:
            self.status.emit('Cargando Keys...')
            totalItems = len(self.img_list.archive.keys())
            self.n_neighbors = totalItems if totalItems < 50 else 50
        self.status.emit('Procesando Imagenes...')
        indices = self.__orderIndices()
        self.freeMem()
        resultMedia: list = []
        imgs = indices[0]
        count: int = 0
        total: int = len(imgs)
        self.progress.emit(count, total)
        for idx in imgs:
            img = self.img_list.archive.get(str(idx))
            count += 1
            self.status.emit('Reordenando Imagen %d de %d...' % (count, total))
            self.progress.emit(count, total)
            for media in self.VICMedia:
                if img.mediaItem['MediaID'] == media['MediaID']:
                    self.VICMedia.remove(media)
                    resultMedia.append(media)
                    break
        resultMedia.extend(self.VICMedia)
        self.status.emit('Proceso terminado en %s!' %
                         secondsToHMS(time() - self.tInicio))
        self.progress.emit(0, -1)
        self.finish.emit(resultMedia)
        del indices, resultMedia, self.img_list, self.VICMedia
        gc.collect()
