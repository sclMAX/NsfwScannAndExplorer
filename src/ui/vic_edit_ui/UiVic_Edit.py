# -*- coding: utf-8 -*-
from src.ui.vic_edit_ui.ui_vic_edit import QtWidgets, QtCore, Ui_DialogVicEdit


class DlgVicEdit(QtWidgets.QDialog, Ui_DialogVicEdit):

    def __init__(self, parent: QtCore.QObject, media_item: dict):
        super().__init__(parent)
        self.setupUi(self)
        self.media_item: dict = media_item
        self.loadData()
        self.btnAceptar.clicked.connect(self.btnAceptar_click)
        self.btnClose.clicked.connect(self.btnClose_click)

    def loadData(self):
        self.Category.setText(str(self.media_item.get('Category')))
        self.VictimIdentified.setText(str(self.media_item.get('VictimIdentified')))
        self.OffenderIdentified.setText(str(self.media_item.get('OffenderIdentified')))
        self.Tags.setText(str(self.media_item.get('Tags')))
        isSet = self.media_item.get('IsDistributed')
        if not isSet:
            isSet = False
        self.IsDistributed.setChecked(isSet)
        isSet = self.media_item.get('IsSuspected')
        if not isSet:
            isSet = False
        self.IsSuspected.setChecked(isSet)
        isSet = self.media_item.get('IsPrecategorized')
        if not isSet:
            isSet = False
        self.IsPrecategorized.setChecked(isSet)

    def updateData(self):
        self.media_item['Category'] = self.Category.text()
        self.media_item['VictimIdentified'] = self.VictimIdentified.text()
        self.media_item['OffenderIdentified'] = self.OffenderIdentified.text()
        self.media_item['Tags'] = self.Tags.text()
        self.media_item['IsDistributed'] = self.IsDistributed.isChecked()
        self.media_item['IsSuspected'] = self.IsSuspected.isChecked()
        self.media_item['IsPrecategorized'] = self.IsPrecategorized.isChecked()

    def btnAceptar_click(self):
        self.updateData()
        self.accept()

    def btnClose_click(self):
        self.close()
