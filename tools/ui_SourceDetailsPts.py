# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_SourceDetailsPts.ui'
#
# Created: Thu Aug 31 16:33:00 2017
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

class Ui_SourceDetailsPts_window(object):
    def setupUi(self, SourceDetailsPts_window):
        SourceDetailsPts_window.setObjectName(_fromUtf8("SourceDetailsPts_window"))
        SourceDetailsPts_window.resize(832, 234)
        self.buttonBox = QtGui.QDialogButtonBox(SourceDetailsPts_window)
        self.buttonBox.setGeometry(QtCore.QRect(440, 180, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.implementation_label_24 = QtGui.QLabel(SourceDetailsPts_window)
        self.implementation_label_24.setGeometry(QtCore.QRect(51, 76, 101, 16))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.implementation_label_24.sizePolicy().hasHeightForWidth())
        self.implementation_label_24.setSizePolicy(sizePolicy)
        self.implementation_label_24.setAlignment(QtCore.Qt.AlignCenter)
        self.implementation_label_24.setObjectName(_fromUtf8("implementation_label_24"))
        self.line_11 = QtGui.QFrame(SourceDetailsPts_window)
        self.line_11.setWindowModality(QtCore.Qt.NonModal)
        self.line_11.setGeometry(QtCore.QRect(21, 90, 781, 20))
        self.line_11.setFrameShape(QtGui.QFrame.HLine)
        self.line_11.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_11.setObjectName(_fromUtf8("line_11"))
        self.layoutWidget_2 = QtGui.QWidget(SourceDetailsPts_window)
        self.layoutWidget_2.setGeometry(QtCore.QRect(21, 110, 791, 35))
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.horizontalLayout_9 = QtGui.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_9.setMargin(0)
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.n_l_label_15 = QtGui.QLabel(self.layoutWidget_2)
        self.n_l_label_15.setMaximumSize(QtCore.QSize(16777215, 27))
        self.n_l_label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.n_l_label_15.setObjectName(_fromUtf8("n_l_label_15"))
        self.horizontalLayout_9.addWidget(self.n_l_label_15)
        self.POWER_P_L_gen_comboBox = QtGui.QComboBox(self.layoutWidget_2)
        self.POWER_P_L_gen_comboBox.setMaximumSize(QtCore.QSize(16777215, 27))
        self.POWER_P_L_gen_comboBox.setObjectName(_fromUtf8("POWER_P_L_gen_comboBox"))
        self.horizontalLayout_9.addWidget(self.POWER_P_L_gen_comboBox)
        self.POWER_P_L_day_comboBox = QtGui.QComboBox(self.layoutWidget_2)
        self.POWER_P_L_day_comboBox.setMaximumSize(QtCore.QSize(16777215, 27))
        self.POWER_P_L_day_comboBox.setObjectName(_fromUtf8("POWER_P_L_day_comboBox"))
        self.horizontalLayout_9.addWidget(self.POWER_P_L_day_comboBox)
        self.POWER_P_L_eve_comboBox = QtGui.QComboBox(self.layoutWidget_2)
        self.POWER_P_L_eve_comboBox.setMaximumSize(QtCore.QSize(16777215, 27))
        self.POWER_P_L_eve_comboBox.setObjectName(_fromUtf8("POWER_P_L_eve_comboBox"))
        self.horizontalLayout_9.addWidget(self.POWER_P_L_eve_comboBox)
        self.POWER_P_L_nig_comboBox = QtGui.QComboBox(self.layoutWidget_2)
        self.POWER_P_L_nig_comboBox.setMaximumSize(QtCore.QSize(16777215, 27))
        self.POWER_P_L_nig_comboBox.setObjectName(_fromUtf8("POWER_P_L_nig_comboBox"))
        self.horizontalLayout_9.addWidget(self.POWER_P_L_nig_comboBox)
        self.POWER_P_L_gen_checkBox = QtGui.QCheckBox(SourceDetailsPts_window)
        self.POWER_P_L_gen_checkBox.setGeometry(QtCore.QRect(221, 70, 91, 21))
        self.POWER_P_L_gen_checkBox.setChecked(False)
        self.POWER_P_L_gen_checkBox.setObjectName(_fromUtf8("POWER_P_L_gen_checkBox"))
        self.POWER_P_L_day_checkBox = QtGui.QCheckBox(SourceDetailsPts_window)
        self.POWER_P_L_day_checkBox.setGeometry(QtCore.QRect(381, 70, 81, 22))
        self.POWER_P_L_day_checkBox.setChecked(False)
        self.POWER_P_L_day_checkBox.setObjectName(_fromUtf8("POWER_P_L_day_checkBox"))
        self.POWER_P_L_eve_checkBox = QtGui.QCheckBox(SourceDetailsPts_window)
        self.POWER_P_L_eve_checkBox.setGeometry(QtCore.QRect(541, 70, 71, 22))
        self.POWER_P_L_eve_checkBox.setChecked(False)
        self.POWER_P_L_eve_checkBox.setObjectName(_fromUtf8("POWER_P_L_eve_checkBox"))
        self.label_2 = QtGui.QLabel(SourceDetailsPts_window)
        self.label_2.setGeometry(QtCore.QRect(20, 20, 751, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.POWER_P_L_nig_checkBox = QtGui.QCheckBox(SourceDetailsPts_window)
        self.POWER_P_L_nig_checkBox.setGeometry(QtCore.QRect(701, 70, 81, 22))
        self.POWER_P_L_nig_checkBox.setChecked(False)
        self.POWER_P_L_nig_checkBox.setObjectName(_fromUtf8("POWER_P_L_nig_checkBox"))

        self.retranslateUi(SourceDetailsPts_window)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), SourceDetailsPts_window.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), SourceDetailsPts_window.reject)
        QtCore.QMetaObject.connectSlotsByName(SourceDetailsPts_window)

    def retranslateUi(self, SourceDetailsPts_window):
        SourceDetailsPts_window.setWindowTitle(_translate("SourceDetailsPts_window", "Points Source Details", None))
        self.implementation_label_24.setText(_translate("SourceDetailsPts_window", "Data type", None))
        self.n_l_label_15.setText(_translate("SourceDetailsPts_window", "Power", None))
        self.POWER_P_L_gen_checkBox.setText(_translate("SourceDetailsPts_window", "Generic", None))
        self.POWER_P_L_day_checkBox.setText(_translate("SourceDetailsPts_window", "L day", None))
        self.POWER_P_L_eve_checkBox.setText(_translate("SourceDetailsPts_window", "L eve", None))
        self.label_2.setText(_translate("SourceDetailsPts_window", "For the point sources, you can set the type of implementation as follow:", None))
        self.POWER_P_L_nig_checkBox.setText(_translate("SourceDetailsPts_window", "L nig", None))

