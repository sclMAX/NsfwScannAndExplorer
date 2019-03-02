# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/ui/main_ui/ui_main.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from src.ui import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1071, 734)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/iconos/mainIcon"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnScanner = QtWidgets.QToolButton(self.groupBox)
        self.btnScanner.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/iconos/scann"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnScanner.setIcon(icon1)
        self.btnScanner.setIconSize(QtCore.QSize(48, 48))
        self.btnScanner.setObjectName("btnScanner")
        self.horizontalLayout.addWidget(self.btnScanner)
        self.btnOpen = QtWidgets.QToolButton(self.groupBox)
        self.btnOpen.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/iconos/open"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnOpen.setIcon(icon2)
        self.btnOpen.setIconSize(QtCore.QSize(48, 48))
        self.btnOpen.setObjectName("btnOpen")
        self.horizontalLayout.addWidget(self.btnOpen)
        self.btnSave = QtWidgets.QToolButton(self.groupBox)
        self.btnSave.setEnabled(False)
        self.btnSave.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/iconos/save"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSave.setIcon(icon3)
        self.btnSave.setIconSize(QtCore.QSize(48, 48))
        self.btnSave.setObjectName("btnSave")
        self.horizontalLayout.addWidget(self.btnSave)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnAnimated = QtWidgets.QToolButton(self.groupBox)
        self.btnAnimated.setEnabled(True)
        self.btnAnimated.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/iconos/video"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAnimated.setIcon(icon4)
        self.btnAnimated.setIconSize(QtCore.QSize(48, 48))
        self.btnAnimated.setCheckable(True)
        self.btnAnimated.setChecked(False)
        self.btnAnimated.setObjectName("btnAnimated")
        self.horizontalLayout.addWidget(self.btnAnimated)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.btnDeleteAll = QtWidgets.QToolButton(self.groupBox)
        self.btnDeleteAll.setEnabled(False)
        self.btnDeleteAll.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/iconos/delete"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnDeleteAll.setIcon(icon5)
        self.btnDeleteAll.setIconSize(QtCore.QSize(48, 48))
        self.btnDeleteAll.setArrowType(QtCore.Qt.NoArrow)
        self.btnDeleteAll.setObjectName("btnDeleteAll")
        self.horizontalLayout.addWidget(self.btnDeleteAll)
        self.btnUndo = QtWidgets.QToolButton(self.groupBox)
        self.btnUndo.setEnabled(False)
        self.btnUndo.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/iconos/undo"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnUndo.setIcon(icon6)
        self.btnUndo.setIconSize(QtCore.QSize(48, 48))
        self.btnUndo.setArrowType(QtCore.Qt.NoArrow)
        self.btnUndo.setObjectName("btnUndo")
        self.horizontalLayout.addWidget(self.btnUndo)
        self.lblSelCount = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lblSelCount.setFont(font)
        self.lblSelCount.setObjectName("lblSelCount")
        self.horizontalLayout.addWidget(self.lblSelCount)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.lblStatus = QtWidgets.QLabel(self.centralwidget)
        self.lblStatus.setText("")
        self.lblStatus.setObjectName("lblStatus")
        self.verticalLayout_4.addWidget(self.lblStatus)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.gbBuscarImagen = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gbBuscarImagen.sizePolicy().hasHeightForWidth())
        self.gbBuscarImagen.setSizePolicy(sizePolicy)
        self.gbBuscarImagen.setMinimumSize(QtCore.QSize(100, 0))
        self.gbBuscarImagen.setMaximumSize(QtCore.QSize(148, 15777215))
        self.gbBuscarImagen.setAutoFillBackground(True)
        self.gbBuscarImagen.setAlignment(QtCore.Qt.AlignCenter)
        self.gbBuscarImagen.setFlat(False)
        self.gbBuscarImagen.setObjectName("gbBuscarImagen")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.gbBuscarImagen)
        self.verticalLayout_7.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.verticalLayout_7.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.lblImageToFind = QtWidgets.QLabel(self.gbBuscarImagen)
        self.lblImageToFind.setMinimumSize(QtCore.QSize(120, 120))
        self.lblImageToFind.setMaximumSize(QtCore.QSize(120, 120))
        self.lblImageToFind.setText("")
        self.lblImageToFind.setScaledContents(True)
        self.lblImageToFind.setObjectName("lblImageToFind")
        self.verticalLayout_6.addWidget(self.lblImageToFind)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.btnOpenImage = QtWidgets.QToolButton(self.gbBuscarImagen)
        self.btnOpenImage.setText("")
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(":/iconos/open_image"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnOpenImage.setIcon(icon7)
        self.btnOpenImage.setIconSize(QtCore.QSize(48, 48))
        self.btnOpenImage.setObjectName("btnOpenImage")
        self.horizontalLayout_4.addWidget(self.btnOpenImage)
        self.btnSortVIC = QtWidgets.QToolButton(self.gbBuscarImagen)
        self.btnSortVIC.setEnabled(False)
        self.btnSortVIC.setText("")
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(":/iconos/scann_image"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSortVIC.setIcon(icon8)
        self.btnSortVIC.setIconSize(QtCore.QSize(48, 48))
        self.btnSortVIC.setObjectName("btnSortVIC")
        self.horizontalLayout_4.addWidget(self.btnSortVIC)
        self.verticalLayout_6.addLayout(self.horizontalLayout_4)
        self.verticalLayout_7.addLayout(self.verticalLayout_6)
        self.gbxBackend = QtWidgets.QGroupBox(self.gbBuscarImagen)
        self.gbxBackend.setObjectName("gbxBackend")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.gbxBackend)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.chkCaffe = QtWidgets.QRadioButton(self.gbxBackend)
        self.chkCaffe.setChecked(True)
        self.chkCaffe.setObjectName("chkCaffe")
        self.verticalLayout_8.addWidget(self.chkCaffe)
        self.chkTensorflow = QtWidgets.QRadioButton(self.gbxBackend)
        self.chkTensorflow.setObjectName("chkTensorflow")
        self.verticalLayout_8.addWidget(self.chkTensorflow)
        self.verticalLayout_9.addLayout(self.verticalLayout_8)
        self.verticalLayout_7.addWidget(self.gbxBackend)
        self.groupBox_2 = QtWidgets.QGroupBox(self.gbBuscarImagen)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.spxNeighbors = QtWidgets.QSpinBox(self.groupBox_2)
        self.spxNeighbors.setMinimum(2)
        self.spxNeighbors.setMaximum(100)
        self.spxNeighbors.setProperty("value", 50)
        self.spxNeighbors.setObjectName("spxNeighbors")
        self.verticalLayout_11.addWidget(self.spxNeighbors)
        self.verticalLayout_7.addWidget(self.groupBox_2)
        self.horizontalLayout_3.addWidget(self.gbBuscarImagen, 0, QtCore.Qt.AlignTop)
        self.listView = QtWidgets.QScrollArea(self.centralwidget)
        self.listView.setAutoFillBackground(True)
        self.listView.setWidgetResizable(True)
        self.listView.setObjectName("listView")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 841, 523))
        self.scrollAreaWidgetContents.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.cards = QtWidgets.QGridLayout()
        self.cards.setSpacing(5)
        self.cards.setObjectName("cards")
        self.verticalLayout_5.addLayout(self.cards)
        self.listView.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout_3.addWidget(self.listView)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnListUp = QtWidgets.QToolButton(self.frame)
        self.btnListUp.setEnabled(False)
        self.btnListUp.setText("")
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(":/iconos/btn_up"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnListUp.setIcon(icon9)
        self.btnListUp.setIconSize(QtCore.QSize(48, 48))
        self.btnListUp.setObjectName("btnListUp")
        self.verticalLayout.addWidget(self.btnListUp, 0, QtCore.Qt.AlignHCenter)
        self.lblPages = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.lblPages.setFont(font)
        self.lblPages.setAlignment(QtCore.Qt.AlignCenter)
        self.lblPages.setObjectName("lblPages")
        self.verticalLayout.addWidget(self.lblPages)
        self.btnListDown = QtWidgets.QToolButton(self.frame)
        self.btnListDown.setEnabled(True)
        self.btnListDown.setText("")
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(":/iconos/btn_down"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnListDown.setIcon(icon10)
        self.btnListDown.setIconSize(QtCore.QSize(48, 48))
        self.btnListDown.setArrowType(QtCore.Qt.NoArrow)
        self.btnListDown.setObjectName("btnListDown")
        self.verticalLayout.addWidget(self.btnListDown, 0, QtCore.Qt.AlignHCenter)
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setText("")
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.btnFiltro = QtWidgets.QToolButton(self.frame)
        self.btnFiltro.setEnabled(True)
        self.btnFiltro.setText("")
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(":/iconos/filter"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnFiltro.setIcon(icon11)
        self.btnFiltro.setIconSize(QtCore.QSize(48, 48))
        self.btnFiltro.setCheckable(True)
        self.btnFiltro.setChecked(False)
        self.btnFiltro.setObjectName("btnFiltro")
        self.verticalLayout.addWidget(self.btnFiltro)
        self.lblFiltro = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblFiltro.sizePolicy().hasHeightForWidth())
        self.lblFiltro.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.lblFiltro.setFont(font)
        self.lblFiltro.setAlignment(QtCore.Qt.AlignCenter)
        self.lblFiltro.setObjectName("lblFiltro")
        self.verticalLayout.addWidget(self.lblFiltro)
        self.btnFiltro_Invertir = QtWidgets.QToolButton(self.frame)
        self.btnFiltro_Invertir.setEnabled(True)
        self.btnFiltro_Invertir.setText("")
        icon12 = QtGui.QIcon()
        icon12.addPixmap(QtGui.QPixmap(":/iconos/invertFilter"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnFiltro_Invertir.setIcon(icon12)
        self.btnFiltro_Invertir.setIconSize(QtCore.QSize(48, 48))
        self.btnFiltro_Invertir.setCheckable(True)
        self.btnFiltro_Invertir.setChecked(False)
        self.btnFiltro_Invertir.setObjectName("btnFiltro_Invertir")
        self.verticalLayout.addWidget(self.btnFiltro_Invertir)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.slrFiltro = QtWidgets.QSlider(self.frame)
        self.slrFiltro.setMaximum(100)
        self.slrFiltro.setSingleStep(1)
        self.slrFiltro.setProperty("value", 15)
        self.slrFiltro.setOrientation(QtCore.Qt.Vertical)
        self.slrFiltro.setObjectName("slrFiltro")
        self.horizontalLayout_2.addWidget(self.slrFiltro)
        self.pgbFiltro = QtWidgets.QProgressBar(self.frame)
        self.pgbFiltro.setProperty("value", 15)
        self.pgbFiltro.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignTop)
        self.pgbFiltro.setOrientation(QtCore.Qt.Vertical)
        self.pgbFiltro.setObjectName("pgbFiltro")
        self.horizontalLayout_2.addWidget(self.pgbFiltro)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addWidget(self.frame)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.lblProgress = QtWidgets.QLabel(self.centralwidget)
        self.lblProgress.setText("")
        self.lblProgress.setWordWrap(True)
        self.lblProgress.setObjectName("lblProgress")
        self.verticalLayout_10.addWidget(self.lblProgress)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_10.addWidget(self.progressBar)
        self.horizontalLayout_5.addLayout(self.verticalLayout_10)
        self.btnStop = QtWidgets.QToolButton(self.centralwidget)
        self.btnStop.setText("")
        icon13 = QtGui.QIcon()
        icon13.addPixmap(QtGui.QPixmap(":/iconos/pause"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnStop.setIcon(icon13)
        self.btnStop.setIconSize(QtCore.QSize(48, 48))
        self.btnStop.setObjectName("btnStop")
        self.horizontalLayout_5.addWidget(self.btnStop)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "VIC Report Explorer v1.0 by MAX"))
        self.btnScanner.setToolTip(_translate("MainWindow", "Abrir Scanner."))
        self.btnScanner.setAccessibleName(_translate("MainWindow", "Escanear Directorio."))
        self.btnOpen.setToolTip(_translate("MainWindow", "Abrir Reporte."))
        self.btnSave.setToolTip(_translate("MainWindow", "Guardar reporte."))
        self.btnAnimated.setToolTip(_translate("MainWindow", "Activar/Desactivar animaciones."))
        self.btnDeleteAll.setToolTip(_translate("MainWindow", "Borrar todas de la pagina actual."))
        self.btnUndo.setToolTip(_translate("MainWindow", "Deshacer."))
        self.lblSelCount.setText(_translate("MainWindow", "0/0"))
        self.gbBuscarImagen.setTitle(_translate("MainWindow", "Buscar Imagen "))
        self.btnOpenImage.setToolTip(_translate("MainWindow", "Abrir Imagen a Buscar."))
        self.btnSortVIC.setToolTip(_translate("MainWindow", "<html><head/><body><p>Iniciar Busqueda.</p></body></html>"))
        self.gbxBackend.setStatusTip(_translate("MainWindow", "Motor a usar en la Red Neuronal"))
        self.gbxBackend.setTitle(_translate("MainWindow", "Backend"))
        self.chkCaffe.setText(_translate("MainWindow", "Caffe"))
        self.chkTensorflow.setText(_translate("MainWindow", "TensorFlow"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Ordenar primeras"))
        self.btnListUp.setToolTip(_translate("MainWindow", "Pagina Anterior."))
        self.lblPages.setText(_translate("MainWindow", "1/1"))
        self.btnListDown.setToolTip(_translate("MainWindow", "Pagina Siguiente."))
        self.btnFiltro.setToolTip(_translate("MainWindow", "Aplicar / Quitar Filtro."))
        self.lblFiltro.setText(_translate("MainWindow", ">15%"))
        self.btnFiltro_Invertir.setToolTip(_translate("MainWindow", "Invertir filtro."))
        self.slrFiltro.setToolTip(_translate("MainWindow", "<html><head/><body><p>Especificar Filtro por Probabilidad.</p></body></html>"))
        self.btnStop.setToolTip(_translate("MainWindow", "Parar Proceso"))
        self.btnStop.setAccessibleName(_translate("MainWindow", "Escanear Directorio."))
