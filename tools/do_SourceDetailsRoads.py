# -*- coding: utf-8 -*-
"""
/***************************************************************************
 opeNoise

 Qgis Plugin to compute noise levels

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

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.core import *

import os, imp
import traceback

from ui_SourceDetailsRoads import Ui_SourceDetailsRoads_window

import on_Settings


# import VectorWriter
try:
    # Qgis from 2.0 to 2.4
    from processing.core.VectorWriter import VectorWriter
except:
    # Qgis from 2.6
    from processing.tools.vector import VectorWriter


class Dialog(QDialog,Ui_SourceDetailsRoads_window):
    
    def __init__(self, iface,layer_name):
        QDialog.__init__(self, iface.mainWindow())
        self.iface = iface
        # Set up the user interface from Designer.
        self.setupUi(self)
        
        self.layer_name = layer_name

        # start definition
        self.POWER_R_emission_comboBoxes_dict = {
                                            'POWER_R_gen' : self.POWER_R_L_gen_comboBox, 
                                            'POWER_R_day' : self.POWER_R_L_day_comboBox,
                                            'POWER_R_eve' : self.POWER_R_L_eve_comboBox,
                                            'POWER_R_nig' : self.POWER_R_L_nig_comboBox
                                            }
        self.NMPB_emission_comboBoxes_dict = {'NMPB_gen_l_n' : self.NMPB_L_gen_l_n_comboBox,
                                            'NMPB_day_l_n' : self.NMPB_L_day_l_n_comboBox,
                                            'NMPB_eve_l_n' : self.NMPB_L_eve_l_n_comboBox,
                                            'NMPB_nig_l_n' : self.NMPB_L_nig_l_n_comboBox,
                                            'NMPB_gen_l_s' : self.NMPB_L_gen_l_s_comboBox,
                                            'NMPB_day_l_s' : self.NMPB_L_day_l_s_comboBox,
                                            'NMPB_eve_l_s' : self.NMPB_L_eve_l_s_comboBox,
                                            'NMPB_nig_l_s' : self.NMPB_L_nig_l_s_comboBox,
                                            'NMPB_gen_h_n' : self.NMPB_L_gen_h_n_comboBox,
                                            'NMPB_day_h_n' : self.NMPB_L_day_h_n_comboBox,
                                            'NMPB_eve_h_n' : self.NMPB_L_eve_h_n_comboBox,
                                            'NMPB_nig_h_n' : self.NMPB_L_nig_h_n_comboBox,
                                            'NMPB_gen_h_s' : self.NMPB_L_gen_h_s_comboBox,
                                            'NMPB_day_h_s' : self.NMPB_L_day_h_s_comboBox,
                                            'NMPB_eve_h_s' : self.NMPB_L_eve_h_s_comboBox,
                                            'NMPB_nig_h_s' : self.NMPB_L_nig_h_s_comboBox,
                                            'NMPB_gen_type' : self.NMPB_L_gen_type_comboBox,
                                            'NMPB_day_type' : self.NMPB_L_day_type_comboBox,
                                            'NMPB_eve_type' : self.NMPB_L_eve_type_comboBox,
                                            'NMPB_nig_type' : self.NMPB_L_nig_type_comboBox,
                                            'NMPB_slope' : self.NMPB_slope_comboBox,
                                            'NMPB_surface' : self.NMPB_surface_comboBox
                                            }
        self.CNOSSOS_emission_comboBoxes_dict = {'CNOSSOS_gen_1_n' : self.CNOSSOS_L_gen_1_n_comboBox,
                                            'CNOSSOS_day_1_n' : self.CNOSSOS_L_day_1_n_comboBox,
                                            'CNOSSOS_eve_1_n' : self.CNOSSOS_L_eve_1_n_comboBox,
                                            'CNOSSOS_nig_1_n' : self.CNOSSOS_L_nig_1_n_comboBox,
                                            'CNOSSOS_gen_1_s' : self.CNOSSOS_L_gen_1_s_comboBox,
                                            'CNOSSOS_day_1_s' : self.CNOSSOS_L_day_1_s_comboBox,
                                            'CNOSSOS_eve_1_s' : self.CNOSSOS_L_eve_1_s_comboBox,
                                            'CNOSSOS_nig_1_s' : self.CNOSSOS_L_nig_1_s_comboBox,
                                            'CNOSSOS_gen_2_n' : self.CNOSSOS_L_gen_2_n_comboBox,
                                            'CNOSSOS_day_2_n' : self.CNOSSOS_L_day_2_n_comboBox,
                                            'CNOSSOS_eve_2_n' : self.CNOSSOS_L_eve_2_n_comboBox,
                                            'CNOSSOS_nig_2_n' : self.CNOSSOS_L_nig_2_n_comboBox,
                                            'CNOSSOS_gen_2_s' : self.CNOSSOS_L_gen_2_s_comboBox,
                                            'CNOSSOS_day_2_s' : self.CNOSSOS_L_day_2_s_comboBox,
                                            'CNOSSOS_eve_2_s' : self.CNOSSOS_L_eve_2_s_comboBox,
                                            'CNOSSOS_nig_2_s' : self.CNOSSOS_L_nig_2_s_comboBox,
                                            'CNOSSOS_gen_3_n' : self.CNOSSOS_L_gen_3_n_comboBox,
                                            'CNOSSOS_day_3_n' : self.CNOSSOS_L_day_3_n_comboBox,
                                            'CNOSSOS_eve_3_n' : self.CNOSSOS_L_eve_3_n_comboBox,
                                            'CNOSSOS_nig_3_n' : self.CNOSSOS_L_nig_3_n_comboBox,
                                            'CNOSSOS_gen_3_s' :  self.CNOSSOS_L_gen_3_s_comboBox,
                                            'CNOSSOS_day_3_s' : self.CNOSSOS_L_day_3_s_comboBox,
                                            'CNOSSOS_eve_3_s' : self.CNOSSOS_L_eve_3_s_comboBox,
                                            'CNOSSOS_nig_3_s' : self.CNOSSOS_L_nig_3_s_comboBox,
                                            'CNOSSOS_gen_4a_n' : self.CNOSSOS_L_gen_4a_n_comboBox,
                                            'CNOSSOS_day_4a_n' : self.CNOSSOS_L_day_4a_n_comboBox,
                                            'CNOSSOS_eve_4a_n' : self.CNOSSOS_L_eve_4a_n_comboBox,
                                            'CNOSSOS_nig_4a_n' : self.CNOSSOS_L_nig_4a_n_comboBox,
                                            'CNOSSOS_gen_4a_s' : self.CNOSSOS_L_gen_4a_s_comboBox,
                                            'CNOSSOS_day_4a_s' : self.CNOSSOS_L_day_4a_s_comboBox,
                                            'CNOSSOS_eve_4a_s' : self.CNOSSOS_L_eve_4a_s_comboBox,
                                            'CNOSSOS_nig_4a_s' : self.CNOSSOS_L_nig_4a_s_comboBox,
                                            'CNOSSOS_gen_4b_n' : self.CNOSSOS_L_gen_4b_n_comboBox,
                                            'CNOSSOS_day_4b_n' : self.CNOSSOS_L_day_4b_n_comboBox,
                                            'CNOSSOS_eve_4b_n' : self.CNOSSOS_L_eve_4b_n_comboBox,
                                            'CNOSSOS_nig_4b_n' : self.CNOSSOS_L_nig_4b_n_comboBox,
                                            'CNOSSOS_gen_4b_s' : self.CNOSSOS_L_gen_4b_s_comboBox,
                                            'CNOSSOS_day_4b_s' : self.CNOSSOS_L_day_4b_s_comboBox,
                                            'CNOSSOS_eve_4b_s' : self.CNOSSOS_L_eve_4b_s_comboBox,
                                            'CNOSSOS_nig_4b_s' : self.CNOSSOS_L_nig_4b_s_comboBox,
                                            'CNOSSOS_slope' : self.CNOSSOS_slope_comboBox,
                                            'CNOSSOS_surface' : self.CNOSSOS_surface_comboBox
                                            }

        self.all_emission_comboBoxes = [self.POWER_R_L_gen_comboBox, self.POWER_R_L_day_comboBox, self.POWER_R_L_eve_comboBox, self.POWER_R_L_nig_comboBox,
                      self.NMPB_L_gen_l_n_comboBox,self.NMPB_L_day_l_n_comboBox,self.NMPB_L_eve_l_n_comboBox,self.NMPB_L_nig_l_n_comboBox,
                      self.NMPB_L_gen_l_s_comboBox,self.NMPB_L_day_l_s_comboBox,self.NMPB_L_eve_l_s_comboBox,self.NMPB_L_nig_l_s_comboBox,
                      self.NMPB_L_gen_h_n_comboBox,self.NMPB_L_day_h_n_comboBox,self.NMPB_L_eve_h_n_comboBox,self.NMPB_L_nig_h_n_comboBox,
                      self.NMPB_L_gen_h_s_comboBox,self.NMPB_L_day_h_s_comboBox,self.NMPB_L_eve_h_s_comboBox,self.NMPB_L_nig_h_s_comboBox,
                      self.NMPB_L_gen_type_comboBox,self.NMPB_L_day_type_comboBox,self.NMPB_L_eve_type_comboBox,self.NMPB_L_nig_type_comboBox,
                      self.NMPB_slope_comboBox, self.NMPB_surface_comboBox,
                      self.CNOSSOS_L_gen_1_n_comboBox,self.CNOSSOS_L_day_1_n_comboBox,self.CNOSSOS_L_eve_1_n_comboBox,self.CNOSSOS_L_nig_1_n_comboBox,
                      self.CNOSSOS_L_gen_1_s_comboBox,self.CNOSSOS_L_day_1_s_comboBox,self.CNOSSOS_L_eve_1_s_comboBox,self.CNOSSOS_L_nig_1_s_comboBox,
                      self.CNOSSOS_L_gen_2_n_comboBox,self.CNOSSOS_L_day_2_n_comboBox,self.CNOSSOS_L_eve_2_n_comboBox,self.CNOSSOS_L_nig_2_n_comboBox,
                      self.CNOSSOS_L_gen_2_s_comboBox,self.CNOSSOS_L_day_2_s_comboBox,self.CNOSSOS_L_eve_2_s_comboBox,self.CNOSSOS_L_nig_2_s_comboBox,
                      self.CNOSSOS_L_gen_3_n_comboBox,self.CNOSSOS_L_day_3_n_comboBox,self.CNOSSOS_L_eve_3_n_comboBox,self.CNOSSOS_L_nig_3_n_comboBox,
                      self.CNOSSOS_L_gen_3_s_comboBox,self.CNOSSOS_L_day_3_s_comboBox,self.CNOSSOS_L_eve_3_s_comboBox,self.CNOSSOS_L_nig_3_s_comboBox,
                      self.CNOSSOS_L_gen_4a_n_comboBox,self.CNOSSOS_L_day_4a_n_comboBox,self.CNOSSOS_L_eve_4a_n_comboBox,self.CNOSSOS_L_nig_4a_n_comboBox,
                      self.CNOSSOS_L_gen_4a_s_comboBox,self.CNOSSOS_L_day_4a_s_comboBox,self.CNOSSOS_L_eve_4a_s_comboBox,self.CNOSSOS_L_nig_4a_s_comboBox,
                      self.CNOSSOS_L_gen_4b_n_comboBox,self.CNOSSOS_L_day_4b_n_comboBox,self.CNOSSOS_L_eve_4b_n_comboBox,self.CNOSSOS_L_nig_4b_n_comboBox,
                      self.CNOSSOS_L_gen_4b_s_comboBox,self.CNOSSOS_L_day_4b_s_comboBox,self.CNOSSOS_L_eve_4b_s_comboBox,self.CNOSSOS_L_nig_4b_s_comboBox,
                      self.CNOSSOS_slope_comboBox, self.CNOSSOS_surface_comboBox
                      ]           

                     
        self.source_checkBoxes = [self.POWER_R_L_gen_checkBox,self.POWER_R_L_day_checkBox,self.POWER_R_L_eve_checkBox,self.POWER_R_L_nig_checkBox,
                           self.NMPB_L_gen_checkBox,self.NMPB_L_day_checkBox,self.NMPB_L_eve_checkBox,self.NMPB_L_nig_checkBox,
                           self.NMPB_l_checkBox,self.NMPB_h_checkBox,
                           self.CNOSSOS_L_gen_checkBox,self.CNOSSOS_L_day_checkBox,self.CNOSSOS_L_eve_checkBox,self.CNOSSOS_L_nig_checkBox,
                           self.CNOSSOS_1_checkBox,self.CNOSSOS_2_checkBox,self.CNOSSOS_3_checkBox,self.CNOSSOS_4a_checkBox,self.CNOSSOS_4b_checkBox]

        self.source_POWER_R_period_checkBoxes = [self.POWER_R_L_day_checkBox,self.POWER_R_L_eve_checkBox,self.POWER_R_L_nig_checkBox]
        self.source_NMPB_period_checkBoxes = [self.NMPB_L_day_checkBox,self.NMPB_L_eve_checkBox,self.NMPB_L_nig_checkBox]
        self.source_CNOSSOS_period_checkBoxes = [self.CNOSSOS_L_day_checkBox,self.CNOSSOS_L_eve_checkBox,self.CNOSSOS_L_nig_checkBox]
        # end definitions
    
        self.road_stackedWidget.setCurrentIndex(0)
        
        self.source_fields_update()
        
        self.POWER_R_radioButton.setChecked(0)
        self.NMPB_radioButton.setChecked(0)
        self.CNOSSOS_radioButton.setChecked(0)
        
        QObject.connect(self.POWER_R_radioButton, SIGNAL("toggled(bool)"), self.road_stackedWidget_update)
        QObject.connect(self.NMPB_radioButton, SIGNAL("toggled(bool)"), self.road_stackedWidget_update)
        QObject.connect(self.CNOSSOS_radioButton, SIGNAL("toggled(bool)"), self.road_stackedWidget_update)

        for source_checkBox in self.source_checkBoxes:
            source_checkBox.setChecked(0)
            QObject.connect(source_checkBox, SIGNAL("toggled(bool)"), self.source_checkBox_update)
            
        self.setToolTips()

        self.reload_settings()


    def road_stackedWidget_update( self ):
        
        if self.POWER_R_radioButton.isChecked():
            self.road_stackedWidget.setCurrentIndex(0)
        if self.NMPB_radioButton.isChecked():
            self.road_stackedWidget.setCurrentIndex(1)
        if self.CNOSSOS_radioButton.isChecked():
            self.road_stackedWidget.setCurrentIndex(2)
        
        self.source_checkBox_update()


    def source_fields_update(self):
        
        source_layer = QgsMapLayerRegistry.instance().mapLayersByName(self.layer_name)[0]
        source_layer_fields = list(source_layer.dataProvider().fields())

        source_layer_fields_labels = [""]

        for f in source_layer_fields:
#            if f.type() == QVariant.Int or f.type() == QVariant.Double:         
                source_layer_fields_labels.append(unicode(f.name()))
        
        
        for comboBox in self.all_emission_comboBoxes:
            comboBox.clear()
            comboBox.setEnabled(False)
        
            for label in source_layer_fields_labels:
                comboBox.addItem(label)


    def source_checkBox_update(self):
       
        # POWER_R
        if self.POWER_R_L_gen_checkBox.isChecked():
            self.POWER_R_L_gen_comboBox.setEnabled(True)    
        else:
            self.POWER_R_L_gen_comboBox.setEnabled(False)    
        if self.POWER_R_L_day_checkBox.isChecked():
            self.POWER_R_L_day_comboBox.setEnabled(True)    
        else:
            self.POWER_R_L_day_comboBox.setEnabled(False)    
        if self.POWER_R_L_eve_checkBox.isChecked():
            self.POWER_R_L_eve_comboBox.setEnabled(True)    
        else:
            self.POWER_R_L_eve_comboBox.setEnabled(False)    
        if self.POWER_R_L_nig_checkBox.isChecked():
            self.POWER_R_L_nig_comboBox.setEnabled(True)    
        else:
            self.POWER_R_L_nig_comboBox.setEnabled(False)    
        
        # NMPB
        if self.NMPB_l_checkBox.isChecked() and self.NMPB_L_gen_checkBox.isChecked():
            self.NMPB_L_gen_l_n_comboBox.setEnabled(True)    
            self.NMPB_L_gen_l_s_comboBox.setEnabled(True) 
        else:
            self.NMPB_L_gen_l_n_comboBox.setEnabled(False)    
            self.NMPB_L_gen_l_s_comboBox.setEnabled(False)    
        if self.NMPB_l_checkBox.isChecked() and self.NMPB_L_day_checkBox.isChecked():
            self.NMPB_L_day_l_n_comboBox.setEnabled(True)    
            self.NMPB_L_day_l_s_comboBox.setEnabled(True)    
        else:
            self.NMPB_L_day_l_n_comboBox.setEnabled(False)    
            self.NMPB_L_day_l_s_comboBox.setEnabled(False)
        if self.NMPB_l_checkBox.isChecked() and self.NMPB_L_eve_checkBox.isChecked():
            self.NMPB_L_eve_l_n_comboBox.setEnabled(True)    
            self.NMPB_L_eve_l_s_comboBox.setEnabled(True)    
        else:
            self.NMPB_L_eve_l_n_comboBox.setEnabled(False)    
            self.NMPB_L_eve_l_s_comboBox.setEnabled(False)
        if self.NMPB_l_checkBox.isChecked() and self.NMPB_L_nig_checkBox.isChecked():
            self.NMPB_L_nig_l_n_comboBox.setEnabled(True)    
            self.NMPB_L_nig_l_s_comboBox.setEnabled(True)    
        else:
            self.NMPB_L_nig_l_n_comboBox.setEnabled(False)    
            self.NMPB_L_nig_l_s_comboBox.setEnabled(False)    

        if self.NMPB_h_checkBox.isChecked() and self.NMPB_L_gen_checkBox.isChecked():
            self.NMPB_L_gen_h_n_comboBox.setEnabled(True)    
            self.NMPB_L_gen_h_s_comboBox.setEnabled(True)    
        else:
            self.NMPB_L_gen_h_n_comboBox.setEnabled(False)    
            self.NMPB_L_gen_h_s_comboBox.setEnabled(False)    
        if self.NMPB_h_checkBox.isChecked() and self.NMPB_L_day_checkBox.isChecked():
            self.NMPB_L_day_h_n_comboBox.setEnabled(True)    
            self.NMPB_L_day_h_s_comboBox.setEnabled(True)    
        else:
            self.NMPB_L_day_h_n_comboBox.setEnabled(False)    
            self.NMPB_L_day_h_s_comboBox.setEnabled(False)
        if self.NMPB_h_checkBox.isChecked() and self.NMPB_L_eve_checkBox.isChecked():
            self.NMPB_L_eve_h_n_comboBox.setEnabled(True)    
            self.NMPB_L_eve_h_s_comboBox.setEnabled(True)    
        else:
            self.NMPB_L_eve_h_n_comboBox.setEnabled(False)    
            self.NMPB_L_eve_h_s_comboBox.setEnabled(False)
        if self.NMPB_h_checkBox.isChecked() and self.NMPB_L_nig_checkBox.isChecked():
            self.NMPB_L_nig_h_n_comboBox.setEnabled(True)    
            self.NMPB_L_nig_h_s_comboBox.setEnabled(True)    
        else:
            self.NMPB_L_nig_h_n_comboBox.setEnabled(False)    
            self.NMPB_L_nig_h_s_comboBox.setEnabled(False) 
            
        if self.NMPB_L_gen_checkBox.isChecked():            
            self.NMPB_L_gen_type_comboBox.setEnabled(True)
        else:
            self.NMPB_L_gen_type_comboBox.setEnabled(False)
        if self.NMPB_L_day_checkBox.isChecked():            
            self.NMPB_L_day_type_comboBox.setEnabled(True)
        else:
            self.NMPB_L_day_type_comboBox.setEnabled(False)
        if self.NMPB_L_eve_checkBox.isChecked():            
            self.NMPB_L_eve_type_comboBox.setEnabled(True)
        else:
            self.NMPB_L_eve_type_comboBox.setEnabled(False)
        if self.NMPB_L_nig_checkBox.isChecked():            
            self.NMPB_L_nig_type_comboBox.setEnabled(True)
        else:
            self.NMPB_L_nig_type_comboBox.setEnabled(False)

        if self.NMPB_radioButton.isChecked():            
            self.NMPB_slope_comboBox.setEnabled(True)
            self.NMPB_surface_comboBox.setEnabled(True)
        else:
            self.NMPB_slope_comboBox.setEnabled(False)          
            self.NMPB_surface_comboBox.setEnabled(False)

        # CNOSSOS
        if self.CNOSSOS_1_checkBox.isChecked() and self.CNOSSOS_L_gen_checkBox.isChecked():
            self.CNOSSOS_L_gen_1_n_comboBox.setEnabled(True)    
            self.CNOSSOS_L_gen_1_s_comboBox.setEnabled(True)    
        else:
            self.CNOSSOS_L_gen_1_n_comboBox.setEnabled(False)    
            self.CNOSSOS_L_gen_1_s_comboBox.setEnabled(False)    
        if self.CNOSSOS_1_checkBox.isChecked() and self.CNOSSOS_L_day_checkBox.isChecked():
            self.CNOSSOS_L_day_1_n_comboBox.setEnabled(True)    
            self.CNOSSOS_L_day_1_s_comboBox.setEnabled(True)    
        else:
            self.CNOSSOS_L_day_1_n_comboBox.setEnabled(False)    
            self.CNOSSOS_L_day_1_s_comboBox.setEnabled(False)
        if self.CNOSSOS_1_checkBox.isChecked() and self.CNOSSOS_L_eve_checkBox.isChecked():
            self.CNOSSOS_L_eve_1_n_comboBox.setEnabled(True)    
            self.CNOSSOS_L_eve_1_s_comboBox.setEnabled(True)    
        else:
            self.CNOSSOS_L_eve_1_n_comboBox.setEnabled(False)    
            self.CNOSSOS_L_eve_1_s_comboBox.setEnabled(False)
        if self.CNOSSOS_1_checkBox.isChecked() and self.CNOSSOS_L_nig_checkBox.isChecked():
            self.CNOSSOS_L_nig_1_n_comboBox.setEnabled(True)    
            self.CNOSSOS_L_nig_1_s_comboBox.setEnabled(True)    
        else:
            self.CNOSSOS_L_nig_1_n_comboBox.setEnabled(False)    
            self.CNOSSOS_L_nig_1_s_comboBox.setEnabled(False) 
        
        if self.CNOSSOS_2_checkBox.isChecked() and self.CNOSSOS_L_gen_checkBox.isChecked():
            self.CNOSSOS_L_gen_2_n_comboBox.setEnabled(True)    
            self.CNOSSOS_L_gen_2_s_comboBox.setEnabled(True)    
        else:
            self.CNOSSOS_L_gen_2_n_comboBox.setEnabled(False)    
            self.CNOSSOS_L_gen_2_s_comboBox.setEnabled(False)    
        if self.CNOSSOS_2_checkBox.isChecked() and self.CNOSSOS_L_day_checkBox.isChecked():
            self.CNOSSOS_L_day_2_n_comboBox.setEnabled(True)    
            self.CNOSSOS_L_day_2_s_comboBox.setEnabled(True)    
        else:
            self.CNOSSOS_L_day_2_n_comboBox.setEnabled(False)    
            self.CNOSSOS_L_day_2_s_comboBox.setEnabled(False)
        if self.CNOSSOS_2_checkBox.isChecked() and self.CNOSSOS_L_eve_checkBox.isChecked():
            self.CNOSSOS_L_eve_2_n_comboBox.setEnabled(True)    
            self.CNOSSOS_L_eve_2_s_comboBox.setEnabled(True)    
        else:
            self.CNOSSOS_L_eve_2_n_comboBox.setEnabled(False)    
            self.CNOSSOS_L_eve_2_s_comboBox.setEnabled(False)
        if self.CNOSSOS_2_checkBox.isChecked() and self.CNOSSOS_L_nig_checkBox.isChecked():
            self.CNOSSOS_L_nig_2_n_comboBox.setEnabled(True)    
            self.CNOSSOS_L_nig_2_s_comboBox.setEnabled(True)    
        else:
            self.CNOSSOS_L_nig_2_n_comboBox.setEnabled(False)    
            self.CNOSSOS_L_nig_2_s_comboBox.setEnabled(False) 

        if self.CNOSSOS_3_checkBox.isChecked() and self.CNOSSOS_L_gen_checkBox.isChecked():
            self.CNOSSOS_L_gen_3_n_comboBox.setEnabled(True)    
            self.CNOSSOS_L_gen_3_s_comboBox.setEnabled(True)    
        else:
            self.CNOSSOS_L_gen_3_n_comboBox.setEnabled(False)    
            self.CNOSSOS_L_gen_3_s_comboBox.setEnabled(False)    
        if self.CNOSSOS_3_checkBox.isChecked() and  self.CNOSSOS_L_day_checkBox.isChecked():
            self.CNOSSOS_L_day_3_n_comboBox.setEnabled(True)    
            self.CNOSSOS_L_day_3_s_comboBox.setEnabled(True)    
        else:
            self.CNOSSOS_L_day_3_n_comboBox.setEnabled(False)    
            self.CNOSSOS_L_day_3_s_comboBox.setEnabled(False)
        if self.CNOSSOS_3_checkBox.isChecked() and  self.CNOSSOS_L_eve_checkBox.isChecked():
            self.CNOSSOS_L_eve_3_n_comboBox.setEnabled(True)    
            self.CNOSSOS_L_eve_3_s_comboBox.setEnabled(True)    
        else:
            self.CNOSSOS_L_eve_3_n_comboBox.setEnabled(False)    
            self.CNOSSOS_L_eve_3_s_comboBox.setEnabled(False)
        if self.CNOSSOS_3_checkBox.isChecked() and  self.CNOSSOS_L_nig_checkBox.isChecked():
            self.CNOSSOS_L_nig_3_n_comboBox.setEnabled(True)    
            self.CNOSSOS_L_nig_3_s_comboBox.setEnabled(True)    
        else:
            self.CNOSSOS_L_nig_3_n_comboBox.setEnabled(False)    
            self.CNOSSOS_L_nig_3_s_comboBox.setEnabled(False) 

        if self.CNOSSOS_4a_checkBox.isChecked() and self.CNOSSOS_L_gen_checkBox.isChecked():
            self.CNOSSOS_L_gen_4a_n_comboBox.setEnabled(True)    
            self.CNOSSOS_L_gen_4a_s_comboBox.setEnabled(True)    
        else:
            self.CNOSSOS_L_gen_4a_n_comboBox.setEnabled(False)    
            self.CNOSSOS_L_gen_4a_s_comboBox.setEnabled(False)    
        if self.CNOSSOS_4a_checkBox.isChecked() and self.CNOSSOS_L_day_checkBox.isChecked():
            self.CNOSSOS_L_day_4a_n_comboBox.setEnabled(True)    
            self.CNOSSOS_L_day_4a_s_comboBox.setEnabled(True)    
        else:
            self.CNOSSOS_L_day_4a_n_comboBox.setEnabled(False)    
            self.CNOSSOS_L_day_4a_s_comboBox.setEnabled(False)
        if self.CNOSSOS_4a_checkBox.isChecked() and self.CNOSSOS_L_eve_checkBox.isChecked():
            self.CNOSSOS_L_eve_4a_n_comboBox.setEnabled(True)    
            self.CNOSSOS_L_eve_4a_s_comboBox.setEnabled(True)    
        else:
            self.CNOSSOS_L_eve_4a_n_comboBox.setEnabled(False)    
            self.CNOSSOS_L_eve_4a_s_comboBox.setEnabled(False)
        if self.CNOSSOS_4a_checkBox.isChecked() and self.CNOSSOS_L_nig_checkBox.isChecked():
            self.CNOSSOS_L_nig_4a_n_comboBox.setEnabled(True)    
            self.CNOSSOS_L_nig_4a_s_comboBox.setEnabled(True)    
        else:
            self.CNOSSOS_L_nig_4a_n_comboBox.setEnabled(False)    
            self.CNOSSOS_L_nig_4a_s_comboBox.setEnabled(False) 

        if self.CNOSSOS_4b_checkBox.isChecked() and self.CNOSSOS_L_gen_checkBox.isChecked():
            self.CNOSSOS_L_gen_4b_n_comboBox.setEnabled(True)    
            self.CNOSSOS_L_gen_4b_s_comboBox.setEnabled(True)    
        else:
            self.CNOSSOS_L_gen_4b_n_comboBox.setEnabled(False)    
            self.CNOSSOS_L_gen_4b_s_comboBox.setEnabled(False)    
        if self.CNOSSOS_4b_checkBox.isChecked() and self.CNOSSOS_L_day_checkBox.isChecked():
            self.CNOSSOS_L_day_4b_n_comboBox.setEnabled(True)    
            self.CNOSSOS_L_day_4b_s_comboBox.setEnabled(True)    
        else:
            self.CNOSSOS_L_day_4b_n_comboBox.setEnabled(False)    
            self.CNOSSOS_L_day_4b_s_comboBox.setEnabled(False)
        if self.CNOSSOS_4b_checkBox.isChecked() and self.CNOSSOS_L_eve_checkBox.isChecked():
            self.CNOSSOS_L_eve_4b_n_comboBox.setEnabled(True)    
            self.CNOSSOS_L_eve_4b_s_comboBox.setEnabled(True)    
        else:
            self.CNOSSOS_L_eve_4b_n_comboBox.setEnabled(False)    
            self.CNOSSOS_L_eve_4b_s_comboBox.setEnabled(False)
        if self.CNOSSOS_4b_checkBox.isChecked() and self.CNOSSOS_L_nig_checkBox.isChecked():
            self.CNOSSOS_L_nig_4b_n_comboBox.setEnabled(True)    
            self.CNOSSOS_L_nig_4b_s_comboBox.setEnabled(True)    
        else:
            self.CNOSSOS_L_nig_4b_n_comboBox.setEnabled(False)    
            self.CNOSSOS_L_nig_4b_s_comboBox.setEnabled(False) 
            
        if self.CNOSSOS_radioButton.isChecked():            
            self.CNOSSOS_slope_comboBox.setEnabled(True)
            self.CNOSSOS_surface_comboBox.setEnabled(True)
        else:
            self.CNOSSOS_slope_comboBox.setEnabled(False)          
            self.CNOSSOS_surface_comboBox.setEnabled(False)
            
       
        self.setToolTips()


    def setToolTips(self):  
        
        for comboBox in self.all_emission_comboBoxes:
            
            if comboBox.isEnabled() == True:
                string = "Choose from a numeric field of the source layer"
                comboBox.setToolTip(string)
            else:
                comboBox.setToolTip("")
        
        string1 = "Choose from a string field of the source layer."
        
        string2 = "Possible Values: 'continuos', 'pulsed acelerated', 'pulsed decelerated', 'non-differentiated pulsed'." 
        if self.NMPB_L_gen_type_comboBox.isEnabled() == True:
            self.NMPB_L_gen_type_comboBox.setToolTip(string1 + "<br>" + string2)
        else:
            self.NMPB_L_gen_type_comboBox.setToolTip("")
        if self.NMPB_L_day_type_comboBox.isEnabled() == True:
            self.NMPB_L_day_type_comboBox.setToolTip(string1 + "<br>" + string2)
        else:
            self.NMPB_L_day_type_comboBox.setToolTip("")
        if self.NMPB_L_eve_type_comboBox.isEnabled() == True:
            self.NMPB_L_eve_type_comboBox.setToolTip(string1 + "<br>" + string2)
        else:
            self.NMPB_L_eve_type_comboBox.setToolTip("")
        if self.NMPB_L_nig_type_comboBox.isEnabled() == True:
            self.NMPB_L_nig_type_comboBox.setToolTip(string1 + "<br>" + string2)
        else:
            self.NMPB_L_nig_type_comboBox.setToolTip("")

        string2 = "Possible Values:  'down', 'flat', 'up'." 
        if self.NMPB_slope_comboBox.isEnabled() == True:
            self.NMPB_slope_comboBox.setToolTip(string1 + "<br>" + string2)
        else:
            self.NMPB_slope_comboBox.setToolTip("")
        
        string2 = "Possible Values: 'smooth', 'porous', 'stones', 'cement', 'corrugated'." 
        if self.NMPB_surface_comboBox.isEnabled() == True:
            self.NMPB_surface_comboBox.setToolTip(string1 + "<br>" + string2)
        else:
            self.NMPB_surface_comboBox.setToolTip("")



    def check(self):
        
        for comboBox in self.all_emission_comboBoxes:
            
            if comboBox.isEnabled() == True and comboBox.currentText() == "":
                QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("Please select a field"))
                return False

       
        if self.POWER_R_radioButton.isChecked():    
            count = 0
            for key in self.POWER_R_emission_comboBoxes_dict.keys():
                comboBox = self.POWER_R_emission_comboBoxes_dict[key]
                if comboBox.isEnabled():
                    count = 1
            if count == 0:
                QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("Please specify at least one power for a reference period."))
                return False
        
        if self.NMPB_radioButton.isChecked():    
            count = 0
            for key in self.NMPB_emission_comboBoxes_dict.keys():
                comboBox = self.NMPB_emission_comboBoxes_dict[key]
                if key <> 'NMPB_gen_type' and key <> 'NMPB_day_type' and key <> 'NMPB_eve_type' and key <> 'NMPB_nig_type' and key <> 'NMPB_slope' and key <> 'NMPB_surface':
                    if comboBox.isEnabled():
                        count = 1
            if count == 0:
                QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("Please specify at least one type of vehicle and reference period."))
                return False
        
        
        if self.CNOSSOS_radioButton.isChecked():    
            count = 0
            for key in self.CNOSSOS_emission_comboBoxes_dict.keys():
                comboBox = self.CNOSSOS_emission_comboBoxes_dict[key]
                
                if key <> 'CNOSSOS_surface' and key <> 'CNOSSOS_slope':
                    if comboBox.isEnabled():
                        count = 1
            if count == 0:
                QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("Please specify at least one type of vehicle and reference period."))
                return False
         

        return True
        

    def write_settings(self):
        
        settings = {}


        if self.POWER_R_radioButton.isChecked():
            settings['implementation_roads'] = 'POWER_R'
        if self.NMPB_radioButton.isChecked():
            settings['implementation_roads'] ='NMPB'
        if self.CNOSSOS_radioButton.isChecked():
            settings['implementation_roads'] ='CNOSSOS'

                
        if self.POWER_R_L_gen_checkBox.isChecked() or self.NMPB_L_gen_checkBox.isChecked() or self.CNOSSOS_L_gen_checkBox.isChecked():
            settings['period_roads_gen'] = 'True'
        else:
            settings['period_roads_gen'] = 'False'
        if self.POWER_R_L_day_checkBox.isChecked() or self.NMPB_L_day_checkBox.isChecked() or self.CNOSSOS_L_day_checkBox.isChecked():
            settings['period_roads_day'] = 'True'
        else:
            settings['period_roads_day'] = 'False'
        if self.POWER_R_L_eve_checkBox.isChecked() or self.NMPB_L_eve_checkBox.isChecked() or self.CNOSSOS_L_eve_checkBox.isChecked():
            settings['period_roads_eve'] = 'True'
        else:
            settings['period_roads_eve'] = 'False'
        if self.POWER_R_L_nig_checkBox.isChecked() or self.NMPB_L_nig_checkBox.isChecked() or self.CNOSSOS_L_nig_checkBox.isChecked():
            settings['period_roads_nig'] = 'True'
        else:
            settings['period_roads_nig'] = 'False'


        if self.POWER_R_radioButton.isChecked():
            for key in self.POWER_R_emission_comboBoxes_dict.keys():
                if self.POWER_R_emission_comboBoxes_dict[key].isEnabled():
                    settings[key] = self.POWER_R_emission_comboBoxes_dict[key].currentText()
                else:
                    settings[key] = ''
        if self.NMPB_radioButton.isChecked():
            for key in self.NMPB_emission_comboBoxes_dict.keys():
                if self.NMPB_emission_comboBoxes_dict[key].isEnabled():
                    settings[key] = self.NMPB_emission_comboBoxes_dict[key].currentText()
                else:
                    settings[key] = ''
        if self.CNOSSOS_radioButton.isChecked():
            for key in self.CNOSSOS_emission_comboBoxes_dict.keys():
                if self.CNOSSOS_emission_comboBoxes_dict[key].isEnabled():
                    settings[key] = self.CNOSSOS_emission_comboBoxes_dict[key].currentText()
                else:
                    settings[key] = ''

        on_Settings.setSettings(settings)
        
        
    def reload_settings(self):
        
        try:
            settings = on_Settings.getAllSettings()                      
        
            if settings['implementation_roads'] == 'POWER_R':
                self.POWER_R_radioButton.setChecked(1)
    
                if settings['period_roads_gen'] == "True":
                    self.POWER_R_L_gen_checkBox.setChecked(1)
                if settings['period_roads_day'] == "True":
                    self.POWER_R_L_day_checkBox.setChecked(1)
                if settings['period_roads_eve'] == "True":
                    self.POWER_R_L_eve_checkBox.setChecked(1)
                if settings['period_roads_nig'] == "True":
                    self.POWER_R_L_nig_checkBox.setChecked(1)
                
                for key in self.POWER_R_emission_comboBoxes_dict.keys():
                    if settings[key] is not None:
                        idx = self.POWER_R_emission_comboBoxes_dict[key].findText(settings[key])
                        self.POWER_R_emission_comboBoxes_dict[key].setCurrentIndex(idx)
    
                        
            if settings['implementation_roads'] == 'NMPB':
                self.NMPB_radioButton.setChecked(1)
    
                if settings['period_roads_gen'] == "True":
                    self.NMPB_L_gen_checkBox.setChecked(1)
                if settings['period_roads_day'] == "True":
                    self.NMPB_L_day_checkBox.setChecked(1)
                if settings['period_roads_eve'] == "True":
                    self.NMPB_L_eve_checkBox.setChecked(1)
                if settings['period_roads_nig'] == "True":
                    self.NMPB_L_nig_checkBox.setChecked(1)    
                            
                for key in self.NMPB_emission_comboBoxes_dict.keys():
                    if settings[key] is not None:
                        idx = self.NMPB_emission_comboBoxes_dict[key].findText(settings[key])
                        self.NMPB_emission_comboBoxes_dict[key].setCurrentIndex(idx)
                        
                        if key.find('_l_') > -1:
                            self.NMPB_l_checkBox.setChecked(1)
                        if key.find('_h_') > -1:
                            self.NMPB_h_checkBox.setChecked(1)
                        
    
            if settings['implementation_roads'] == 'CNOSSOS':
                self.CNOSSOS_radioButton.setChecked(1)
    
                if settings['period_roads_gen'] == "True":
                    self.CNOSSOS_L_gen_checkBox.setChecked(1)
                if settings['period_roads_day'] == "True":
                    self.CNOSSOS_L_day_checkBox.setChecked(1)
                if settings['period_roads_eve'] == "True":
                    self.CNOSSOS_L_eve_checkBox.setChecked(1)
                if settings['period_roads_nig'] == "True":
                    self.CNOSSOS_L_nig_checkBox.setChecked(1)                    
                            
                for key in self.CNOSSOS_emission_comboBoxes_dict.keys():
                    if settings[key] is not None:
                        idx = self.CNOSSOS_emission_comboBoxes_dict[key].findText(settings[key])
                        self.CNOSSOS_emission_comboBoxes_dict[key].setCurrentIndex(idx)
                        
                        if key.find('_1_') > -1:
                            self.CNOSSOS_1_checkBox.setChecked(1)
                        if key.find('_2_') > -1:
                            self.CNOSSOS_2_checkBox.setChecked(1)
                        if key.find('_3_') > -1:
                            self.CNOSSOS_3_checkBox.setChecked(1)
                        if key.find('_4a_') > -1:
                            self.CNOSSOS_4a_checkBox.setChecked(1)
                        if key.find('_4b_') > -1:
                            self.CNOSSOS_4b_checkBox.setChecked(1)
    
            self.source_checkBox_update()
    
        except:
            QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("Sorry, but somethigs wrong in import last settings."))
            
    
    def accept(self):
        
        if self.check() == False:
            return

        self.write_settings()
       
        self.close()

        
        

    
