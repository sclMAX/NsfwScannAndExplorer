# -*- coding: utf-8 -*-
from pathlib import Path
import webbrowser
import cv2 as cv
from PyQt5 import QtGui, QtWidgets, QtCore
from src.ui import resources_rc
from src.ui.vic_edit_ui.UiVic_Edit import DlgVicEdit


class NsfwCard(QtWidgets.QFrame):
    data: dict
    base_path: str

    # Signals
    remove_me: QtCore.pyqtSignal = QtCore.pyqtSignal(object)
    update_me: QtCore.pyqtSignal = QtCore.pyqtSignal()

    # Gif and Video
    isAnimated: bool = False
    cap = None
    frames: int = 0
    currentFrame: int = 0
    frameIncremento: int = 1
    nextFrame: int = 1
    __timer: QtCore.QTimer = QtCore.QTimer()

    def __init__(self, parent, media_item, width: int, height: int, base_path: str, isAnimated: bool):
        super().__init__(parent)
        self.data = media_item
        self.dlgEdit: DlgVicEdit = None
        self.base_path = base_path
        self.isAnimated = isAnimated
        self.__setup(width, height)
        self.self_btnOpen.clicked.connect(self.btnOpen_click)
        self.self_btnEdit.clicked.connect(self.btnEdit_click)
        self.self_btnRemove.clicked.connect(self.btnRemove_click)

    def getScore(self):
        comment: str = self.data.get('Comments')
        score: float = float(comment)
        return score

    def getFilePath(self):
        file_path: str = self.data.get('RelativeFilePath')
        if file_path:
            file_path = file_path.replace('\\', '/')
            media_base_path = Path(file_path).parent
            if Path(self.base_path) != media_base_path.parent:
                file_path = str(Path(self.base_path).joinpath(file_path))
            return file_path
        return ''

    def getToolTip(self):
        media = self.data.get('MediaFiles')
        if media:
            file_path = media[0].get('FilePath')
            file_name = media[0].get('FileName')
            return 'RelativeFilePath: %s \nFilePath: %s \nFileName: %s' % (self.getFilePath(), file_path, file_name)
        return self.getFilePath()

    def getCategory(self):
        category = self.data.get('Category')
        return category

    def getImage(self):
        file_path = self.getFilePath()
        if file_path:
            if not self.isAnimated:
                return QtGui.QPixmap(file_path)
            file_type = self.data.get('FileType')
            file_Extension = self.data.get('FileExtension')
            if file_type and 'video' in file_type:
                return self.__processVideo(file_path)
            if file_Extension and 'gif' in file_Extension:
                return self.__processGif(file_path)
            return QtGui.QPixmap(file_path)
        return QtGui.QPixmap(':iconos/noimage')

    def __processGif(self, file: str):
        import imageio
        try:
            n = imageio.mimread(file)
            self.frames = len(n)
        except:
            return QtGui.QPixmap(file)
        self.frameIncremento = 1
        self.nextFrame = 2
        self.cap = cv.VideoCapture(file)
        self.__timer.setInterval(500)
        self.__timer.timeout.connect(self.__play)
        self.__timer.start()
        return QtGui.QPixmap(file)

    def __processVideo(self, file: str):
        self.cap = cv.VideoCapture(file)
        self.frames = abs(self.cap.get(cv.CAP_PROP_FRAME_COUNT))
        self.frameIncremento = abs(self.cap.get(cv.CAP_PROP_FPS))
        self.__timer.setInterval(100)
        self.__timer.timeout.connect(self.__play)
        self.__timer.start()
        return QtGui.QPixmap(':iconos/noimage')

    def __play(self):
        if self.cap and self.cap.isOpened:
            self.nextFrame += self.frameIncremento
            if self.nextFrame >= self.frames:
                self.nextFrame = self.frameIncremento
            self.cap.set(1, self.nextFrame - 1)
            ok, frame = self.cap.read()
            if ok:
                frame = cv.resize(frame, (200, 200))
                height, width, _ = frame.shape
                bytesPerLine = 3 * width
                cv.cvtColor(frame, cv.COLOR_BGR2RGB, frame)
                img = QtGui.QImage(frame.data, width, height,
                                   bytesPerLine, QtGui.QImage.Format_RGB888)
                self.self_image.setPixmap(QtGui.QPixmap(img))
                self.self_image.repaint()
            else:
                self.cap.release()
                self.cap = cv.VideoCapture(self.getFilePath())

    def __setup(self, w: int, h: int):
        self.resize(w, h)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMaximumSize(QtCore.QSize(w, h))
        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setLineWidth(2)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setSizeConstraint(
            QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(2)
        self.horizontalFrame = QtWidgets.QFrame(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.horizontalFrame.sizePolicy().hasHeightForWidth())
        self.horizontalFrame.setSizePolicy(sizePolicy)
        self.self_buttons = QtWidgets.QHBoxLayout(self.horizontalFrame)
        self.self_buttons.setContentsMargins(2, 2, 2, 2)
        self.self_buttons.setSpacing(2)
        # btnOpen
        self.self_btnOpen = QtWidgets.QToolButton(self.horizontalFrame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.self_btnOpen.sizePolicy().hasHeightForWidth())
        self.self_btnOpen.setSizePolicy(sizePolicy)
        self.self_btnOpen.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":iconos/view_image"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.self_btnOpen.setIcon(icon)
        self.self_btnOpen.setIconSize(QtCore.QSize(16, 16))
        self.self_btnOpen.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.self_btnOpen.setArrowType(QtCore.Qt.NoArrow)
        self.self_btnOpen.setToolTip('Abrir imagen.')
        self.self_buttons.addWidget(self.self_btnOpen)
        #/btnOpen
        # btnEdit
        self.self_btnEdit = QtWidgets.QToolButton(self.horizontalFrame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.self_btnEdit.sizePolicy().hasHeightForWidth())
        self.self_btnEdit.setSizePolicy(sizePolicy)
        self.self_btnEdit.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":iconos/edit"),
                       QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.self_btnEdit.setIcon(icon)
        self.self_btnEdit.setIconSize(QtCore.QSize(16, 16))
        self.self_btnEdit.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.self_btnEdit.setArrowType(QtCore.Qt.NoArrow)
        self.self_btnEdit.setToolTip('Editar VIC Media Item.')
        self.self_buttons.addWidget(self.self_btnEdit)
        #/btnEdit
        self.self_btnRemove = QtWidgets.QToolButton(self.horizontalFrame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.self_btnRemove.sizePolicy().hasHeightForWidth())
        self.self_btnRemove.setSizePolicy(sizePolicy)
        self.self_btnRemove.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":iconos/delete"),
                        QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.self_btnRemove.setIcon(icon1)
        self.self_btnRemove.setIconSize(QtCore.QSize(16, 16))
        self.self_btnRemove.setToolTip('Quitar del reporte.')
        self.self_buttons.addWidget(self.self_btnRemove)
        # Category
        category = self.getCategory()
        if category != None:
            self.createCat(category)
        #/Category
        self.verticalLayout.addWidget(
            self.horizontalFrame, 0, QtCore.Qt.AlignTop)
        self.self_image = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.self_image.sizePolicy().hasHeightForWidth())
        self.self_image.setSizePolicy(sizePolicy)
        self.self_image.setText("")
        self.self_image.setPixmap(self.getImage())
        self.self_image.setScaledContents(True)
        self.self_image.setToolTip(self.getToolTip())
        self.self_image.setAlignment(QtCore.Qt.AlignCenter)
        self.self_image.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.verticalLayout.addWidget(self.self_image)
        self.self_score = QtWidgets.QProgressBar(self)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.self_score.sizePolicy().hasHeightForWidth())
        self.self_score.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(5)
        font.setBold(True)
        font.setWeight(75)
        self.self_score.setFont(font)
        try:
            score = self.getScore()
            self.self_score.setValue(score * 100)
        except ValueError:
            self.self_score.setVisible(False)
        self.self_score.setAlignment(QtCore.Qt.AlignCenter)
        self.self_score.setTextVisible(True)
        self.verticalLayout.addWidget(
            self.self_score, 0, QtCore.Qt.AlignBottom)

    def btnOpen_click(self):
        webbrowser.open_new_tab(self.getFilePath())

    def createCat(self, category):
        self.self_cat = QtWidgets.QLabel(self.horizontalFrame)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.self_cat.sizePolicy().hasHeightForWidth())
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.self_cat.setSizePolicy(sizePolicy)
        self.self_cat.setFont(font)
        self.self_cat.setStyleSheet('color: blue; background: gray')
        self.self_cat.setText(category)
        self.self_cat.setScaledContents(True)
        self.self_cat.setAlignment(QtCore.Qt.AlignCenter)
        self.self_buttons.addWidget(self.self_cat)

    def btnEdit_click(self):
        self.dlgEdit = DlgVicEdit(self, self.data)
        if self.dlgEdit.exec_():
            self.data = self.dlgEdit.media_item
            self.update_me.emit()
            category = self.getCategory()
            if category != None:
                try:
                    self.self_cat.setText(category)
                except AttributeError:
                    self.createCat(category)

    def btnRemove_click(self):
        self.remove_me.emit(self)
