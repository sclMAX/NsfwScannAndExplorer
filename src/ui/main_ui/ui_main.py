# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_ui/ui_main.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1071, 734)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/icon-searchfolder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
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
        icon1.addPixmap(QtGui.QPixmap("icons/icon-wifi.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnScanner.setIcon(icon1)
        self.btnScanner.setIconSize(QtCore.QSize(48, 48))
        self.btnScanner.setObjectName("btnScanner")
        self.horizontalLayout.addWidget(self.btnScanner)
        self.btnOpen = QtWidgets.QToolButton(self.groupBox)
        self.btnOpen.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/icon-folder-open.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnOpen.setIcon(icon2)
        self.btnOpen.setIconSize(QtCore.QSize(48, 48))
        self.btnOpen.setObjectName("btnOpen")
        self.horizontalLayout.addWidget(self.btnOpen)
        self.btnClose = QtWidgets.QToolButton(self.groupBox)
        self.btnClose.setEnabled(False)
        self.btnClose.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/icon-deletefolderalt.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnClose.setIcon(icon3)
        self.btnClose.setIconSize(QtCore.QSize(48, 48))
        self.btnClose.setObjectName("btnClose")
        self.horizontalLayout.addWidget(self.btnClose)
        self.btnSave = QtWidgets.QToolButton(self.groupBox)
        self.btnSave.setEnabled(False)
        self.btnSave.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/icon-save-floppy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSave.setIcon(icon4)
        self.btnSave.setIconSize(QtCore.QSize(48, 48))
        self.btnSave.setObjectName("btnSave")
        self.horizontalLayout.addWidget(self.btnSave)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
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
        self.listView = QtWidgets.QScrollArea(self.centralwidget)
        self.listView.setAutoFillBackground(True)
        self.listView.setWidgetResizable(True)
        self.listView.setObjectName("listView")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 986, 531))
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
        self.btnListUp.setIconSize(QtCore.QSize(48, 48))
        self.btnListUp.setArrowType(QtCore.Qt.UpArrow)
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
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/icon-th.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnListDown.setIcon(icon5)
        self.btnListDown.setIconSize(QtCore.QSize(48, 48))
        self.btnListDown.setArrowType(QtCore.Qt.DownArrow)
        self.btnListDown.setObjectName("btnListDown")
        self.verticalLayout.addWidget(self.btnListDown, 0, QtCore.Qt.AlignHCenter)
        self.btnFiltro = QtWidgets.QToolButton(self.frame)
        self.btnFiltro.setEnabled(True)
        self.btnFiltro.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icons/icon-antenna.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnFiltro.setIcon(icon6)
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
        self.lblProgress = QtWidgets.QLabel(self.centralwidget)
        self.lblProgress.setText("")
        self.lblProgress.setWordWrap(True)
        self.lblProgress.setObjectName("lblProgress")
        self.verticalLayout_2.addWidget(self.lblProgress)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_2.addWidget(self.progressBar)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setMouseTracking(False)
        self.statusbar.setToolTip("")
        self.statusbar.setToolTipDuration(0)
        self.statusbar.setStatusTip("")
        self.statusbar.setWhatsThis("")
        self.statusbar.setAutoFillBackground(False)
        self.statusbar.setSizeGripEnabled(True)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Nsfw Report Explorer v1.0 by MAX"))
        self.btnScanner.setToolTip(_translate("MainWindow", "<html><head/><body><p>Abrir Nsfw Scanner.</p></body></html>"))
        self.btnScanner.setAccessibleName(_translate("MainWindow", "Escanear Directorio."))
        self.btnOpen.setToolTip(_translate("MainWindow", "Abrir Reporte."))
        self.btnClose.setToolTip(_translate("MainWindow", "Cerrar Reporte."))
        self.btnSave.setToolTip(_translate("MainWindow", "Guardar reporte."))
        self.lblSelCount.setText(_translate("MainWindow", "0/0"))
        self.btnListUp.setToolTip(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.lblPages.setText(_translate("MainWindow", "1/1"))
        self.btnListDown.setToolTip(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.btnFiltro.setToolTip(_translate("MainWindow", "<html><head/><body><p>Aplicar / Quitar Filtro.</p><p><br/></p></body></html>"))
        self.lblFiltro.setText(_translate("MainWindow", "15%"))
        self.slrFiltro.setToolTip(_translate("MainWindow", "<html><head/><body><p>Especificar Filtro por Probabilidad.</p><p><br/></p></body></html>"))

