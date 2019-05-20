# -*- coding: utf-8 -*-
"""
/***************************************************************************
 opeNoise

 Qgis Plugin to compute noise levels.

                             -------------------
        begin                : March 2014
        copyright            : (C) 2014 by Arpa Piemonte
        email                : s.masera@arpa.piemonte.it
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

#from PyQt4.QtCore import *
from builtins import str
from qgis.PyQt.QtCore import QObject

from qgis.PyQt.QtWidgets import QDialog, QFileDialog
from qgis.PyQt.QtWidgets import QDialogButtonBox
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import QgsProject, QgsWkbTypes, QgsMapLayerProxyModel
from qgis.PyQt import uic
import os,sys
import traceback

#from math import *

from datetime import datetime

sys.path.append(os.path.dirname(__file__))
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_CreateReceiverPoints.ui'), resource_suffix='')
from . import on_CreateReceiverPoints

from . import on_Settings







class Dialog(QDialog,FORM_CLASS):
    
    def __init__(self, iface):
        QDialog.__init__(self, iface.mainWindow())
        self.iface = iface
        # Set up the user interface from Designer.
        self.setupUi(self)
                
        self.populateLayers()
        
        spaced_distance_list = ['1','2','3','4','5']        
        self.spaced_pts_comboBox.clear()
        for distance in spaced_distance_list:
            self.spaced_pts_comboBox.addItem(distance)
        self.spaced_pts_comboBox.setEnabled(False)
        
        self.middle_pts_radioButton.setChecked(1)
        self.spaced_pts_radioButton.setChecked(0)
        
        self.middle_pts_radioButton.toggled.connect(self.method_update)
        self.spaced_pts_radioButton.toggled.connect(self.method_update)

        self.receiver_layer_pushButton.clicked.connect(self.outFile)        
        self.buttonBox = self.buttonBox.button( QDialogButtonBox.Ok )


        self.progressBar.setValue(0)
    
    
    def populateLayers( self ):
        self.buildings_layer_comboBox.clear()
        self.buildings_layer_comboBox.setFilters(QgsMapLayerProxyModel.PolygonLayer)
        
    def outFile(self):
        self.receiver_layer_lineEdit.clear()

        self.shapefileName = QFileDialog.getSaveFileName(None,'Open file', on_Settings.getOneSetting('directory_last') , "Shapefile (*.shp);;All files (*)")

        if self.shapefileName is None or self.shapefileName == "":
            return
            
        if str.find(self.shapefileName[0],".shp") == -1 and str.find(self.shapefileName[0],".SHP") == -1:
            self.receiver_layer_lineEdit.setText( self.shapefileName[0] + ".shp")
        else:
            self.receiver_layer_lineEdit.setText( self.shapefileName[0])
       
        on_Settings.setOneSetting('directory_last',os.path.dirname(self.receiver_layer_lineEdit.text()))
            
    
    def method_update(self):
        
        if self.middle_pts_radioButton.isChecked():
            self.spaced_pts_comboBox.setEnabled(False)
        if self.spaced_pts_radioButton.isChecked():
            self.spaced_pts_comboBox.setEnabled(True)


    def log_start(self):
        
        global log_errors, log_errors_path_name
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)        
        log_errors_path_name = os.path.join(dir_path,"log_CreateReceiverPoints_errors.txt")
        log_errors = open(log_errors_path_name,"w")
        log_errors.write(self.tr("opeNoise") + " - " + self.tr("Create Receiver Points") + " - " + self.tr("Errors") + "\n\n")
        
        
    def log_end(self):

        log_errors.close()    

    def accept(self):
      
        self.buttonBox.setEnabled( False )
        if self.buildings_layer_comboBox.currentText() == "":
            QMessageBox.information(self, self.tr("opeNoise - Create Receiver Points"), self.tr("Please specify the buildings vector layer"))
            self.buttonBox.setEnabled( True )
            return
        elif self.receiver_layer_lineEdit.text() == "" or self.receiver_layer_lineEdit.text() == ".shp":
            QMessageBox.information(self, self.tr("opeNoise - Create Receiver Points"), self.tr("Please specify output shapefile"))
            
            self.buttonBox.setEnabled( True )
            return
        else:
            
            #buildings_layer = QgsProject.instance().mapLayersByName(self.buildings_layer_comboBox.currentText())[0]
            buildings_layer = self.buildings_layer_comboBox.currentLayer()
            buildings_layer_path = buildings_layer.source()
            receiver_points_layer_path = self.receiver_layer_lineEdit.text()
            
            # writes the settings log file
            self.log_start()
            
            self.time_start = datetime.now()
            
            bar = self.progressBar



            try:
                # CreateReceiverPoints
            
                if self.middle_pts_radioButton.isChecked():
                    on_CreateReceiverPoints.middle(bar,buildings_layer_path,receiver_points_layer_path)
                if self.spaced_pts_radioButton.isChecked():
                    spaced_pts_distance = float(self.spaced_pts_comboBox.currentText())
                    on_CreateReceiverPoints.spaced(bar,buildings_layer_path,receiver_points_layer_path,spaced_pts_distance)

                run = 1

            except:
                error= traceback.format_exc()
                log_errors.write(error)
                run = 0
                
            self.time_end = datetime.now()

            if run == 1:
                log_errors.write(self.tr("No errors.") + "\n\n") 
                result_string = self.tr("Receiver points created with success.") + "\n\n" +\
                                self.tr("Start: ") + self.time_start.strftime("%a %d/%b/%Y %H:%M:%S") + "\n" +\
                                self.tr("End: ") + self.time_end.strftime("%a %d/%b/%Y %H:%M:%S") + "\n"+\
                                self.tr("Duration: ") + str(self.duration())

                QMessageBox.information(self, self.tr("opeNoise - Create Receiver Points"), result_string)
            else:
                result_string = self.tr("Sorry, process not complete.") + "\n\n" +\
                                self.tr("View the log file to understand the problem:") + "\n" +\
                                str(log_errors_path_name) + "\n\n" +\
                                self.tr("Start: ") + self.time_start.strftime("%a %d/%b/%Y %H:%M:%S.%f") + "\n" +\
                                self.tr("End: ") + self.time_end.strftime("%a %d/%b/%Y %H:%M:%S.%f") + "\n"+\
                                self.tr("Duration: ") + str(self.duration())
                                
                QMessageBox.information(self, self.tr("opeNoise - Create Receiver Points"), self.tr(result_string))
                
                self.buttonBox.setEnabled( True )

           
            self.log_end()
        
        
        self.progressBar.setValue(0)
        self.buttonBox.setEnabled( True )

        self.close()
        
    def duration(self):
        duration = self.time_end - self.time_start
        duration_h = duration.seconds // 3600
        duration_m = (duration.seconds // 60) % 60
        duration_s = duration.seconds
        duration_string = str(format(duration_h, '02')) + ':' + str(format(duration_m, '02')) + ':' + str(
            format(duration_s, '02'))
        return duration_string

    
    

    
