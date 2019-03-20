# -*- coding: utf-8 -*-
import webbrowser
from pathlib import Path
from PyQt5 import QtWidgets, QtCore, QtGui
from src.ui import resources_rc


class NsfwLogItem(QtWidgets.QFrame):
    __image: QtWidgets.QLabel
    __btnImage: QtWidgets.QToolButton
    __image_score: QtWidgets.QProgressBar

    def __init__(self, parent):
        super().__init__(parent)
        self.__setup()

    def __btnImage_click(self):
        if self.__image.toolTip():
            webbrowser.open_new_tab(str(Path(self.__image.toolTip())))

    def setFile(self, file: str):
        self.__image.setToolTip(file)
        self.__image.setPixmap(QtGui.QPixmap(file))
        self.__image.repaint()

    def setScore(self, score: int):
        self.__image_score.setValue(score)

    def setAll(self, file: str, score: int):
        self.setScore(score)
        self.setFile(file)

    def __setup(self):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QtCore.QSize(0, 0))
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.__verticalLayout_1 = QtWidgets.QVBoxLayout(self)
        self.__verticalLayout_1.setContentsMargins(0, 0, 0, 0)
        self.__verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.__verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.__image = QtWidgets.QLabel(self)
        self.__image.setMinimumSize(QtCore.QSize(200, 200))
        self.__image.setMaximumSize(QtCore.QSize(200, 200))
        self.__image.setBaseSize(QtCore.QSize(200, 200))
        self.__image.setText("")
        self.__image.setScaledContents(True)
        self.__verticalLayout_2.addWidget(self.__image, 0, QtCore.Qt.AlignTop)
        self.__horizontalLayout_1 = QtWidgets.QHBoxLayout()
        self.__horizontalLayout_1.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.__image_score = QtWidgets.QProgressBar(self)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.__image_score.setFont(font)
        self.__image_score.setProperty("value", 0)
        self.__image_score.setAlignment(QtCore.Qt.AlignCenter)
        self.__horizontalLayout_1.addWidget(self.__image_score, 0, QtCore.Qt.AlignTop)
        self.__btnImage = QtWidgets.QToolButton(self)
        self.__btnImage.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":iconos/view_image"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.__btnImage.setIcon(icon6)
        self.__btnImage.clicked.connect(self.__btnImage_click)
        self.__horizontalLayout_1.addWidget(self.__btnImage, 0, QtCore.Qt.AlignRight|QtCore.Qt.AlignTop)
        self.__verticalLayout_2.addLayout(self.__horizontalLayout_1)
        self.__verticalLayout_1.addLayout(self.__verticalLayout_2)
      