# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'scann_ui/ui_nsfw_scann.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_dlgNsfwScanner(object):
    def setupUi(self, dlgNsfwScanner):
        dlgNsfwScanner.setObjectName("dlgNsfwScanner")
        dlgNsfwScanner.setWindowModality(QtCore.Qt.ApplicationModal)
        dlgNsfwScanner.resize(1001, 655)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dlgNsfwScanner.sizePolicy().hasHeightForWidth())
        dlgNsfwScanner.setSizePolicy(sizePolicy)
        dlgNsfwScanner.setMaximumSize(QtCore.QSize(16777215, 16777215))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/icon-wifi.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        dlgNsfwScanner.setWindowIcon(icon)
        dlgNsfwScanner.setToolTip("")
        dlgNsfwScanner.setLayoutDirection(QtCore.Qt.LeftToRight)
        dlgNsfwScanner.setSizeGripEnabled(False)
        dlgNsfwScanner.setModal(False)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(dlgNsfwScanner)
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(dlgNsfwScanner)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.splitter = QtWidgets.QSplitter(self.groupBox)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnScannFolder = QtWidgets.QToolButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnScannFolder.sizePolicy().hasHeightForWidth())
        self.btnScannFolder.setSizePolicy(sizePolicy)
        self.btnScannFolder.setMinimumSize(QtCore.QSize(50, 50))
        self.btnScannFolder.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/icon-searchfolder.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnScannFolder.setIcon(icon1)
        self.btnScannFolder.setIconSize(QtCore.QSize(48, 48))
        self.btnScannFolder.setObjectName("btnScannFolder")
        self.horizontalLayout.addWidget(self.btnScannFolder, 0, QtCore.Qt.AlignLeft)
        self.btnVIC = QtWidgets.QToolButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnVIC.sizePolicy().hasHeightForWidth())
        self.btnVIC.setSizePolicy(sizePolicy)
        self.btnVIC.setMaximumSize(QtCore.QSize(52, 16777215))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btnVIC.setFont(font)
        self.btnVIC.setObjectName("btnVIC")
        self.horizontalLayout.addWidget(self.btnVIC)
        self.lblScannFolder = QtWidgets.QLabel(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblScannFolder.sizePolicy().hasHeightForWidth())
        self.lblScannFolder.setSizePolicy(sizePolicy)
        self.lblScannFolder.setMaximumSize(QtCore.QSize(16777215, 60))
        self.lblScannFolder.setWordWrap(False)
        self.lblScannFolder.setObjectName("lblScannFolder")
        self.horizontalLayout.addWidget(self.lblScannFolder)
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnSave = QtWidgets.QToolButton(self.layoutWidget1)
        self.btnSave.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnSave.sizePolicy().hasHeightForWidth())
        self.btnSave.setSizePolicy(sizePolicy)
        self.btnSave.setMinimumSize(QtCore.QSize(50, 50))
        self.btnSave.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/icon-save-floppy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnSave.setIcon(icon2)
        self.btnSave.setIconSize(QtCore.QSize(48, 48))
        self.btnSave.setObjectName("btnSave")
        self.horizontalLayout_2.addWidget(self.btnSave)
        self.lblSaveFolder = QtWidgets.QLabel(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblSaveFolder.sizePolicy().hasHeightForWidth())
        self.lblSaveFolder.setSizePolicy(sizePolicy)
        self.lblSaveFolder.setMaximumSize(QtCore.QSize(16777215, 60))
        self.lblSaveFolder.setWordWrap(False)
        self.lblSaveFolder.setObjectName("lblSaveFolder")
        self.horizontalLayout_2.addWidget(self.lblSaveFolder)
        self.groupBox_2 = QtWidgets.QGroupBox(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.groupBox_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.chkShowImage = QtWidgets.QCheckBox(self.groupBox_2)
        self.chkShowImage.setChecked(True)
        self.chkShowImage.setObjectName("chkShowImage")
        self.verticalLayout_3.addWidget(self.chkShowImage)
        self.progressBarScore = QtWidgets.QProgressBar(self.groupBox_2)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(252, 175, 62))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(252, 175, 62))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(145, 141, 126))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        self.progressBarScore.setPalette(palette)
        self.progressBarScore.setProperty("value", 15)
        self.progressBarScore.setObjectName("progressBarScore")
        self.verticalLayout_3.addWidget(self.progressBarScore, 0, QtCore.Qt.AlignTop)
        self.selScore = QtWidgets.QSlider(self.groupBox_2)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(252, 175, 62))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(252, 175, 62))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(145, 141, 126))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)
        self.selScore.setPalette(palette)
        self.selScore.setMaximum(100)
        self.selScore.setProperty("value", 15)
        self.selScore.setOrientation(QtCore.Qt.Horizontal)
        self.selScore.setObjectName("selScore")
        self.verticalLayout_3.addWidget(self.selScore, 0, QtCore.Qt.AlignTop)
        self.horizontalLayout_3.addWidget(self.splitter)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.frameImage = QtWidgets.QFrame(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frameImage.sizePolicy().hasHeightForWidth())
        self.frameImage.setSizePolicy(sizePolicy)
        self.frameImage.setMinimumSize(QtCore.QSize(256, 256))
        self.frameImage.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameImage.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameImage.setObjectName("frameImage")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.frameImage)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.lblImage = QtWidgets.QLabel(self.frameImage)
        self.lblImage.setMinimumSize(QtCore.QSize(256, 256))
        self.lblImage.setText("")
        self.lblImage.setObjectName("lblImage")
        self.verticalLayout_5.addWidget(self.lblImage)
        self.imageScore = QtWidgets.QProgressBar(self.frameImage)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 127, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 42, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 56, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 127, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 42, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 56, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ToolTipText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 42, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Button, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 170, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Light, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 127, 63))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Midlight, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 42, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Dark, brush)
        brush = QtGui.QBrush(QtGui.QColor(170, 56, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Mid, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 42, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.BrightText, brush)
        brush = QtGui.QBrush(QtGui.QColor(127, 42, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Window, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Shadow, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 85, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.AlternateBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 220))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipBase, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ToolTipText, brush)
        self.imageScore.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.imageScore.setFont(font)
        self.imageScore.setProperty("value", 0)
        self.imageScore.setAlignment(QtCore.Qt.AlignCenter)
        self.imageScore.setObjectName("imageScore")
        self.verticalLayout_5.addWidget(self.imageScore)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)
        self.horizontalLayout_3.addWidget(self.frameImage)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnStart = QtWidgets.QToolButton(self.groupBox)
        self.btnStart.setEnabled(False)
        self.btnStart.setMinimumSize(QtCore.QSize(50, 50))
        self.btnStart.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/icon-acsource.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnStart.setIcon(icon3)
        self.btnStart.setIconSize(QtCore.QSize(48, 48))
        self.btnStart.setObjectName("btnStart")
        self.verticalLayout.addWidget(self.btnStart)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.btnAceptar = QtWidgets.QToolButton(self.groupBox)
        self.btnAceptar.setEnabled(False)
        self.btnAceptar.setMinimumSize(QtCore.QSize(50, 50))
        self.btnAceptar.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/icon-circleselect.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAceptar.setIcon(icon4)
        self.btnAceptar.setIconSize(QtCore.QSize(48, 48))
        self.btnAceptar.setObjectName("btnAceptar")
        self.verticalLayout.addWidget(self.btnAceptar)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.btnClose = QtWidgets.QToolButton(self.groupBox)
        self.btnClose.setMinimumSize(QtCore.QSize(50, 50))
        self.btnClose.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/icon-circledelete.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnClose.setIcon(icon5)
        self.btnClose.setIconSize(QtCore.QSize(48, 48))
        self.btnClose.setObjectName("btnClose")
        self.verticalLayout.addWidget(self.btnClose)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.frame = QtWidgets.QFrame(dlgNsfwScanner)
        self.frame.setMinimumSize(QtCore.QSize(0, 0))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lblProgressBar = QtWidgets.QLabel(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblProgressBar.sizePolicy().hasHeightForWidth())
        self.lblProgressBar.setSizePolicy(sizePolicy)
        self.lblProgressBar.setText("")
        self.lblProgressBar.setWordWrap(False)
        self.lblProgressBar.setObjectName("lblProgressBar")
        self.verticalLayout_4.addWidget(self.lblProgressBar, 0, QtCore.Qt.AlignTop)
        self.progressBar = QtWidgets.QProgressBar(self.frame)
        self.progressBar.setMaximum(0)
        self.progressBar.setProperty("value", -1)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setObjectName("progressBar")
        self.verticalLayout_4.addWidget(self.progressBar, 0, QtCore.Qt.AlignTop)
        self.progressBar.raise_()
        self.lblProgressBar.raise_()
        self.verticalLayout_2.addWidget(self.frame, 0, QtCore.Qt.AlignTop)
        self.txtLog = QtWidgets.QTextEdit(dlgNsfwScanner)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtLog.sizePolicy().hasHeightForWidth())
        self.txtLog.setSizePolicy(sizePolicy)
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(78, 154, 6))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(46, 52, 54))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(78, 154, 6))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(46, 52, 54))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(239, 235, 231))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.txtLog.setPalette(palette)
        self.txtLog.setAutoFillBackground(False)
        self.txtLog.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.txtLog.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.txtLog.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.txtLog.setReadOnly(True)
        self.txtLog.setAcceptRichText(False)
        self.txtLog.setObjectName("txtLog")
        self.verticalLayout_2.addWidget(self.txtLog)
        self.lblScannStatus = QtWidgets.QLabel(dlgNsfwScanner)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblScannStatus.sizePolicy().hasHeightForWidth())
        self.lblScannStatus.setSizePolicy(sizePolicy)
        self.lblScannStatus.setMaximumSize(QtCore.QSize(16777215, 16777215))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(32, 74, 135))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(32, 74, 135))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(190, 190, 190))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        self.lblScannStatus.setPalette(palette)
        font = QtGui.QFont()
        font.setFamily("aakar")
        font.setBold(False)
        font.setWeight(50)
        self.lblScannStatus.setFont(font)
        self.lblScannStatus.setAutoFillBackground(True)
        self.lblScannStatus.setText("")
        self.lblScannStatus.setTextFormat(QtCore.Qt.PlainText)
        self.lblScannStatus.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lblScannStatus.setWordWrap(False)
        self.lblScannStatus.setObjectName("lblScannStatus")
        self.verticalLayout_2.addWidget(self.lblScannStatus, 0, QtCore.Qt.AlignBottom)
        self.lblScannFolder.setBuddy(self.btnScannFolder)
        self.lblSaveFolder.setBuddy(self.btnScannFolder)

        self.retranslateUi(dlgNsfwScanner)
        QtCore.QMetaObject.connectSlotsByName(dlgNsfwScanner)

    def retranslateUi(self, dlgNsfwScanner):
        _translate = QtCore.QCoreApplication.translate
        dlgNsfwScanner.setWindowTitle(_translate("dlgNsfwScanner", "Open Nsfw Scann v1.0 by MAX"))
        self.btnScannFolder.setToolTip(_translate("dlgNsfwScanner", "Directorio a Escanear."))
        self.btnScannFolder.setShortcut(_translate("dlgNsfwScanner", "Ctrl+S"))
        self.btnVIC.setToolTip(_translate("dlgNsfwScanner", "<html><head/><body><p>Escanear desde Reporte VIC 1.3.</p></body></html>"))
        self.btnVIC.setText(_translate("dlgNsfwScanner", "VIC"))
        self.lblScannFolder.setText(_translate("dlgNsfwScanner", "Seleccione el directorio a escanear!"))
        self.btnSave.setToolTip(_translate("dlgNsfwScanner", "Guardar Reporte."))
        self.lblSaveFolder.setText(_translate("dlgNsfwScanner", "Seleccione el Archivo para guaradar el Reporte!"))
        self.groupBox_2.setTitle(_translate("dlgNsfwScanner", "Filtro por Probabilidad"))
        self.chkShowImage.setToolTip(_translate("dlgNsfwScanner", "<html><head/><body><p>Muestra una vista previa de las imagenes que esten por sobre la Probabilidad espesificada.</p></body></html>"))
        self.chkShowImage.setText(_translate("dlgNsfwScanner", "Mostrar Nsfw Imagenes"))
        self.btnStart.setStatusTip(_translate("dlgNsfwScanner", "Iniciar Escaneo."))
        self.btnAceptar.setStatusTip(_translate("dlgNsfwScanner", "Cerrar."))
        self.btnClose.setStatusTip(_translate("dlgNsfwScanner", "Cerrar."))

