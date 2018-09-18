# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_AssignLevelsToBuildings.ui'
#
# Created: Thu Sep  7 10:32:46 2017
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from builtins import object
from qgis.PyQt import QtCore, QtGui

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

class Ui_AssignLevelsToBuildings_window(object):
    def setupUi(self, AssignLevelsToBuildings_window):
        AssignLevelsToBuildings_window.setObjectName(_fromUtf8("AssignLevelsToBuildings_window"))
        AssignLevelsToBuildings_window.setEnabled(True)
        AssignLevelsToBuildings_window.resize(713, 300)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AssignLevelsToBuildings_window.sizePolicy().hasHeightForWidth())
        AssignLevelsToBuildings_window.setSizePolicy(sizePolicy)
        AssignLevelsToBuildings_window.setMinimumSize(QtCore.QSize(713, 300))
        AssignLevelsToBuildings_window.setMaximumSize(QtCore.QSize(713, 300))
        AssignLevelsToBuildings_window.setSizeIncrement(QtCore.QSize(0, 0))
        AssignLevelsToBuildings_window.setLocale(QtCore.QLocale(QtCore.QLocale.Italian, QtCore.QLocale.Italy))
        self.verticalLayoutWidget = QtGui.QWidget(AssignLevelsToBuildings_window)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 170, 691, 61))
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
        self.horizontalLayoutWidget_2 = QtGui.QWidget(AssignLevelsToBuildings_window)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 240, 691, 41))
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
        self.verticalLayoutWidget_2 = QtGui.QWidget(AssignLevelsToBuildings_window)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(10, 20, 691, 61))
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
        self.receiver_points_layer_comboBox = QtGui.QComboBox(self.verticalLayoutWidget_2)
        self.receiver_points_layer_comboBox.setObjectName(_fromUtf8("receiver_points_layer_comboBox"))
        self.receivers_layer_verticalLayout.addWidget(self.receiver_points_layer_comboBox)
        self.line = QtGui.QFrame(AssignLevelsToBuildings_window)
        self.line.setGeometry(QtCore.QRect(10, 150, 681, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayoutWidget_3 = QtGui.QWidget(AssignLevelsToBuildings_window)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(10, 90, 691, 60))
        self.verticalLayoutWidget_3.setObjectName(_fromUtf8("verticalLayoutWidget_3"))
        self.verticalLayout = QtGui.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.choose_fileds_label = QtGui.QLabel(self.verticalLayoutWidget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.choose_fileds_label.sizePolicy().hasHeightForWidth())
        self.choose_fileds_label.setSizePolicy(sizePolicy)
        self.choose_fileds_label.setObjectName(_fromUtf8("choose_fileds_label"))
        self.verticalLayout.addWidget(self.choose_fileds_label)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.level_1_comboBox = QtGui.QComboBox(self.verticalLayoutWidget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.level_1_comboBox.sizePolicy().hasHeightForWidth())
        self.level_1_comboBox.setSizePolicy(sizePolicy)
        self.level_1_comboBox.setObjectName(_fromUtf8("level_1_comboBox"))
        self.horizontalLayout_2.addWidget(self.level_1_comboBox)
        self.level_2_comboBox = QtGui.QComboBox(self.verticalLayoutWidget_3)
        self.level_2_comboBox.setObjectName(_fromUtf8("level_2_comboBox"))
        self.horizontalLayout_2.addWidget(self.level_2_comboBox)
        self.level_3_comboBox = QtGui.QComboBox(self.verticalLayoutWidget_3)
        self.level_3_comboBox.setObjectName(_fromUtf8("level_3_comboBox"))
        self.horizontalLayout_2.addWidget(self.level_3_comboBox)
        self.level_4_comboBox = QtGui.QComboBox(self.verticalLayoutWidget_3)
        self.level_4_comboBox.setObjectName(_fromUtf8("level_4_comboBox"))
        self.horizontalLayout_2.addWidget(self.level_4_comboBox)
        self.level_5_comboBox = QtGui.QComboBox(self.verticalLayoutWidget_3)
        self.level_5_comboBox.setObjectName(_fromUtf8("level_5_comboBox"))
        self.horizontalLayout_2.addWidget(self.level_5_comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(AssignLevelsToBuildings_window)
        QtCore.QObject.connect(self.run_buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), AssignLevelsToBuildings_window.accept)
        QtCore.QObject.connect(self.run_buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), AssignLevelsToBuildings_window.reject)
        QtCore.QMetaObject.connectSlotsByName(AssignLevelsToBuildings_window)

    def retranslateUi(self, AssignLevelsToBuildings_window):
        AssignLevelsToBuildings_window.setWindowTitle(_translate("AssignLevelsToBuildings_window", "opeNoise - Assign Levels To Buildings", None))
        self.buildings_layer_label.setText(_translate("AssignLevelsToBuildings_window", "Buildings layer (input polygon layer)", None))
        self.receiver_points_layer_label.setText(_translate("AssignLevelsToBuildings_window", "Receiver points layer (input point layer)", None))
        self.choose_fileds_label.setText(_translate("AssignLevelsToBuildings_window", "Choose the sound level fields to assign to the buildings layer (the max level):", None))

