# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_ApplyNoiseSymbology.ui'
#
# Created: Thu Jul 17 16:25:14 2014
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

class Ui_ApplyNoiseSymbology_window(object):
    def setupUi(self, ApplyNoiseSymbology_window):
        ApplyNoiseSymbology_window.setObjectName(_fromUtf8("ApplyNoiseSymbology_window"))
        ApplyNoiseSymbology_window.setEnabled(True)
        ApplyNoiseSymbology_window.resize(713, 225)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ApplyNoiseSymbology_window.sizePolicy().hasHeightForWidth())
        ApplyNoiseSymbology_window.setSizePolicy(sizePolicy)
        ApplyNoiseSymbology_window.setMinimumSize(QtCore.QSize(713, 225))
        ApplyNoiseSymbology_window.setMaximumSize(QtCore.QSize(713, 225))
        ApplyNoiseSymbology_window.setSizeIncrement(QtCore.QSize(0, 0))
        ApplyNoiseSymbology_window.setLocale(QtCore.QLocale(QtCore.QLocale.Italian, QtCore.QLocale.Italy))
        self.horizontalLayoutWidget_2 = QtGui.QWidget(ApplyNoiseSymbology_window)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 165, 691, 41))
        self.horizontalLayoutWidget_2.setObjectName(_fromUtf8("horizontalLayoutWidget_2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.progressBar = QtGui.QProgressBar(self.horizontalLayoutWidget_2)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.horizontalLayout.addWidget(self.progressBar)
        self.run_buttonBox = QtGui.QDialogButtonBox(self.horizontalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.run_buttonBox.sizePolicy().hasHeightForWidth())
        self.run_buttonBox.setSizePolicy(sizePolicy)
        self.run_buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.run_buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.run_buttonBox.setObjectName(_fromUtf8("run_buttonBox"))
        self.horizontalLayout.addWidget(self.run_buttonBox)
        self.verticalLayoutWidget_2 = QtGui.QWidget(ApplyNoiseSymbology_window)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 15, 691, 61))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.receivers_layer_verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.receivers_layer_verticalLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.receivers_layer_verticalLayout.setMargin(0)
        self.receivers_layer_verticalLayout.setObjectName(_fromUtf8("receivers_layer_verticalLayout"))
        self.receiver_points_layer_label = QtGui.QLabel(self.verticalLayoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.receiver_points_layer_label.sizePolicy().hasHeightForWidth())
        self.receiver_points_layer_label.setSizePolicy(sizePolicy)
        self.receiver_points_layer_label.setObjectName(_fromUtf8("receiver_points_layer_label"))
        self.receivers_layer_verticalLayout.addWidget(self.receiver_points_layer_label)
        self.layer_comboBox = QtGui.QComboBox(self.verticalLayoutWidget_2)
        self.layer_comboBox.setObjectName(_fromUtf8("layer_comboBox"))
        self.receivers_layer_verticalLayout.addWidget(self.layer_comboBox)
        self.verticalLayoutWidget_3 = QtGui.QWidget(ApplyNoiseSymbology_window)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 90, 691, 61))
        self.verticalLayoutWidget_3.setObjectName(_fromUtf8("verticalLayoutWidget_3"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtGui.QLayout.SetMinAndMaxSize)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.choose_fileds_label = QtGui.QLabel(self.verticalLayoutWidget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.choose_fileds_label.sizePolicy().hasHeightForWidth())
        self.choose_fileds_label.setSizePolicy(sizePolicy)
        self.choose_fileds_label.setObjectName(_fromUtf8("choose_fileds_label"))
        self.horizontalLayout_2.addWidget(self.choose_fileds_label)
        self.level_comboBox = QtGui.QComboBox(self.verticalLayoutWidget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.level_comboBox.sizePolicy().hasHeightForWidth())
        self.level_comboBox.setSizePolicy(sizePolicy)
        self.level_comboBox.setObjectName(_fromUtf8("level_comboBox"))
        self.horizontalLayout_2.addWidget(self.level_comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.choose_fileds_label_2 = QtGui.QLabel(self.verticalLayoutWidget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.choose_fileds_label_2.sizePolicy().hasHeightForWidth())
        self.choose_fileds_label_2.setSizePolicy(sizePolicy)
        self.choose_fileds_label_2.setText(_fromUtf8("<html><head/><body><p><span style=\" font-style:italic;\">NOTE: For negative values the legend is \'No Level\'.</span></p></body></html>"))
        self.choose_fileds_label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.choose_fileds_label_2.setObjectName(_fromUtf8("choose_fileds_label_2"))
        self.verticalLayout.addWidget(self.choose_fileds_label_2)

        self.retranslateUi(ApplyNoiseSymbology_window)
        QtCore.QObject.connect(self.run_buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ApplyNoiseSymbology_window.accept)
        QtCore.QObject.connect(self.run_buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ApplyNoiseSymbology_window.reject)
        QtCore.QMetaObject.connectSlotsByName(ApplyNoiseSymbology_window)

    def retranslateUi(self, ApplyNoiseSymbology_window):
        ApplyNoiseSymbology_window.setWindowTitle(_translate("ApplyNoiseSymbology_window", "opeNoise - Apply Noise Symbology", None))
        self.receiver_points_layer_label.setText(_translate("ApplyNoiseSymbology_window", "Input layer:", None))
        self.choose_fileds_label.setText(_translate("ApplyNoiseSymbology_window", "Choose the sound level fields to apply noise symbology:", None))

