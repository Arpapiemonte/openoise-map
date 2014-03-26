# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_Informations.ui'
#
# Created: Thu Mar 20 16:51:34 2014
#      by: PyQt4 UI code generator 4.10.3
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
        self.page_2 = QtGui.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.page_2.setObjectName(_fromUtf8("page_2"))
        self.textBrowser_8 = QtGui.QTextBrowser(self.page_2)
        self.textBrowser_8.setGeometry(QtCore.QRect(20, 0, 590, 351))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Ubuntu"))
        font.setBold(True)
        font.setWeight(75)
        self.textBrowser_8.setFont(font)
        self.textBrowser_8.setObjectName(_fromUtf8("textBrowser_8"))
        self.toolBox.addItem(self.page_2, _fromUtf8(""))
        self.page_3 = QtGui.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.page_3.setObjectName(_fromUtf8("page_3"))
        self.textBrowser_9 = QtGui.QTextBrowser(self.page_3)
        self.textBrowser_9.setGeometry(QtCore.QRect(20, 0, 590, 351))
        self.textBrowser_9.setObjectName(_fromUtf8("textBrowser_9"))
        self.toolBox.addItem(self.page_3, _fromUtf8(""))
        self.page_4 = QtGui.QWidget()
        self.page_4.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.page_4.setObjectName(_fromUtf8("page_4"))
        self.textBrowser_10 = QtGui.QTextBrowser(self.page_4)
        self.textBrowser_10.setGeometry(QtCore.QRect(20, 0, 590, 351))
        self.textBrowser_10.setObjectName(_fromUtf8("textBrowser_10"))
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
        self.textBrowser.setHtml(_translate("Info_window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">opeNoise</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /><span style=\" font-size:12pt;\">The plugin allows to compute the noise level generated by road traffic at fixed receiver points and buildings.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">The calculation is based on the French national computation method NMPB-Routes-96, as indicated in the DIRECTIVE 2002/49/EC OF THE EUROPEAN PARLIAMENT AND OF THE COUNCIL of 25 June 2002 relating to the assessment and management of environmental noise.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Please consider the following semplifications:<br />- the modelization is 2D (only the distance receiver points - roads is calculated considering the receiver points at 4m on the ground);<br />- no reflections or diffractions are calculated;<br />- the terrain is flat.</span></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.opeNoisePlugin), _translate("Info_window", "opeNoise", None))
        self.textBrowser_8.setHtml(_translate("Info_window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:600; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt;\">Create Receiver Points</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /><span style=\" font-size:12pt; font-weight:400;\">The first script generates one receiver point along all the facades of a buildings layer (a polygon layer). </span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:400;\">The points are created at a distance of 0.1 m from the facade.<br /><br /><br /></span><span style=\" font-size:12pt; font-style:italic; text-decoration: underline;\">INPUT DATA: </span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:400; font-style:italic;\">Buildings (a polygon layer)<br /><br /><br /></span><span style=\" font-size:12pt; font-style:italic; text-decoration: underline;\">OUTPUT DATA: </span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:400; font-style:italic;\">Receiver points (a point layer)</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("Info_window", "1  -   Create Receiver Points", None))
        self.textBrowser_9.setHtml(_translate("Info_window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">Calculate Noise Levels</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /><span style=\" font-size:12pt;\">The second script computes the noise level at receiver points (a point layer).</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">For each road (line of a polyline layer) is calculated the emission power as established in the NMPB \'96.<br />Then all the distances between each receiver point and the road is calculated, and the road is divided in emission points spaced as half of the minimum distance receiver points-road.<br />A ray is traced between each emission point and each receiver point and then, if the length of the ray is lower then a fixed distance (choosen in the input form), the noise level will be calculated.<br />To compute the level, it\'s taken into account only the geometrical divergence.<br />If the ray cross an obstacles, it won\'t be used to the final computation.<br />It\'s possible to create the emission points and rays layers.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">The computation is available for 4 reference periods, defined as established by the Italian law (in any case they are only \'label names\'):<br />- Ldiu: 06 - 22;<br />- Lnig: 22 - 06;<br />- Lday: 06 - 20;<br />- Leve: 20 - 22.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Lden, if checked, is calculated using the indication of the European Directive 2002/49/EC (penalizations of 5 dB for the evening period, and 10 dB for the night period).<br /><br />The computation results are written in the attribute table of the receiver points layer.<br /><br /></span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; font-style:italic; text-decoration: underline;\">INPUT DATA:</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-style:italic;\">1. Receiver points layer<br /></span><span style=\" font-size:12pt;\">A point layer.<br /><br /></span><span style=\" font-size:12pt; font-style:italic;\">2. Roads layer<br /></span><span style=\" font-size:12pt;\">A polyline layer.<br />It needs a roads layer input (a polyline layer) with some attributes table fields: it\'s necessary to give some information about the characteristic of the single road to exhistimate the emission power.<br />It\'s possible to indicate the power (expressed in dB) or, alternatively, to specify the number of light and heavy vehicles/hour, their speeds and the characteristic of the road as traffic type, surface and slope.<br />The power, as defined into NMPB \'96, is: sound power level per meter of lane, corrected in the light of the road surface during the reference period.<br /><br /></span><span style=\" font-size:12pt; font-style:italic;\">3. Distance<br /></span><span style=\" font-size:12pt;\">This is the maximum distance roads-receiver points allowed.<br /><br /></span><span style=\" font-size:12pt; font-style:italic;\">4. Obstacles (optional)<br /></span><span style=\" font-size:12pt;\">A polygon layer.<br /><br /><br /></span><span style=\" font-size:12pt; font-weight:600; font-style:italic; text-decoration: underline;\">OUTPUT DATA:</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-style:italic;\">1. Emission points layer<br /></span><span style=\" font-size:12pt;\">A point layer.<br /><br /></span><span style=\" font-size:12pt; font-style:italic;\">2. Rays layer<br /></span><span style=\" font-size:12pt;\">A polyline layer.</span></p></body></html>", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), _translate("Info_window", "2  -   Calculate Noise Levels", None))
        self.textBrowser_10.setHtml(_translate("Info_window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">Assign Levels To Buildings</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /><span style=\" font-size:12pt;\">The last script assigns the noise levels calculated for each receiver point to the corresponding building.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">The level assigned is the max level computed.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">It is possible to assign up to five levels.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">NOTE: this script works correctly only if you created the receiver points layer from a buildings layer with opeNoise and you didn\'t modify their structure.<br /></span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; font-style:italic; text-decoration: underline;\">INPUT DATA:</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-style:italic;\">1. Receiver points layer<br /></span><span style=\" font-size:12pt;\">A point layer.<br />You have to select at least a level field to assign the max level to the corresponding building.<br /><br /></span><span style=\" font-size:12pt; font-style:italic;\">2. Buildings layer<br /></span><span style=\" font-size:12pt;\">A polygon layer.<br /></span></p></body></html>", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_4), _translate("Info_window", "3  -   Assign Levels To Buldings", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Info_window", "How it works", None))
        self.textBrowser_4.setHtml(_translate("Info_window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">NMPB-Routes-96</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /><span style=\" font-size:12pt;\">The NMPB \'96 is the French national computation method for road traffic noise.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">In this plugin you can use it with the implementation of the emission power or of detailed data for each road, as the number of light and heavy vehicles, their speeds and the characteristics of the road, as traffic type, surface and slope.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">The power is the sound power level per meter of lane, corrected in the light of the road surface during the reference period.</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">The detailed data of the roads are:</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">- number of light vehicles per hour (number);<br />- number of heavy vehicles per hour (number);<br />- speed of light vehicles (number);<br />- speed of heavy vehicles (number);<br />- type of the traffic flow (string: \'continuos\', \'pulsed accelerated\', \'pulsed decelerated\', \'non-differentiated pulsed\');<br />- type of road surface (string: \'smooth\', \'porous\', \'stones\', \'cement\', \'corrugated\')<br />- slope of the road (string: \'flat\', \'down\', \'up\').</span></p>\n"
"<p align=\"justify\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Info_window", "NMPB-Routes-96", None))
        self.textBrowser_5.setHtml(_translate("Info_window", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Ubuntu\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:16pt; font-weight:600;\">Credits</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /><span style=\" font-size:12pt; font-style:italic; text-decoration: underline;\">opeNoise:</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Experimental Qgis Plugin to compute noise levels<br />version 0.1 - March 2014<br />GNU General Public License version 2 or later</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /><span style=\" font-size:12pt; font-style:italic; text-decoration: underline;\">Created by:<br /><br /></span><img src=\":/plugins/opeNoise/icons/icon_arpa_piemonte.png\" height=\"60\" /><br /><span style=\" font-size:12pt;\"><br />Arpa Piemonte<br />(Environmental Protection Agency of Piedmont - Italy)<br /></span><a href=\"http://www.arpa.piemonte.it\"><span style=\" text-decoration: underline; color:#0000ff;\">www.arpa.piemonte.it</span></a></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-style:italic; text-decoration: underline;\"><br />With the support of:<br /><br /></span><img src=\":/plugins/opeNoise/icons/icon_comune_torino.png\" height=\"120\" /><br /><span style=\" font-size:12pt;\"><br />Città di Torino<br /></span><a href=\"http://www.comune.torino.it/\"><span style=\" text-decoration: underline; color:#0000ff;\">www.comune.torino.it<br /><br /></span></a><span style=\" font-size:12pt;\"><br /></span><span style=\" font-size:12pt; font-style:italic; text-decoration: underline;\">Contacs:</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Stefano Masera<br />s.masera@arpa.piemonte.it</span></p>\n"
"<p align=\"center\" style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt;\">Enrico Gallo<br />enrico.gallo@comune.torino.it</span><br /><br /></p></body></html>", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Info_window", "Credits", None))

