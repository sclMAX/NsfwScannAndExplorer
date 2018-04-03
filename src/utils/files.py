from PyQt5 import QtCore
from imghdr import what
from pathlib import Path
from src.utils.message import Message, NORMAL, DANGER, WARNING
from src.utils.formats import secondsToHMS
from src.Nsfw.vic13 import genNewMediaItem, updateMediaItem
from time import time


def searching_all_files(path: Path):
    dirpath = Path(path)
    assert(dirpath.is_dir())
    file_list = []
    for x in dirpath.iterdir():
        if x.is_file():
            file_list.append(x)
        elif x.is_dir():
            file_list.extend(searching_all_files(str(x)))
    return file_list


class ImagesFinder(QtCore.QThread):
    findPath: str = ''
    isRun: bool = False
    # Signals
    finish: QtCore.pyqtSignal = QtCore.pyqtSignal(list)
    status: QtCore.pyqtSignal = QtCore.pyqtSignal(Message)
    statusBar: QtCore.pyqtSignal = QtCore.pyqtSignal(str)
    progressMax: QtCore.pyqtSignal = QtCore.pyqtSignal(int)
    progress: QtCore.pyqtSignal = QtCore.pyqtSignal(int)
    # Process Vars
    tInico: int = time()
    totalFiles: int = 0
    totalImages: int = 0

    def __init__(self, parent: object, findPath: str):
        super().__init__(parent)
        self.findPath = findPath

    def find(self):
        self.tInico = time()
        self.isRun = True
        self.start()

    def stop(self,):
        self.isRun = False
        self.status.emit(Message('Proceso cancelado!', False, DANGER, True))
        self.exit()

    def emitStatusBar(self):
        et: int = time() - self.tInico
        fs: float = self.totalFiles / et
        txt: str = 'I: %d de A: %d | T: %s @ %.2f A/Seg' % (
            self.totalImages, self.totalFiles, secondsToHMS(et), fs)
        self.statusBar.emit(txt)

    def __findImages(self, path: str):
        dirpath = Path(path)
        assert(dirpath.is_dir())
        file_list = []
        for x in dirpath.iterdir():
            if(not self.isRun):
                break
            if x.is_file():
                try:
                    self.totalFiles += 1
                    fileType = what(x)
                    if(not fileType):
                        continue
                    self.totalImages += 1
                    file_list.append(
                        {'file': str(x), 'type': fileType})
                finally:
                    txt: str = 'Encontradas %d Imagenes  de %d Archivos encontrados! Buscando...' % (
                        self.totalImages, self.totalFiles)
                    self.status.emit(Message(txt, False, NORMAL, False))
                    self.emitStatusBar()
            elif x.is_dir():
                file_list.extend(self.__findImages(str(x)))
        return file_list

    def run(self):
        self.status.emit(Message('Buscando Imagenes...'))
        # Buscar imagen en directorio y subdirectorios
        fileList: list = self.__findImages(self.findPath)
        if(len(fileList)):
            # Crear media con las imagen encontradas
            media: list = []
            count: int = 0
            self.progressMax.emit(len(fileList))
            self.status.emit(Message('Creando Media...', True))
            for f in fileList:
                if(not self.isRun):
                    break
                mediaItem = genNewMediaItem()
                updateMediaItem(mediaItem, {
                    'MediaID': count,
                    'RelativeFilePath': str(f['file']),
                    'ImageType': str(f['type'])
                })
                media.append(mediaItem)
                count += 1
                self.progress.emit(count)
            self.finish.emit(media)
        else:
            self.status.emit(Message(
                'No se encontraron Imagenes en el Directorio seleccionado!', False, WARNING))
            self.finish.emit(None)