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
from qgis.core import QgsProject, QgsWkbTypes, QgsMapLayerProxyModel,QgsCoordinateReferenceSystem
try:
    from qgis.core import Qgis
except ImportError:
    from qgis.core import QGis as Qgis
from qgis.PyQt import uic
import os,sys
import traceback

#from math import *

from datetime import datetime

sys.path.append(os.path.dirname(__file__))
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_CreateReceiverPoints.ui'), resource_suffix='')
from . import on_CreateReceiverPoints,on_CreateGrid

from . import on_Settings







class Dialog(QDialog,FORM_CLASS):
    
    def __init__(self, iface):
        QDialog.__init__(self, iface.mainWindow())
        self.iface = iface
        # Set up the user interface from Designer.
        self.setupUi(self)
                
        self.populateLayers()
        # self.populate_overlayLayer()
        # added only distances of 5 m
        # spaced_distance_list = ['1','2','3','4','5']
        spaced_distance_list = ['5']
        self.spaced_pts_comboBox.clear()
        for distance in spaced_distance_list:
            self.spaced_pts_comboBox.addItem(distance)
        self.spaced_pts_comboBox.setEnabled(False)
        # scurisco in partenza l'opzione non default
        self.case2b_radioButton.setStyleSheet("color: gray;")
        self.label_5.setStyleSheet("color: gray;")

        self.middle_pts_radioButton.setChecked(1)
        self.spaced_pts_radioButton.setChecked(0)
        self.spaced_pts_radioButton.hide()
        self.spaced_pts_comboBox.hide()
        self.case2b_radioButton.setChecked(0)

        
        self.middle_pts_radioButton.toggled.connect(self.method_update)
        self.spaced_pts_radioButton.toggled.connect(self.method_update)
        self.case2b_radioButton.toggled.connect(self.method_update)

        self.receiver_layer_pushButton.clicked.connect(self.outFile)
        self.gridSave_pushButton.clicked.connect(self.outputFile_grid)
        self.runGrid_pushButton.clicked.connect(self.runGrid)
        self.buttonBox = self.buttonBox.button( QDialogButtonBox.Ok )

        # set the extend layer definition
        projCrs = QgsProject.instance().crs()
        canvas_extent = self.iface.mapCanvas().extent()
        self.ExtentGrid.setCurrentExtent(canvas_extent,projCrs)

        #     info button for receivers and grid
        self.infoReceivers.clicked.connect(self.infoReceivers_show)
        self.infoGrid.clicked.connect(self.infoGrid_show)


        self.progressBar.setValue(0)

        spacing = ['5', '10', '20', '30', '40', '50']
        self.resolution_comboBox.clear()
        for space in spacing:
            self.resolution_comboBox.addItem(space)
    
    def populateLayers( self ):
        if Qgis.QGIS_VERSION_INT < 31401:
            self.buildings_layer_comboBox.clear()
        self.buildings_layer_comboBox.setFilters(QgsMapLayerProxyModel.PolygonLayer)

    # def populate_overlayLayer(self):
    #
    #     if Qgis.QGIS_VERSION_INT < 31401:
    #         self.BuildingMaskLayerCombo.clear()
    #     self.BuildingMaskLayerCombo.allowEmptyLayer()
    #     self.BuildingMaskLayerCombo.setFilters(QgsMapLayerProxyModel.PolygonLayer)

    def infoReceivers_show(self):
        QMessageBox.information(self, self.tr("opeNoise - Help"), self.tr('''
         <p><strong>Create Receiver Points: </strong>By default, level calculations are performed 4m above the ground.  
         After creating the receivers, you can add a new attribute with a numeric field of a height other than 4m. 
         In the Calculate Noise Levels tool, you can activate the custom height of the receivers. 
         In this way it is possible to create receptor points at different floors of the building, making a copy of the points created by the tool.</p>
         '''))

    def infoGrid_show(self):
        QMessageBox.information(self, self.tr("opeNoise - Help"), self.tr('''
         <p><strong>Create Grid Points: </strong>By default, level calculations are performed 4m above the ground.  
         After creating the receivers, you can add a new attribute with a numeric field of a height other than 4m. 
         In the Calculate Noise Levels tool, you can activate the custom height of the receivers. 
         In this way it is possible to create receptor points at different height, making a copy of the points created by the tool. 
        </p>
         '''))

    def extent_layer_definition2(self):
        extent = self.iface.mapCanvas().extent()
        self.ExtentGrid.setCurrentExtent(extent,QgsCoordinateReferenceSystem("EPSG:3003"))

    def outputFile_grid(self):

        self.gridpoint_lineEdit.clear()
        self.fileName = QFileDialog.getSaveFileName(
            None,
            'Open file',
            on_Settings.getOneSetting('directory_last'),
            "Shapefile (*.shp);;All files (*)"
        )

        if self.fileName is None or self.fileName == "":
            return

        if str.find(self.fileName[0], ".shp") == -1 and str.find(self.fileName[0], ".SHP") == -1:
            self.gridpoint_lineEdit.setText(self.fileName[0] + ".shp")
        else:
            self.gridpoint_lineEdit.setText(self.fileName[0])

        pathFile = on_Settings.setOneSetting(
            'directory_last',
            os.path.dirname(self.gridpoint_lineEdit.text())
        )

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
        '''
        function to deactivate the combobox to select the distances
        :return:
        '''
        self.spaced_pts_radioButton.setEnabled(False)

        # metodo mezzeria facciata
        if self.middle_pts_radioButton.isChecked():
            # self.case2b_radioButton.setEnabled(True)
            self.case2b_radioButton.setStyleSheet("color: gray;")
            self.middle_pts_radioButton.setStyleSheet("color: black;")
            self.label_5.setStyleSheet("color: gray;")

        # metodo obsoleto
        if self.spaced_pts_radioButton.isChecked():
            pass
        # metodo nuovo
        if self.case2b_radioButton.isChecked():
            # self.middle_pts_radioButton.setEnabled(False)
            self.case2b_radioButton.setStyleSheet("color: black;")
            self.middle_pts_radioButton.setStyleSheet("color: gray;")
            self.label_5.setStyleSheet("color: black;")




    def log_start(self):
        
        global log_errors, log_errors_path_name
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)        
        log_errors_path_name = os.path.join(dir_path,"log_CreateReceiverPoints_errors.txt")
        log_errors = open(log_errors_path_name,"w")
        log_errors.write(self.tr("opeNoise") + " - " + self.tr("Create Receiver or Grid Points") + " - " + self.tr("Errors") + "\n\n")
        
        
    def log_end(self):

        log_errors.close()    

    def accept(self):
      
        self.buttonBox.setEnabled( False )
        if self.buildings_layer_comboBox.currentText() == "":
            QMessageBox.information(self, self.tr("opeNoise - Create Receiver or Grid Points"), self.tr("Please specify buildings layer"))
            self.buttonBox.setEnabled( True )
            return
        elif self.receiver_layer_lineEdit.text() == "" or self.receiver_layer_lineEdit.text() == ".shp":
            QMessageBox.information(self, self.tr("opeNoise - Create Receiver or Grid Points"), self.tr("Please specify output receiver points layer"))
            
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
                if self.case2b_radioButton.isChecked():
                    on_CreateReceiverPoints.case2b(bar,buildings_layer_path,receiver_points_layer_path)

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

                QMessageBox.information(self, self.tr("opeNoise - Create Receiver or Grid Points"), result_string)
            else:
                result_string = self.tr("Sorry, process not complete.") + "\n\n" +\
                                self.tr("View the log file to understand the problem:") + "\n" +\
                                str(log_errors_path_name) + "\n\n" +\
                                self.tr("Start: ") + self.time_start.strftime("%a %d/%b/%Y %H:%M:%S.%f") + "\n" +\
                                self.tr("End: ") + self.time_end.strftime("%a %d/%b/%Y %H:%M:%S.%f") + "\n"+\
                                self.tr("Duration: ") + str(self.duration())
                                
                QMessageBox.information(self, self.tr("opeNoise - Create Receiver or Grid Points"), self.tr(result_string))
                
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

    def runGrid(self):

        # check that CRS in projected
        project = QgsProject.instance()
        if project.crs().isGeographic():
            QMessageBox.information(self, self.tr("opeNoise - Create Receiver or Grid Points"), self.tr(
                "The project have to use a projected CRS (Coordinate Reference System)."))
            return

        # progressbar Grid Point
        BarGridReceiver = self.progressBarGridReceiver
        BarGridReceiver.setMaximum(100)

        extentSelected = self.ExtentGrid.outputExtent()
        if extentSelected.area() == 0:
            QMessageBox.information(self, self.tr("opeNoise - Create Receiver or Grid Points"),
                                    self.tr("Please specify extension layer"))
            return

        if self.gridpoint_lineEdit.text()== "" or self.gridpoint_lineEdit.text() == ".shp":
            QMessageBox.information(self, self.tr("opeNoise - Create Receiver or Grid Points"),
                                    self.tr("Please specify output grid points layer"))
            return





        resolution = int(self.resolution_comboBox.currentText())



        grid_path = self.gridpoint_lineEdit.text()

        if grid_path == "":
            QMessageBox.information(self, self.tr("opeNoise - Apply Noise Symbology"),
                                    self.tr("Please specify the output grid vector layer"))
            return 0




        on_CreateGrid.createGrid(
            resolution,
            grid_path,
            extentSelected,
            BarGridReceiver,

        )

        self.close()

    

    
