from PyQt5 import QtGui, QtWidgets, QtCore

class NsfwCard(QtWidgets.QFrame):
    __media_item: dict
    #Visual Objects
    __image: QtWidgets.QLabel
    __image_score: QtWidgets.QProgressBar
    __vl1: QtWidgets.QVBoxLayout
    __vl2: QtWidgets.QVBoxLayout
    __hl1: QtWidgets.QHBoxLayout
    __btnOpen: QtWidgets.QToolButton


    def __init__(self, parent, media_item: dict):
        super().__init__(parent)
        self.__setup(100, 100)
        self.setMediaItem(media_item)

    def __setup(self, w: int, h: int):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(0, 0))
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.__vl1 = QtWidgets.QVBoxLayout(self)
        self.__vl1.setContentsMargins(0, 0, 0, 0)
        self.__vl2 = QtWidgets.QVBoxLayout()
        self.__vl2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.__image = QtWidgets.QLabel(self)
        self.__image.setMinimumSize(QtCore.QSize(w, h))
        self.__image.setMaximumSize(QtCore.QSize(w, h))
        self.__image.setBaseSize(QtCore.QSize(w, h))
        self.__image.setText("")
        self.__image.setScaledContents(True)
        self.__vl2.addWidget(self.__image, 0, QtCore.Qt.AlignTop)
        self.__hl1 = QtWidgets.QHBoxLayout()
        self.__hl1.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.__image_score = QtWidgets.QProgressBar(self)
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(False)
        font.setWeight(50)
        self.__image_score.setFont(font)
        self.__image_score.setProperty("value", 0)
        self.__image_score.setAlignment(QtCore.Qt.AlignCenter)
        self.__hl1.addWidget(self.__image_score, 0, QtCore.Qt.AlignTop)
        self.__btnOpen = QtWidgets.QToolButton(self)
        self.__btnOpen.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icons/icon-tectile.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.__btnOpen.setIconSize(QtCore.QSize(10, 10))
        self.__btnOpen.setIcon(icon6)
        self.__hl1.addWidget(self.__btnOpen, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.__vl2.addLayout(self.__hl1)
        self.__vl1.addLayout(self.__vl2)

    def setMediaItem(self, media_item: dict):
        self.__media_item = media_item
        file_path: str = self.__media_item.get('RelativeFilePath')
        score: float = float(self.__media_item.get('Comments'))
        if score > -1:
            self.__image.setPixmap(QtGui.QPixmap(file_path))
            self.__image_score.setValue(round(score * 100))
