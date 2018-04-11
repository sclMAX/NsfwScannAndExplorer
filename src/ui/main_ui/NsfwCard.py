from pathlib import Path
import webbrowser
from PyQt5 import QtGui, QtWidgets, QtCore

class NsfwCard(QtWidgets.QFrame):
    data: dict
    base_path: str

    #Signals
    remove_me: QtCore.pyqtSignal = QtCore.pyqtSignal(object)

    def __init__(self, parent, media_item, width: int, height: int, base_path: str):
        super().__init__(parent)
        self.data = media_item
        self.base_path = base_path
        self.__setup(width, height)
        self.self_btnOpen.clicked.connect(self.btnOpen_click)
        self.self_btnRemove.clicked.connect(self.btnRemove_click)
        
    def getScore(self):
        comment: str = self.data.get('Comments')
        score: float = float(comment)
        return score or 0

    def getFilePath(self):
        file_path: str = self.data.get('RelativeFilePath')
        if file_path:
            media_base_path = Path(file_path).parent
            if Path(self.base_path) != media_base_path.parent:
                file_path = str(Path(self.base_path).joinpath(file_path))
            return file_path
        return 'Error RelativeFilePath'

    def __setup(self, w: int, h: int):
        self.resize(w, h)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMaximumSize(QtCore.QSize(w, h))
        self.setFrameShape(QtWidgets.QFrame.Box)
        self.setFrameShadow(QtWidgets.QFrame.Plain)
        self.setLineWidth(2)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalFrame = QtWidgets.QFrame(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.horizontalFrame.sizePolicy().hasHeightForWidth())
        self.horizontalFrame.setSizePolicy(sizePolicy)
        self.horizontalFrame.setObjectName("horizontalFrame")
        self.self_buttons = QtWidgets.QHBoxLayout(self.horizontalFrame)
        self.self_buttons.setContentsMargins(2, 2, 2, 2)
        self.self_buttons.setSpacing(2)
        self.self_buttons.setObjectName("self_buttons")
        self.self_btnOpen = QtWidgets.QToolButton(self.horizontalFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.self_btnOpen.sizePolicy().hasHeightForWidth())
        self.self_btnOpen.setSizePolicy(sizePolicy)
        self.self_btnOpen.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/icon-search.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.self_btnOpen.setIcon(icon)
        self.self_btnOpen.setIconSize(QtCore.QSize(16, 16))
        self.self_btnOpen.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.self_btnOpen.setArrowType(QtCore.Qt.NoArrow)
        self.self_btnOpen.setObjectName("self_btnOpen")
        self.self_buttons.addWidget(self.self_btnOpen)
        self.self_btnRemove = QtWidgets.QToolButton(self.horizontalFrame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.self_btnRemove.sizePolicy().hasHeightForWidth())
        self.self_btnRemove.setSizePolicy(sizePolicy)
        self.self_btnRemove.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/icon-circledelete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.self_btnRemove.setIcon(icon1)
        self.self_btnRemove.setIconSize(QtCore.QSize(16, 16))
        self.self_btnRemove.setObjectName("self_btnRemove")
        self.self_buttons.addWidget(self.self_btnRemove)
        self.verticalLayout.addWidget(self.horizontalFrame, 0, QtCore.Qt.AlignTop)
        self.self_image = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.self_image.sizePolicy().hasHeightForWidth())
        self.self_image.setSizePolicy(sizePolicy)
        self.self_image.setText("")
        file_path = self.getFilePath()
        if file_path != 'Error RelativeFilePath':
            self.self_image.setPixmap(QtGui.QPixmap(file_path))
        else:
            self.self_image.setPixmap(QtGui.QPixmap('icons/noimage.gif'))
        self.self_image.setScaledContents(True)
        self.self_image.setToolTip(file_path)
        self.self_image.setAlignment(QtCore.Qt.AlignCenter)
        self.self_image.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.verticalLayout.addWidget(self.self_image)
        self.self_score = QtWidgets.QProgressBar(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.self_score.sizePolicy().hasHeightForWidth())
        self.self_score.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(5)
        font.setBold(True)
        font.setWeight(75)
        self.self_score.setFont(font)
        self.self_score.setValue(self.getScore() * 100)
        self.self_score.setAlignment(QtCore.Qt.AlignCenter)
        self.self_score.setTextVisible(True)
        self.self_score.setObjectName("self_score")
        self.verticalLayout.addWidget(self.self_score, 0, QtCore.Qt.AlignBottom)

    def btnOpen_click(self):
        webbrowser.open_new_tab(self.getFilePath())

    def btnRemove_click(self):
        self.remove_me.emit(self)
