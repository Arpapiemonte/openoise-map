# -*- coding: utf-8 -*-
"""
/***************************************************************************
 opeNoise
 Qgis Plugin to compute noise levels
                             -------------------
        begin                : February 2022
        copyright            : (C) 2022 by Arpa Piemonte
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

from qgis.core import QgsProject, QgsMapLayerProxyModel

try:
    from qgis.core import Qgis
except ImportError:
    from qgis.core import QGis as Qgis
from qgis.PyQt import QtCore
from PyQt5 import QtGui, uic
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog, QMessageBox

import os
import sys

from . import on_CreateGrid, on_Settings

ui_path = os.path.join(
    os.path.dirname(__file__),
    'ui_ContoursLevel.ui'
)

FORM_CLASS, _ = uic.loadUiType(ui_path, resource_suffix='')


class Dialog(QDialog, FORM_CLASS):

    def __init__(self, iface):
        QDialog.__init__(self, iface.mainWindow())
        self.iface = iface
        self.setupUi(self)
        self.populate_layerTOrasterize()
        self.isolineSave_pushButton.clicked.connect(self.outputFile_contour)
        self.polygonSave_pushButton.clicked.connect(self.outputFile_polygon)
        self.runContPoly_pushButton.clicked.connect(self.runContPoly)



    def populate_layerTOrasterize(self):

        if Qgis.QGIS_VERSION_INT < 31401:
            self.layerTOrasterize_ComboBox.clear()
        self.layerTOrasterize_ComboBox.setFilters(QgsMapLayerProxyModel.PointLayer)
        self.fieldsLayer_ComboBox.setLayer(self.layerTOrasterize_ComboBox.currentLayer())




    def outputFile_raster(self):
        '''
        function not used anymore
        '''

        self.raster_lineEdit.clear()
        self.fileName = QFileDialog.getSaveFileName(
            None,
            'Open file',
            on_Settings.getOneSetting('directory_last'),
            "Raster (*.tif);;All files (*)"
        )

        if self.fileName is None or self.fileName == "":
            return

        if str.find(self.fileName[0], ".tif") == -1 and str.find(self.fileName[0], ".TIF") == -1:
            self.raster_lineEdit.setText(self.fileName[0] + ".tif")
        else:
            self.raster_lineEdit.setText(self.fileName[0])

        pathFile = on_Settings.setOneSetting(
            'directory_last',
            os.path.dirname(self.raster_lineEdit.text())
        )

    def outputFile_contour(self):

        self.isoline_lineEdit.clear()
        self.fileName = QFileDialog.getSaveFileName(
            None,
            'Open file',
            on_Settings.getOneSetting('directory_last'),
            "Shapefile (*.shp);;All files (*)"
        )



        if self.fileName is None or self.fileName == "":
            return

        if str.find(self.fileName[0], ".shp") == -1 and str.find(self.fileName[0], ".SHP") == -1:
            self.isoline_lineEdit.setText(self.fileName[0] + ".shp")
        else:
            self.isoline_lineEdit.setText(self.fileName[0])

        pathFile = on_Settings.setOneSetting(
            'directory_last',
            os.path.dirname(self.isoline_lineEdit.text())
        )

    def outputFile_polygon(self):

        self.polygon_lineEdit.clear()
        self.fileName = QFileDialog.getSaveFileName(
            None,
            'Open file',
            on_Settings.getOneSetting('directory_last'),
            "Shapefile (*.shp);;All files (*)"
        )



        if self.fileName is None or self.fileName == "":
            return

        if str.find(self.fileName[0], ".shp") == -1 and str.find(self.fileName[0], ".SHP") == -1:
            self.polygon_lineEdit.setText(self.fileName[0] + ".shp")
        else:
            self.polygon_lineEdit.setText(self.fileName[0])

        pathFile = on_Settings.setOneSetting(
            'directory_last',
            os.path.dirname(self.polygon_lineEdit.text())
        )



    # make Raster - Contour and Polygonize
    def runContPoly(self):
        ProgressBarGrid = self.progressBarGrid
        ProgressBarGrid.setMaximum(100)
        # test is linedit are compiled
        if self.layerTOrasterize_ComboBox.currentLayer() is None:
            QMessageBox.information(self, self.tr("opeNoise - Create Grid tool"),
                                    self.tr("Please specify grid receiver points layer"))
            return

        if self.isoline_lineEdit.text() == "" or self.isoline_lineEdit.text() == ".shp":
            QMessageBox.information(self, self.tr("opeNoise - Create Grid tool"),
                                    self.tr("Please specify output layer for contours level"))
            return

        if self.polygon_lineEdit.text() == "" or self.polygon_lineEdit.text() == ".shp":
            QMessageBox.information(self, self.tr("opeNoise - Create Grid tool"),
                                    self.tr("Please specify output layer for polygons level"))
            return

        resolution = 5
        layerTOrasterize = self.layerTOrasterize_ComboBox.currentLayer()
        layerTOrasterize_path = layerTOrasterize.source()
        field = self.fieldsLayer_ComboBox.currentText()

        # raster = self.rasterISOL_ComboBox.currentLayer()
        # raster_path = raster.source()

        minimum = self.min_spinBox.value()
        maximum = self.max_spinBox.value()
        interval = self.interval_spinBox.value()

        contour_path = self.isoline_lineEdit.text()
        poly_path = self.polygon_lineEdit.text()

        if contour_path == "" or poly_path == "":
            QMessageBox.information(self, self.tr("opeNoise - Create Grid tool"),
                                    self.tr("Please specify the output vector layers"))
            return 0

        # create isolines
        raster_path = on_CreateGrid.createRasterAndContour(
            resolution,
            layerTOrasterize_path,
            field,
            interval,
            contour_path,
            poly_path,
            ProgressBarGrid
        )

        self.close()

        # create polygon from reclassified raster
        # on_CreateGrid.polygonize(
        #     raster_path,
        #     minimum,
        #     maximum,
        #     interval,
        #     poly_path
        # )