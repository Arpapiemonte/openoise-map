# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_CreateReceiverPoints.ui'
#
# Created: Wed Jan 18 15:46:23 2017
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_CreateReceiverPoints_window(object):
    def setupUi(self, CreateReceiverPoints_window):
        CreateReceiverPoints_window.setObjectName(_fromUtf8("CreateReceiverPoints_window"))
        CreateReceiverPoints_window.setEnabled(True)
        CreateReceiverPoints_window.resize(500, 229)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CreateReceiverPoints_window.sizePolicy().hasHeightForWidth())
        CreateReceiverPoints_window.setSizePolicy(sizePolicy)
        CreateReceiverPoints_window.setMinimumSize(QtCore.QSize(500, 229))
        CreateReceiverPoints_window.setMaximumSize(QtCore.QSize(500, 229))
        CreateReceiverPoints_window.setSizeIncrement(QtCore.QSize(0, 0))
        CreateReceiverPoints_window.setLocale(QtCore.QLocale(QtCore.QLocale.Italian, QtCore.QLocale.Italy))
        self.verticalLayoutWidget = QtGui.QWidget(CreateReceiverPoints_window)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 19, 481, 61))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.buildings_layer_verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.buildings_layer_verticalLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.buildings_layer_verticalLayout.setMargin(0)
        self.buildings_layer_verticalLayout.setObjectName(_fromUtf8("buildings_layer_verticalLayout"))
        self.buildings_layer_label = QtGui.QLabel(self.verticalLayoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buildings_layer_label.sizePolicy().hasHeightForWidth())
        self.buildings_layer_label.setSizePolicy(sizePolicy)
        self.buildings_layer_label.setObjectName(_fromUtf8("buildings_layer_label"))
        self.buildings_layer_verticalLayout.addWidget(self.buildings_layer_label)
        self.buildings_layer_comboBox = QtGui.QComboBox(self.verticalLayoutWidget)
        self.buildings_layer_comboBox.setObjectName(_fromUtf8("buildings_layer_comboBox"))
        self.buildings_layer_verticalLayout.addWidget(self.buildings_layer_comboBox)
        self.verticalLayoutWidget_2 = QtGui.QWidget(CreateReceiverPoints_window)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 100, 481, 61))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.receivers_layer_verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.receivers_layer_verticalLayout.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.receivers_layer_verticalLayout.setMargin(0)
        self.receivers_layer_verticalLayout.setObjectName(_fromUtf8("receivers_layer_verticalLayout"))
        self.receivers_layer_label = QtGui.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.receivers_layer_label.sizePolicy().hasHeightForWidth())
        self.receivers_layer_label.setSizePolicy(sizePolicy)
        self.receivers_layer_label.setObjectName(_fromUtf8("receivers_layer_label"))
        self.receivers_layer_verticalLayout.addWidget(self.receivers_layer_label)
        self.receiver_layer_horizontalLayout = QtGui.QHBoxLayout()
        self.receiver_layer_horizontalLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.receiver_layer_horizontalLayout.setObjectName(_fromUtf8("receiver_layer_horizontalLayout"))
        self.receiver_layer_lineEdit = QtGui.QLineEdit(self.verticalLayoutWidget_2)
        self.receiver_layer_lineEdit.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.receiver_layer_lineEdit.sizePolicy().hasHeightForWidth())
        self.receiver_layer_lineEdit.setSizePolicy(sizePolicy)
        self.receiver_layer_lineEdit.setObjectName(_fromUtf8("receiver_layer_lineEdit"))
        self.receiver_layer_horizontalLayout.addWidget(self.receiver_layer_lineEdit)
        self.receiver_layer_pushButton = QtGui.QPushButton(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.receiver_layer_pushButton.sizePolicy().hasHeightForWidth())
        self.receiver_layer_pushButton.setSizePolicy(sizePolicy)
        self.receiver_layer_pushButton.setObjectName(_fromUtf8("receiver_layer_pushButton"))
        self.receiver_layer_horizontalLayout.addWidget(self.receiver_layer_pushButton)
        self.receivers_layer_verticalLayout.addLayout(self.receiver_layer_horizontalLayout)
        self.horizontalLayoutWidget_2 = QtGui.QWidget(CreateReceiverPoints_window)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 180, 481, 31))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.progressBar = QtGui.QProgressBar(self.horizontalLayoutWidget_2)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.horizontalLayout.addWidget(self.progressBar)
        self.buttonBox = QtGui.QDialogButtonBox(self.horizontalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout.addWidget(self.buttonBox)

        self.retranslateUi(CreateReceiverPoints_window)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), CreateReceiverPoints_window.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), CreateReceiverPoints_window.reject)
        QtCore.QMetaObject.connectSlotsByName(CreateReceiverPoints_window)

    def retranslateUi(self, CreateReceiverPoints_window):
        CreateReceiverPoints_window.setWindowTitle(_translate("CreateReceiverPoints_window", "opeNoise - Create receiver points", None))
        self.buildings_layer_label.setText(_translate("CreateReceiverPoints_window", "Buildings layer (input polygon layer)", None))
        self.receivers_layer_label.setText(_translate("CreateReceiverPoints_window", "Receivers layer (output point layer)", None))
        self.receiver_layer_pushButton.setText(_translate("CreateReceiverPoints_window", "Browse", None))

