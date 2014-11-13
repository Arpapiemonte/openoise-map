# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_Informations.ui'
#
# Created: Thu Nov 13 11:14:50 2014
#      by: PyQt4 UI code generator 4.9.6
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

class Ui_Info_window(object):
    def setupUi(self, Info_window):
        Info_window.setObjectName(_fromUtf8("Info_window"))
        Info_window.resize(700, 590)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Info_window.sizePolicy().hasHeightForWidth())
        Info_window.setSizePolicy(sizePolicy)
        Info_window.setMinimumSize(QtCore.QSize(700, 590))
        Info_window.setMaximumSize(QtCore.QSize(700, 590))
        self.buttonBox = QtGui.QDialogButtonBox(Info_window)
        self.buttonBox.setGeometry(QtCore.QRect(490, 550, 201, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.tabWidget = QtGui.QTabWidget(Info_window)
        self.tabWidget.setGeometry(QtCore.QRect(20, 20, 660, 521))
        self.tabWidget.setToolTip(_fromUtf8(""))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.opeNoisePlugin = QtGui.QWidget()
        self.opeNoisePlugin.setObjectName(_fromUtf8("opeNoisePlugin"))
        self.textBrowser = QtGui.QTextBrowser(self.opeNoisePlugin)
        self.textBrowser.setGeometry(QtCore.QRect(30, 20, 600, 440))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setBold(False)
        font.setWeight(50)
        self.textBrowser.setFont(font)
        
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.tabWidget.addTab(self.opeNoisePlugin, _fromUtf8(""))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.toolBox = QtGui.QToolBox(self.tab_4)
        self.toolBox.setGeometry(QtCore.QRect(10, 20, 631, 451))
        self.toolBox.setObjectName(_fromUtf8("toolBox"))
        self.page_1 = QtGui.QWidget()
        self.page_1.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.page_1.setObjectName(_fromUtf8("page_1"))
        self.textBrowser_8 = QtGui.QTextBrowser(self.page_1)
        self.textBrowser_8.setGeometry(QtCore.QRect(20, 0, 590, 321))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setBold(True)
        font.setWeight(75)
        self.textBrowser_8.setFont(font)
        
        self.textBrowser_8.setObjectName(_fromUtf8("textBrowser_8"))
        self.toolBox.addItem(self.page_1, _fromUtf8(""))
        self.page_2 = QtGui.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.page_2.setObjectName(_fromUtf8("page_2"))
        self.textBrowser_9 = QtGui.QTextBrowser(self.page_2)
        self.textBrowser_9.setGeometry(QtCore.QRect(20, 0, 590, 321))
        
        self.textBrowser_9.setObjectName(_fromUtf8("textBrowser_9"))
        self.toolBox.addItem(self.page_2, _fromUtf8(""))
        self.page_3 = QtGui.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.page_3.setObjectName(_fromUtf8("page_3"))
        self.textBrowser_10 = QtGui.QTextBrowser(self.page_3)
        self.textBrowser_10.setGeometry(QtCore.QRect(20, 0, 590, 321))
        
        self.textBrowser_10.setObjectName(_fromUtf8("textBrowser_10"))
        self.toolBox.addItem(self.page_3, _fromUtf8(""))
        self.page_4 = QtGui.QWidget()
        self.page_4.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.page_4.setObjectName(_fromUtf8("page_4"))
        self.textBrowser_11 = QtGui.QTextBrowser(self.page_4)
        self.textBrowser_11.setGeometry(QtCore.QRect(20, 0, 590, 321))
        
        self.textBrowser_11.setObjectName(_fromUtf8("textBrowser_11"))
        self.toolBox.addItem(self.page_4, _fromUtf8(""))
        self.tabWidget.addTab(self.tab_4, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.textBrowser_4 = QtGui.QTextBrowser(self.tab_2)
        self.textBrowser_4.setGeometry(QtCore.QRect(30, 30, 600, 440))
        
        self.textBrowser_4.setObjectName(_fromUtf8("textBrowser_4"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.textBrowser_5 = QtGui.QTextBrowser(self.tab)
        self.textBrowser_5.setGeometry(QtCore.QRect(30, 30, 600, 440))
        
        self.textBrowser_5.setObjectName(_fromUtf8("textBrowser_5"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))

        self.retranslateUi(Info_window)
        self.tabWidget.setCurrentIndex(0)
        self.toolBox.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Info_window.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Info_window.reject)
        QtCore.QMetaObject.connectSlotsByName(Info_window)

    def retranslateUi(self, Info_window):
        Info_window.setWindowTitle(_translate("Info_window", "opeNoise - Informations", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.opeNoisePlugin), _translate("Info_window", "opeNoise", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_1), _translate("Info_window", "1  -   Create Receiver Points", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("Info_window", "2  -   Calculate Noise Levels", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), _translate("Info_window", "3  -   Assign Levels To Buldings", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_4), _translate("Info_window", "4  -   Apply Noise Symbology", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Info_window", "How it works", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Info_window", "NMPB-Routes-96", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Info_window", "Credits", None))

