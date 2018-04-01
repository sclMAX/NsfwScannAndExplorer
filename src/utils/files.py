from PyQt5 import QtCore
from imghdr import what
from pathlib import Path
from src.utils.message import Message, NORMAL


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


class FilesFinder(QtCore.QThread):
    id: int = 0
    findPath: str = ''
    fileList: list = []
    dirList: list = []
    isRun:bool = False
    # Signals
    finish = QtCore.pyqtSignal(QtCore.QThread,int, list, list)  # id, fileList, dirList
    status = QtCore.pyqtSignal(int, int)  # images , files

    def __init__(self, parent: object, id: int, findPath: str):
        super().__init__(parent)
        self.id = id
        self.findPath = findPath

    def find(self):
        self.start()

    def run(self):
        print('RUNNN ID:',self.id)
        self.isRun = True
        dirpath = Path(self.findPath)
        assert(dirpath.is_dir())
        files: int = 0
        images: int = 0
        for x in dirpath.iterdir():
            if x.is_file():
                files += 1
                fileType = what(x)
                self.status.emit(images, files)
                if(not fileType):
                    continue
                images += 1
                self.fileList.append({'file': x, 'type': fileType})
            elif x.is_dir():
                self.dirList.append(str(x))
        if(self.isRun):
            self.isRun = False
            self.finish.emit(self,self.id, self.fileList, self.dirList)

        


class ImagesFinder(QtCore.QObject):

    parent: object = None
    fileList: list = []
    # Threads Vars
    maxThreads: int = QtCore.QThread.idealThreadCount()
    threads: list = []
    countThreads: int = 0
    pathStack: list = []
    totalFiles: int = 0
    totalImages: int = 0
    mutex = QtCore.QMutex()

    # Signals
    status = QtCore.pyqtSignal(Message)
    finish = QtCore.pyqtSignal(list)

    def __init__(self, parent: None):
        super().__init__(parent)
        self.parent = parent

    def find(self, path: str):
        self.createThread(path)
        
    def createThread(self, path:str):
        self.countThreads += 1
        print('CREADO ID:', self.countThreads,' DE ',self.countThreads)
        self.threads.append(self.countThreads)
        self.filesFinder = FilesFinder(self, self.countThreads, path)
        self.filesFinder.finish.connect(self.threadFinish)
        self.filesFinder.status.connect(self.threadStatus)
        self.filesFinder.find()

    def threadStatus(self, images: int, files: int):
        self.totalFiles += files
        self.totalImages += images
        msg = Message('%d Imagenes de %d Archivos Encontrados...'%(self.totalImages,self.totalFiles),
                      False, NORMAL, False)
        self.status.emit(msg)

    def threadFinish(self,th:QtCore.QThread, id: int, fileList: list, dirList: list):
        try:
            self.mutex.lock()
            #TODO implementar uso de multiplet Threads      
            
        finally:
            self.mutex.unlock()
