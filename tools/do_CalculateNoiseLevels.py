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
from __future__ import print_function

#from PyQt4.QtCore import *
from builtins import str

from qgis.PyQt.QtCore import QVariant, Qt
from qgis.PyQt.QtWidgets import QDialog
#from qgis.core import *
from qgis.PyQt.QtWidgets import QFileDialog
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import (QgsProject, QgsWkbTypes, QgsMapLayerProxyModel,QgsVectorFileWriter)
try:
    from qgis.core import Qgis
except ImportError:
    from qgis.core import QGis as Qgis
from qgis.PyQt import uic
from osgeo import ogr
import os, sys
from pathlib import Path
import traceback

#from math import *

from datetime import datetime

sys.path.append(os.path.dirname(__file__))
NoiseLevel_ui, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_CalculateNoiseLevels.ui'), resource_suffix='')
from . import do_SourceDetailsPts,do_SourceDetailsRoads
from . import on_Settings
from . import on_CalculateNoiseLevels


def removeLayer(path_layer):
    # remove layer from TOC if already loaded
    basefile = os.path.basename(path_layer)
    diff_layer = os.path.splitext(basefile)[0]
    directory = os.path.dirname(path_layer)
    extensions = ["shp", "shx", "dbf", "prj", "sbn", "sbx", "fbn", "fbx", "ain", "aih", "ixs", "mxs", "atx", "xml",
                  "cpg", "qix"]
    if len(QgsProject.instance().mapLayersByName(diff_layer)) > 0:
        lyr = QgsProject.instance().mapLayersByName(diff_layer)[0]
        print(diff_layer,':',directory,':',basefile,':',path_layer)
        print('rename layer1: ', lyr.id())
        print(os.path.join(directory,diff_layer+'1.shp',))
        QgsProject.instance().removeMapLayer(lyr.id())
        QgsVectorFileWriter.deleteShapeFile(path_layer)

        # for ext in extensions:
        #     f = os.path.join(directory,diff_layer+'.'+ext)
        #     if os.path.exists(f):
        #         print('removing file: ',f)
        #         os.remove(f)





class Dialog(QDialog,NoiseLevel_ui):

    def __init__(self, iface):
        QDialog.__init__(self, iface.mainWindow())

        self.iface = iface
        # Set up the user interface from Designer.
        self.setupUi(self)


        self.tabWidget.setCurrentIndex(0)
        self.reload_last_settings_pushButton.clicked.connect(self.reload_last_settings)
        self.reload_saved_settings_pushButton.clicked.connect(self.reload_saved_settings)

        if len(list(QgsProject.instance().mapLayers().values())) > 0:
            self.populateLayersReceiver()
            self.populateLayersSourcePts()
            self.populateLayersSourceRoads()

        self.sources_pts_layer_checkBox.setEnabled(True)
        self.sources_roads_layer_checkBox.setEnabled(True)
        self.sources_checkBox_update()

        self.sources_pts_layer_checkBox.toggled.connect(self.sources_checkBox_update)
        self.sources_roads_layer_checkBox.toggled.connect(self.sources_checkBox_update)
        self.sources_pts_layer_comboBox.currentIndexChanged.connect(self.sources_pts_update)
        self.sources_roads_layer_comboBox.currentIndexChanged.connect(self.sources_roads_update)

        self.sources_pts_pushButton.clicked.connect(self.sourcePts_show)
        self.sources_roads_pushButton.clicked.connect(self.sourceRoads_show)
        # self.helpBuilding.cliFcked.connect(self.helpBuilding_show)
        self.HelpParameters.clicked.connect(self.HelpParameters_show)
        self.helpCalculateOptions.clicked.connect(self.HelpCalculateOptions_show)


        self.buildings_layer_checkBox.setChecked(0)
        self.buildings_layer_comboBox.setEnabled(False)
        self.buildings_layer_label.setEnabled(False)
        self.buildings_layer_label2.setEnabled(False)
        self.buildings_layer_checkBox.toggled.connect(self.buildings_checkBox_update)


        self.save_settings_checkBox.setChecked(0)
        self.save_settings_checkBox.toggled.connect(self.save_settings_checkBox_update)
        self.save_settings_pushButton.clicked.connect(self.outFile_save_settings)

        research_ray = ['50','100','250','500','1000']
        self.research_ray_comboBox.clear()
        for value in research_ray:
            self.research_ray_comboBox.addItem(value)

        # cambio temperatura TASK
        temperature = ['-20', '-15', '-10', '-5', '0', '5', '10', '15', '20',
                       '25', '30', '35', '40', '45', '50']
        self.temperature_comboBox.clear()
        for value in temperature:
            self.temperature_comboBox.addItem(value)
        idx = self.temperature_comboBox.findText('20')
        self.temperature_comboBox.setCurrentIndex(idx)

        humidity = ['10','20','30','40','50','60','70','80','90','100']
        self.humidity_comboBox.clear()
        for value in humidity:
            self.humidity_comboBox.addItem(value)
        idx = self.humidity_comboBox.findText('70')
        self.humidity_comboBox.setCurrentIndex(idx)

        self.L_den_checkBox.setChecked(0)
        self.L_den_checkBox.setEnabled(False)
        self.den_checkBox_update()
        self.L_den_checkBox.toggled.connect(self.den_checkBox_update)

        self.rays_layer_checkBox.setChecked(0)
        self.rays_layer_checkBox.toggled.connect(self.rays_checkBox_update)
        self.rays_layer_pushButton.clicked.connect(self.outFile_rays)
        self.diff_rays_layer_checkBox.setChecked(0)
        self.diff_rays_layer_checkBox.toggled.connect(self.diff_rays_checkBox_update)
        self.diff3DRaysCheck.setChecked(0)
        self.diff3DRaysCheck.toggled.connect(self.diff3D_rays_checkBox_update)
        self.skip_diffraction_checkBox.setChecked(0)
        self.skip_diffraction_checkBox.toggled.connect(self.skip_diffraction_checkBox_update)
        self.saveEmissionCheckBox.setChecked(0)
        self.diff_rays_layer_pushButton.clicked.connect(self.outFile_diff_rays)
        self.dif3Df_rays_layer_pushButton.clicked.connect(self.outFile_diff3D_rays)

        # turn off widget with
        self.barsWidget.hide()

        self.tabWidget.currentChanged.connect(self.tabUpdate)

        self.calculate_pushButton.clicked.connect(self.accept)

        # progress bars
        self.progress_bars = {'create_dif' : {'bar' : self.progressBar_create_dif, 'label' : self.label_time_create_dif},
                              'prepare_emi' : {'bar' : self.progressBar_prepare_emi, 'label' : self.label_time_prepare_emi},
                              'recTOsou' : {'bar' : self.progressBar_recTOsou, 'label' : self.label_time_recTOsou},
                              'difTOsou' : {'bar' : self.progressBar_difTOsou, 'label' : self.label_time_difTOsou},
                              'recTOdif' : {'bar' : self.progressBar_recTOdif, 'label' : self.label_time_recTOdif},
                              'calculate' : {'bar' : self.progressBar_calculate, 'label' : self.label_time_calculate}
                                }
        for key in self.progress_bars:
            self.progress_bars[key]['label'].setText('')

        self.label_time_start.setText('')
        self.label_time_end.setText('')
        self.label_time_duration.setText('')

    # def helpBuilding_show(self):
    #     QMessageBox.information(self, self.tr("opeNoise - Help"),
    #                             self.tr("Buildings are considered as obstacles to the propagation, diffraction effects are taken into account"))
    def HelpParameters_show(self):
        QMessageBox.information(self, self.tr("opeNoise - Help"), self.tr('''
<p><strong>Search ray: </strong>maximum distance of influence of the source to the receiver is expressed in meters. Receiver points beyond research ray return a -99 value. Setting a smaller search ray reduces the calculation time with consequent loss of precision in noise levels estimates.
</p><p><strong>Lden definition: </strong>in accordance with Directive 2002/49/CE and regulations of each Country. The plugin automatically calculates the value of Lden when emission levels referred to the three reference periods are set (Day, Evening, Night).</p>
        '''))

    def HelpCalculateOptions_show(self):
        QMessageBox.information(self, self.tr("opeNoise - Help"), self.tr('''
        <p><strong>Skip Diffraction Calculation: </strong>the calculation will not take into account the diffraction of horizontal and vertical obstacles. This reduces the calculation time with consequent loss of precision in sound levels estimates. Receiver points beyond buildings return a -99 value.</p>
<p><strong>Save Emission Level in Source Layer: </strong>allows you to save road emissions in the input layer.&nbsp; The results are expressed in dB(A).</p> 
<p><strong>Save Current Settings: </strong>allows you to save all settings. Saved settings can be reloaded later in the start tab.</p>
        '''))


    def sourcePts_show(self):
        if self.sources_pts_layer_comboBox.currentText() == "":
            QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("Please specify points source layer"))
            return False
        else:
            d = do_SourceDetailsPts.Dialog(self.iface, self.sources_pts_layer_comboBox.currentText())
            d.setWindowModality(Qt.ApplicationModal)
            d.show()
            d.exec_()



    def sourceRoads_show(self):
        if self.sources_roads_layer_comboBox.currentText() == "":
            QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("Please specify roads source layer"))
            return False
        else:
            d = do_SourceDetailsRoads.Dialog(self.iface, self.sources_roads_layer_comboBox.currentText())
            d.setWindowModality(Qt.ApplicationModal)
            d.show()
            d.exec_()


    def populateLayersReceiver( self ):
        if Qgis.QGIS_VERSION_INT < 31401:
            self.receivers_layer_comboBox.clear()
        self.receivers_layer_comboBox.setFilters(QgsMapLayerProxyModel.PointLayer)
        self.field_height_receiver.setLayer(self.receivers_layer_comboBox.currentLayer())



    def populateLayersSourcePts( self ):
        if Qgis.QGIS_VERSION_INT < 31401:
            self.sources_pts_layer_comboBox.clear()
        self.sources_pts_layer_comboBox.setFilters(QgsMapLayerProxyModel.PointLayer)



    def populateLayersSourceRoads( self ):
        if Qgis.QGIS_VERSION_INT < 31401:
            self.sources_roads_layer_comboBox.clear()
        self.sources_roads_layer_comboBox.setFilters(QgsMapLayerProxyModel.LineLayer)


    def populateLayersBuildings( self ):
        if Qgis.QGIS_VERSION_INT < 31401:
            self.buildings_layer_comboBox.clear()
        self.buildings_layer_comboBox.setFilters(QgsMapLayerProxyModel.PolygonLayer)
        self.field_height_building.setLayer(self.buildings_layer_comboBox.currentLayer())



    def sources_checkBox_update(self):

        if self.sources_pts_layer_checkBox.isChecked():
            self.sources_pts_layer_label.setEnabled(True)
            self.sources_pts_layer_comboBox.setEnabled(True)
            self.sources_pts_pushButton.setEnabled(True)
        else:
            self.sources_pts_layer_label.setEnabled(False)
            self.sources_pts_layer_comboBox.setEnabled(False)
            self.sources_pts_pushButton.setEnabled(False)

        if self.height_receiver_check.isChecked():
            self.field_height_receiver.setEnabled(True)
        else:
            self.field_height_receiver.setEnabled(False)

        if self.height_building_check.isChecked():
            self.field_height_building.setEnabled(True)
        else:
            self.field_height_building.setEnabled(False)

        if self.sources_roads_layer_checkBox.isChecked():
            self.sources_roads_layer_label.setEnabled(True)
            self.sources_roads_layer_comboBox.setEnabled(True)
            self.sources_roads_pushButton.setEnabled(True)
        else:
            self.sources_roads_layer_label.setEnabled(False)
            self.sources_roads_layer_comboBox.setEnabled(False)
            self.sources_roads_pushButton.setEnabled(False)

        # if self.sources_pts_layer_checkBox.isChecked() and self.sources_roads_layer_checkBox.isChecked():
        #     QMessageBox.warning(self, self.tr("opeNoise - Calculate Noise Levels"),
        #                             self.tr("Please select only one source layer: points or roads"))



    def sources_pts_update( self ):
        source_pts = on_Settings.getOneSetting('sources_pts_name')
        if self.sources_pts_layer_comboBox.currentText() != "" and self.sources_pts_layer_comboBox.currentText() != source_pts:
            on_Settings.clearPtsEmissionSettings()


    def sources_roads_update( self ):
        source_roads = on_Settings.getOneSetting('sources_roads_name')
        if self.sources_roads_layer_comboBox.currentText() != "" and self.sources_roads_layer_comboBox.currentText() != source_roads:
            on_Settings.clearRoadsEmissionSettings()


    def buildings_checkBox_update(self):

        if self.buildings_layer_checkBox.isChecked():
            self.buildings_layer_label.setEnabled(True)
            self.buildings_layer_label2.setEnabled(True)
            self.buildings_layer_comboBox.setEnabled(True)
            self.height_building_check.setEnabled(True)
            self.populateLayersBuildings()
        else:
            self.buildings_layer_label.setEnabled(False)
            self.buildings_layer_label2.setEnabled(False)
            self.buildings_layer_comboBox.setEnabled(False)
            self.height_building_check.setEnabled(False)
            self.height_building_check.setChecked(0)
            self.diff3DRaysCheck.setChecked(0)
            self.populateLayersBuildings()

    def tabUpdate(self):

        # Lden check
        settings = on_Settings.getAllSettings()

        day_pts = False
        eve_pts = False
        nig_pts = False
        day_roads = False
        eve_roads = False
        nig_roads = False

        if self.sources_pts_layer_checkBox.isChecked():
            if settings['period_pts_day'] == 'True':
                day_pts = True
            if settings['period_pts_eve'] == 'True':
                eve_pts = True
            if settings['period_pts_nig'] == 'True':
                nig_pts = True
        if self.sources_roads_layer_checkBox.isChecked():
            if settings['period_roads_day'] == 'True':
                day_roads = True
            if settings['period_roads_eve'] == 'True':
                eve_roads = True
            if settings['period_roads_nig'] == 'True':
                nig_roads = True

        #L_den option activated only if all data are provided
        if (day_pts == True and eve_pts == True and nig_pts == True) or (day_roads == True and eve_roads == True and nig_roads == True):
            #self.L_den_checkBox.setEnabled(True)
            self.L_den_checkBox.setChecked(True)
        else:
            self.L_den_checkBox.setChecked(False)
            self.L_den_checkBox.setEnabled(False)

        self.den_checkBox_update()

        # label
        if self.rays_layer_checkBox.isChecked() or self.diff_rays_layer_checkBox.isChecked():
            self.label_calculate.setText(self.tr('Calculate levels and draw rays'))
        else:
            self.label_calculate.setText(self.tr('Calculate levels'))

    def den_checkBox_update(self):

        if self.L_den_checkBox.isChecked():
            self.L_day_hours_spinBox.setEnabled( True )
            self.L_eve_hours_spinBox.setEnabled( True )
            self.L_nig_hours_spinBox.setEnabled( True )
            # self.L_day_penalty_spinBox.setEnabled( True )
            # self.L_eve_penalty_spinBox.setEnabled( True )
            # self.L_nig_penalty_spinBox.setEnabled( True )
            self.L_den_day_label.setEnabled( True )
            self.L_den_eve_label.setEnabled( True )
            self.L_den_nig_label.setEnabled( True )
            self.L_den_hours_label.setEnabled( True )
            self.L_den_eve_label_penalization.setEnabled( True )
            self.L_den_nig_label_penalization .setEnabled( True )
            # self.L_den_penalty_label.setEnabled( True )
        else:
            self.L_day_hours_spinBox.setEnabled( False )
            self.L_eve_hours_spinBox.setEnabled( False )
            self.L_nig_hours_spinBox.setEnabled( False )
            # self.L_day_penalty_spinBox.setEnabled( False )
            # self.L_eve_penalty_spinBox.setEnabled( False )
            # self.L_nig_penalty_spinBox.setEnabled( False )
            self.L_day_penalty_spinBox.hide()
            self.L_eve_penalty_spinBox.hide()
            self.L_nig_penalty_spinBox.hide()
            self.L_den_day_label.setEnabled( False )
            self.L_den_eve_label.setEnabled( False )
            self.L_den_nig_label.setEnabled( False )
            self.L_den_hours_label.setEnabled( False )
            self.L_den_eve_label_penalization.setEnabled( False )
            self.L_den_nig_label_penalization.setEnabled( False )
            # self.L_den_penalty_label.setEnabled( False )
            self.L_den_penalty_label.hide()
            self.L_den_checkBox.hide()


    def rays_checkBox_update(self):

        if self.rays_layer_checkBox.isChecked():
            self.rays_layer_pushButton.setEnabled( True )
        else:
            self.rays_layer_pushButton.setEnabled( False )


    def diff_rays_checkBox_update(self):

        if self.diff_rays_layer_checkBox.isChecked():
            self.diff_rays_layer_pushButton.setEnabled( True )
        else:
            self.diff_rays_layer_pushButton.setEnabled( False )

    def diff3D_rays_checkBox_update(self):

        if self.diff3DRaysCheck.isChecked():
            self.dif3Df_rays_layer_pushButton.setEnabled( True )
        else:
            self.dif3Df_rays_layer_pushButton.setEnabled( False )

    def skip_diffraction_checkBox_update(self):
        if self.skip_diffraction_checkBox.isChecked():
            #block create diffraction layer 2D
            self.diff_rays_layer_checkBox.setEnabled(False)
            self.diff_rays_layer_checkBox.setChecked(False)
            self.diff3DRaysCheck.setChecked(False)
            self.diff3DRaysCheck.setEnabled(False)
        #     block create diffraction layer 3D
            self.height_building_check.setChecked(False)
            self.height_building_check.setEnabled(False)
            self.field_height_building.setEnabled(False)
        else:
            self.diff_rays_layer_checkBox.setEnabled(True)
            self.diff3DRaysCheck.setEnabled(True)
            self.height_building_check.setEnabled(True)
            self.field_height_building.setEnabled(True)

    def outFile_rays(self):

        self.rays_layer_lineEdit.clear()
        shapefileName, __ = QFileDialog.getSaveFileName(None,'Open file', on_Settings.getOneSetting('directory_last') , "Shapefile (*.shp);;All files (*)")

        if shapefileName is None or shapefileName == "":
            return

        if str.find(shapefileName,".shp") == -1 and str.find(shapefileName,".SHP") == -1:
            self.rays_layer_lineEdit.setText( shapefileName + ".shp")
        else:
            self.rays_layer_lineEdit.setText( shapefileName)

        on_Settings.setOneSetting('directory_last',os.path.dirname(self.rays_layer_lineEdit.text()))


    def outFile_diff_rays(self):

        self.diff_rays_layer_lineEdit.clear()
        shapefileName, __ = QFileDialog.getSaveFileName(None,'Open file', on_Settings.getOneSetting('directory_last')  , "Shapefile (*.shp);;All files (*)")

        if shapefileName is None or shapefileName == "":
            return

        if str.find(shapefileName,".shp") == -1 and str.find(shapefileName,".SHP") == -1:
            self.diff_rays_layer_lineEdit.setText( shapefileName + ".shp")
        else:
            self.diff_rays_layer_lineEdit.setText( shapefileName)

        removeLayer(shapefileName)

        on_Settings.setOneSetting('directory_last',os.path.dirname(self.diff_rays_layer_lineEdit.text()))

    def outFile_diff3D_rays(self):
        self.diff3D_rays_layer_lineEdit.clear()
        shapefileName, __ = QFileDialog.getSaveFileName(None, 'Open file', on_Settings.getOneSetting('directory_last'),
                                                        "Shapefile (*.shp);;All files (*)")

        if shapefileName is None or shapefileName == "":
            return

        if str.find(shapefileName, ".shp") == -1 and str.find(shapefileName, ".SHP") == -1:
            self.diff3D_rays_layer_lineEdit.setText(shapefileName + ".shp")
        else:
            self.diff3D_rays_layer_lineEdit.setText(shapefileName)

        removeLayer(shapefileName)

        on_Settings.setOneSetting('directory_last',
                                  os.path.dirname(self.diff3D_rays_layer_lineEdit.text()))

    def check(self):

        # TAB Geometry
        if self.receivers_layer_comboBox.currentText() == "":
            QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("Please specify receiver points layer"))
            return False

        if self.sources_pts_layer_checkBox.isChecked() is False and self.sources_roads_layer_checkBox.isChecked() is False:
            QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("Please specify at least one source layer"))
            return False

        settings = on_Settings.getAllSettings()

        if self.sources_pts_layer_checkBox.isChecked():
            if self.sources_pts_layer_comboBox.currentText() == "":
                QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("Please specify the points sources layer"))
                return False
            if not (settings['period_pts_gen'] == 'True' or settings['period_pts_day'] == 'True' or settings['period_pts_eve'] == 'True' or settings['period_pts_nig'] == 'True'):
                QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("Please specify at least one power for a reference period in the point source"))
                return False
            if self.receivers_layer_comboBox.currentText() == self.sources_pts_layer_comboBox.currentText():
                QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("The receivers point layer and the source point layer are the same"))
                return False

        if self.sources_roads_layer_checkBox.isChecked():
            if self.sources_roads_layer_comboBox.currentText() == "":
                QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("Please specify the road source layer"))
                return False
            if not (settings['period_roads_gen'] == 'True' or settings['period_roads_day'] == 'True' or settings['period_roads_eve'] == 'True' or settings['period_roads_nig'] == 'True'):
                QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("Please specify at least one power for a reference period in the road source"))
                return False

        if self.height_receiver_check.isChecked() and self.field_height_receiver.currentText() == "":
            QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"),
                                    self.tr("Please specify elevation field for receiver points layer"))
            return False

        if self.height_building_check.isChecked() and self.field_height_building.currentText() == "":
            QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"),
                                    self.tr("Please specify elevation field for buildings layer"))
            return False


        if self.buildings_layer_checkBox.isChecked() == True and self.buildings_layer_comboBox.currentText() == "":
            QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("Please specify the buildings layer"))
            return False


        ## TAB Option
        if self.save_settings_checkBox.isChecked() and self.save_settings_lineEdit.text() == "":
            QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("Please specify a file to save current settings"))
            return False

        if  self.L_den_checkBox.isChecked() and int(self.L_day_hours_spinBox.value()) + int(self.L_eve_hours_spinBox.value()) + int(self.L_nig_hours_spinBox.value()) != 24:
            QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("In the Parameters section, to calculate Lden, the total amount of the hours of day, evening and night period must be 24"))
            return False


        if self.rays_layer_checkBox.isChecked() == True and self.rays_layer_lineEdit.text() == "":
            QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("Please specify the direct sound rays layer"))
            return False

        if self.diff_rays_layer_checkBox.isChecked() == True and self.diff_rays_layer_lineEdit.text() == "":
            QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("Please specify the diffracted vertical sound rays layer"))
            return False

        # check that 3d diffraction is activated when diffracted layers are outputted
        if self.diff3DRaysCheck.isChecked() == True and self.diff3D_rays_layer_lineEdit.text() == "":
            QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"),
                                    self.tr("Please specify the diffracted horizontal sound rays layer"))
            return False
        if self.diff3DRaysCheck.isChecked() == True and self.height_building_check.isChecked() == False:
            QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"),
                                    self.tr("Please activate the 3D global in Input tab"))
            return False

        if self.diff_rays_layer_checkBox.isChecked() == True and self.rays_layer_checkBox.isChecked() == True:
            if self.diff_rays_layer_lineEdit.text() == self.rays_layer_lineEdit.text():
                QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"),
                                        self.tr("Please use different name for the diffracted and rays layer"))
                return False

        # check old fields in receiver
        if self.check_oldFields() == False:
            return False

        return True


    def check_oldFields(self):
        receiver_layer = self.receivers_layer_comboBox.currentLayer()
        receiver_fields = receiver_layer.fields()
        fields = [x.name() for x in receiver_fields.toList()]

        # get period to calculate
        settings = on_Settings.getAllSettings()
        fields_to_calculate = []

        if self.sources_pts_layer_checkBox.isChecked():
            if settings['period_pts_gen'] == 'True':
                fields_to_calculate.append('Lgeneric')
            if settings['period_pts_day'] == 'True':
                fields_to_calculate.append('Lday')
            if settings['period_pts_eve'] == 'True':
                fields_to_calculate.append('Levening')
            if settings['period_pts_nig'] == 'True':
                fields_to_calculate.append('Lnight')

        if self.sources_roads_layer_checkBox.isChecked():
            if settings['period_roads_gen'] == 'True':
                fields_to_calculate.append('Lgeneric')
            if settings['period_roads_day'] == 'True':
                fields_to_calculate.append('Lday')
            if settings['period_roads_eve'] == 'True':
                fields_to_calculate.append('Levening')
            if settings['period_roads_nig'] == 'True':
                fields_to_calculate.append('Lnight')

        if ('Lday' in fields_to_calculate) and ('Levening' in fields_to_calculate) and ('Lnight' in fields_to_calculate):
            fields_to_calculate.append('Lden')

        #print("fields_to_calculate",fields_to_calculate)
        #personal_fields = ['Lgeneric', 'Lday', 'Levening', 'Lnight','Lden']
        fields_already_present = list(set(fields_to_calculate) & set(fields))
        if fields_already_present:
            overwrite_begin = self.tr("In the receivers point layer the following fields already exist: ")
            overwrite_end = self.tr(" . Do you want to overwrite them?")
            reply = QMessageBox.question(self, self.tr("opeNoise - Calculate Noise Levels"),
                                           overwrite_begin + '\n' + str(fields_already_present) + overwrite_end, QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.No:
                reply2 = QMessageBox.question(self, self.tr("opeNoise - Calculate Noise Levels"),
                                               self.tr("To mantain old data, copy them in a new field"), QMessageBox.Ok)
                return False
            else:
                fList = []
                for field_to_delete in fields_already_present:
                    idx_field = receiver_layer.dataProvider().fieldNameIndex(field_to_delete)
                    fList.append(idx_field)

                receiver_layer.dataProvider().deleteAttributes(fList)
                receiver_layer.updateFields()
                return True
        else:
            return True


    def CRS_check(self):

        self.receiver_layer = QgsProject.instance().mapLayersByName(self.receivers_layer_comboBox.currentText())[0]

        if self.sources_pts_layer_checkBox.isChecked() and self.sources_pts_layer_comboBox.currentText() != "":
            self.sources_pts_layer = QgsProject.instance().mapLayersByName(self.sources_pts_layer_comboBox.currentText())[0]
            # check that is used a projected CRS
            if self.sources_pts_layer.crs().isGeographic():
                QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr(
                    "The source layer have to use a projected CRS (Coordinate Reference System)"))
                return False

            if self.sources_pts_layer.crs().authid() != self.receiver_layer.crs().authid():
                QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("The receivers and the points sources layers don't have the same CRS (Coordinate Reference System). Please use layers with same CRS"))
                return False

        if self.sources_roads_layer_checkBox.isChecked() and self.sources_roads_layer_comboBox.currentText() != "":
            self.sources_roads_layer = QgsProject.instance().mapLayersByName(self.sources_roads_layer_comboBox.currentText())[0]

            if self.sources_roads_layer.crs().isGeographic():
                QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr(
                    "The source layer have to use a projected CRS (Coordinate Reference System)"))
                return False

            if self.sources_roads_layer.crs().authid() != self.receiver_layer.crs().authid():
                QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("The receivers and the road sources layers don't have the same CRS (Coordinate Reference System). Please use layers with same CRS"))
                return False

        if self.buildings_layer_checkBox.isChecked() and self.buildings_layer_comboBox.currentText() != "":
            self.buildings_layer = QgsProject.instance().mapLayersByName(self.buildings_layer_comboBox.currentText())[0]

            if self.buildings_layer.crs().isGeographic():
                QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr(
                    "The building layer have to use a projected CRS (Coordinate Reference System)"))
                return False

            if self.receiver_layer.crs().authid() != self.buildings_layer.crs().authid():
                QMessageBox.information(self, self.tr("opeNoise - Road Source Calculation"), self.tr("The receivers and buildings layers don't have the same CRS (Coordinate Reference System). Please use layers with same CRS"))
                return False

        return True


    def write_settings(self):


        settings = {}


        # receivers
        settings['receivers_name'] = self.receiver_layer.name()
        settings['receivers_path'] = self.receiver_layer.source()

        # custom 3D
        if self.height_receiver_check.isChecked():
            settings['custom3d'] = 'True'
            settings['custom3dfield'] = self.field_height_receiver.currentText()
        else:
            settings['custom3d'] = 'False'
            settings['custom3dfield'] =''

        if self.sources_pts_layer_checkBox.isChecked() == True:
            settings['sources_pts_name'] = self.sources_pts_layer.name()
            settings['sources_pts_path'] = self.sources_pts_layer.source()
        else:
            settings['sources_pts_name'] = None
            settings['sources_pts_path'] = None
            on_Settings.clearPtsEmissionSettings()

        if self.sources_roads_layer_checkBox.isChecked() == True:
            settings['sources_roads_name'] = self.sources_roads_layer.name()
            settings['sources_roads_path'] = self.sources_roads_layer.source()
        else:
            settings['sources_roads_name'] = None
            settings['sources_roads_path'] = None
            on_Settings.clearRoadsEmissionSettings()

        # buildings
        if self.buildings_layer_checkBox.isChecked():
            settings['buildings_name'] = self.buildings_layer.name()
            settings['buildings_path'] = self.buildings_layer.source()
        else:
            settings['buildings_name'] = None
            settings['buildings_path'] = None

        # skip diffraction
        if self.skip_diffraction_checkBox.isChecked():
            settings['skip_diffraction'] = 'True'
        else:
            settings['skip_diffraction'] = 'False'

        # save emission value in input road layer
        if self.saveEmissionCheckBox.isChecked():
            settings['save_emission'] = 'True'
        else:
            settings['save_emission'] = 'False'

        # TAB option
        settings['research_ray'] = self.research_ray_comboBox.currentText()
        settings['temperature'] = self.temperature_comboBox.currentText()
        settings['humidity'] = self.humidity_comboBox.currentText()

        if self.L_den_checkBox.isChecked():
            settings['period_den'] = 'True'
            settings['day_hours'] = str(self.L_day_hours_spinBox.value())
            settings['eve_hours'] = str(self.L_eve_hours_spinBox.value())
            settings['nig_hours'] = str(self.L_nig_hours_spinBox.value())
            settings['day_penalty'] = str(self.L_day_penalty_spinBox.value())
            settings['eve_penalty'] = str(self.L_eve_penalty_spinBox.value())
            settings['nig_penalty'] = str(self.L_nig_penalty_spinBox.value())
        else:
            settings['period_den'] = 'False'

        if self.rays_layer_checkBox.isChecked():
            settings['rays_path'] = self.rays_layer_lineEdit.text()
            removeLayer(settings['rays_path'])
        else:
            settings['rays_path'] = ''
        if self.diff_rays_layer_checkBox.isChecked():

            settings['diff_rays_path'] = self.diff_rays_layer_lineEdit.text()
            removeLayer(settings['diff_rays_path'])
        else:
            settings['diff_rays_path'] = ''

        if self.diff3DRaysCheck.isChecked():
            settings['diff3D_rays_path'] = self.diff3D_rays_layer_lineEdit.text()
            removeLayer(settings['diff3D_rays_path'])
        else:
            settings['diff3D_rays_path'] = ''

        # 3D Settings
        if self.height_receiver_check.isChecked():
            settings['height_receiver'] = 'True'
            settings['height_receiver'] = 'True'
        else:
            settings['height_receiver'] = 'False'

        if self.height_building_check.isChecked():
            settings['threedglobal'] = 'True'
            settings['field3D'] = self.field_height_building.currentText()
        else:
            settings['threedglobal'] = 'False'
            settings['field3D'] = ''
        if self.diff3DRaysCheck.isChecked():
            settings['threedglobal_rays'] = 'True'
        else:
            settings['threedglobal_rays'] = 'False'

        on_Settings.setSettings(settings)

        on_Settings.copySettingsToLastSettings()

        if self.save_settings_checkBox.isChecked():
            on_Settings.copySettingsToSavedSettings(self.save_settings_lineEdit.text())




    def reload_settings(self):

        settings = on_Settings.getAllSettings()


        if len(list(QgsProject.instance().mapLayers().values())) > 0:
            self.populateLayersReceiver()
            self.populateLayersSourcePts()
            self.populateLayersSourceRoads()


        try:
            # receivers
            idx = self.receivers_layer_comboBox.findText(settings['receivers_name'])
            self.receivers_layer_comboBox.setCurrentIndex(idx)

            # sources
            if settings['implementation_pts'] is not None:
                self.sources_pts_layer_checkBox.setEnabled(True)
                self.sources_pts_layer_checkBox.setChecked(True)
                idx = self.sources_pts_layer_comboBox.findText(settings['sources_pts_name'])
                self.sources_pts_layer_comboBox.setCurrentIndex(idx)
            else:
                self.sources_pts_layer_checkBox.setChecked(False)

            # custom 3d
            if settings['custom3d'] == "True":
                self.height_receiver_check.setChecked(1)
                self.field_height_receiver.setEnabled(True)
                self.field_height_receiver.setField(settings['custom3dfield'])


            if settings['implementation_roads'] is not None:
                self.sources_roads_layer_checkBox.setEnabled(True)
                self.sources_roads_layer_checkBox.setChecked(True)
                idx = self.sources_roads_layer_comboBox.findText(settings['sources_roads_name'])
                self.sources_roads_layer_comboBox.setCurrentIndex(idx)
            else:
                self.sources_roads_layer_checkBox.setChecked(False)

            self.sources_checkBox_update()


            # buildings
            if settings['buildings_path'] is not None:
                self.buildings_layer_checkBox.setChecked(1)
                self.buildings_layer_comboBox.setEnabled(True)
                self.buildings_layer_label.setEnabled(True)
                self.buildings_layer_label2.setEnabled(True)
                idx = self.buildings_layer_comboBox.findText(settings['buildings_name'])
                self.buildings_layer_comboBox.setCurrentIndex(idx)

            #skip diffraction
            if settings['skip_diffraction'] == "True":
                self.skip_diffraction_checkBox.setChecked(1)
                self.diff_rays_layer_checkBox.setEnabled(False)

            # save emission in input layer
            if settings['save_emission'] == "True":
                self.saveEmissionCheckBox.setChecked(1)

            # 3D setting
            if settings['threedglobal'] == "True":
                self.height_building_check.setChecked(1)
                self.field_height_building.setEnabled(True)
                self.field_height_building.setField(settings['field3D'])


            # research ray
            idx = self.research_ray_comboBox.findText(settings['research_ray'])
            self.research_ray_comboBox.setCurrentIndex(idx)
            # temperature
            idx = self.temperature_comboBox.findText(settings['temperature'])
            self.temperature_comboBox.setCurrentIndex(idx)
            # humidity
            idx = self.humidity_comboBox.findText(settings['humidity'])
            self.humidity_comboBox.setCurrentIndex(idx)

            if settings['period_den'] == "True":
                    self.L_den_checkBox.setChecked(1)
                    self.L_den_checkBox.setEnabled(True)
                    self.L_day_hours_spinBox.setValue(int(settings['day_hours']))
                    self.L_eve_hours_spinBox.setValue(int(settings['eve_hours']))
                    self.L_nig_hours_spinBox.setValue(int(settings['nig_hours']))
                    self.L_day_penalty_spinBox.setValue(int(settings['day_penalty']))
                    self.L_eve_penalty_spinBox.setValue(int(settings['eve_penalty']))
                    self.L_nig_penalty_spinBox.setValue(int(settings['nig_penalty']))

            # rays
            if settings['rays_path'] is not None:
                self.rays_layer_checkBox.setChecked(1)
                self.rays_layer_lineEdit.setText(settings['rays_path'])
                removeLayer(settings['rays_path'])
            else:
                self.rays_layer_checkBox.setChecked(0)
                self.rays_layer_lineEdit.clear()

            if settings['diff_rays_path'] is not None:
                self.diff_rays_layer_checkBox.setChecked(1)
                self.diff_rays_layer_lineEdit.setText(settings['diff_rays_path'])
                removeLayer(settings['diff_rays_path'])
            else:
                self.diff_rays_layer_checkBox.setChecked(0)
                self.diff_rays_layer_lineEdit.clear()

            if settings['diff3D_rays_path'] is not None:
                self.diff3DRaysCheck.setChecked(1)
                self.diff3D_rays_layer_lineEdit.setText(settings['diff3D_rays_path'])
                removeLayer(settings['diff3D_rays_path'])
            else:
                self.diff3DRaysCheck.setChecked(0)
                self.diff3D_rays_layer_lineEdit.clear()

        except:
            QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("Sorry, but somethigs wrong in import last settings"))


    def reload_last_settings(self):

        on_Settings.copyLastSettingsToSettings()
        self.reload_settings()


    def reload_saved_settings(self):

        saved_settings, __ = QFileDialog.getOpenFileName(None,'Open file', on_Settings.getOneSetting('directory_last') , "Settings (*.xml);;All files (*)")

        if saved_settings is None or saved_settings == "":
            return

        try:
            on_Settings.copySavedSettingsToSettings(saved_settings)
            self.reload_settings()

        except:
            QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("Sorry, but somethigs wrong in import saved settings"))

    def save_settings_checkBox_update(self):

        if self.save_settings_checkBox.isChecked():
            self.save_settings_pushButton.setEnabled( True )
        else:
            self.save_settings_pushButton.setEnabled( False )

    def outFile_save_settings(self):

        self.save_settings_lineEdit.clear()
        save_settings_path, __ = QFileDialog.getSaveFileName(None,'Open file', on_Settings.getOneSetting('directory_last') , "Settings (*.xml);;All files (*)")

        if save_settings_path is None or save_settings_path == "":
            return

        if str.find(save_settings_path,".xml") == -1 and str.find(save_settings_path,".XML") == -1:
            self.save_settings_lineEdit.setText( save_settings_path + ".xml")
        else:
            self.save_settings_lineEdit.setText( save_settings_path )


        on_Settings.setOneSetting('directory_last',os.path.dirname(self.save_settings_lineEdit.text()))

    def log_start(self):

        global log_errors, log_errors_path_name
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        log_errors_path_name = os.path.join(dir_path,"log_CalculateNoiseLevels_errors.txt")
        log_errors = open(log_errors_path_name,"w")
        log_errors.write(self.tr("opeNoise") + " - " + self.tr("Calculate Noise Levels") + " - " + self.tr("Errors") + "\n\n")


    def log_end(self):

        log_errors.close()


    def duration(self):
        duration = self.time_end - self.time_start
        duration_h = duration.seconds // 3600
        duration_m = (duration.seconds // 60) % 60
        duration_s = duration.seconds
        duration_string = str(format(duration_h, '02')) + ':' + str(format(duration_m, '02')) + ':' + str(
            format(duration_s, '02'))
        return duration_string



    def accept(self):

        if self.check() == False:
            return

        if self.CRS_check() == False:
            return

        if self.diff_rays_layer_checkBox.isChecked():
            skip_diff = True
        else:
            skip_diff = False

        self.calculate_pushButton.setEnabled(False)
        self.label_time_start.setText('')
        self.label_time_end.setText('')
        self.label_time_duration.setText('')

        self.log_start()
        self.time_start = datetime.now()
        # fix_print_with_import
        print('###################################################')

        self.write_settings()

        settings = on_Settings.getAllSettings()

        try:
            on_CalculateNoiseLevels.run(settings,self.progress_bars,self.totalBar)
            run = 1
        except:
            error= traceback.format_exc()
            log_errors.write(error)
            run = 0

        self.time_end = datetime.now()

        if run == 1:
            log_errors.write(self.tr("No errors.") + "\n\n")

            self.label_time_start.setText(self.tr("Start: ") + ' ' + self.time_start.strftime("%a %d/%b/%Y %H:%M:%S"))
            self.label_time_end.setText(self.tr("End: ") + ' ' + self.time_end.strftime("%a %d/%b/%Y %H:%M:%S"))
            self.label_time_duration.setText(self.tr("Duration: ") + ' ' + str(self.duration()))

            result_string = self.tr("The calculation results have been successfully saved into the receivers point layer."
                                    "The results are expressed in dB(A)") + "\n\n" +\
                            self.tr("Start: ") + self.time_start.strftime("%a %d/%b/%Y %H:%M:%S") + "\n" +\
                            self.tr("End: ") + self.time_end.strftime("%a %d/%b/%Y %H:%M:%S") + "\n"+\
                            self.tr("Duration: ") + str(self.duration())
            QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), result_string)

        else:

            result_string = self.tr("Sorry, process not complete.") + "\n\n" +\
                            self.tr("View the log file to understand the problem:") + "\n" +\
                            str(log_errors_path_name) + "\n\n" +\
                            self.tr("Start: ") + self.time_start.strftime("%a %d/%b/%Y %H:%M:%S.%f") + "\n" +\
                            self.tr("End: ") + self.time_end.strftime("%a %d/%b/%Y %H:%M:%S.%f") + "\n"+\
                            self.tr("Duration: ") + str(self.duration())
            QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr(result_string))

        # fix_print_with_import
        print(self.duration())
        # fix_print_with_import
        print('###################################################')
        # fix_print_with_import
        print('\n')
        self.log_end()

        self.calculate_pushButton.setEnabled(True)
        self.close()
