# -*- coding: utf-8 -*-
"""
/***************************************************************************
 opeNoise

 Qgis Plugin to compute noise levels

                             -------------------
        begin                : February 2019
        copyright            : (C) 2019 by Arpa Piemonte
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

from PyQt5.uic.properties import QtGui
from qgis.PyQt.QtCore import QObject, QSize

from qgis.PyQt import uic
from qgis.PyQt.QtWidgets import QDialog, QScrollArea, QWidget, QVBoxLayout, QLabel
from qgis.PyQt.QtWidgets import QMessageBox
from qgis.core import QgsProject, QgsFieldProxyModel

import os, sys



sys.path.append(os.path.dirname(__file__))
ui_SourceDetailsRoads_ui, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_SourceDetailsRoads.ui'), resource_suffix='')


from . import on_Settings




class Dialog(QDialog,ui_SourceDetailsRoads_ui):

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

        self.decimal_comboBoxes = [self.POWER_R_L_gen_comboBox, self.POWER_R_L_day_comboBox,
                                        self.POWER_R_L_eve_comboBox, self.POWER_R_L_nig_comboBox
                                   ]

        self.int_comboBoxes = [        self.NMPB_L_gen_l_n_comboBox, self.NMPB_L_day_l_n_comboBox,
                                       self.NMPB_L_eve_l_n_comboBox, self.NMPB_L_nig_l_n_comboBox,
                                       self.NMPB_L_gen_l_s_comboBox, self.NMPB_L_day_l_s_comboBox,
                                       self.NMPB_L_eve_l_s_comboBox, self.NMPB_L_nig_l_s_comboBox,
                                       self.NMPB_L_gen_h_n_comboBox, self.NMPB_L_day_h_n_comboBox,
                                       self.NMPB_L_eve_h_n_comboBox, self.NMPB_L_nig_h_n_comboBox,
                                       self.NMPB_L_gen_h_s_comboBox, self.NMPB_L_day_h_s_comboBox,
                                       self.NMPB_L_eve_h_s_comboBox, self.NMPB_L_nig_h_s_comboBox,
                                       self.CNOSSOS_L_gen_1_n_comboBox, self.CNOSSOS_L_day_1_n_comboBox,
                                       self.CNOSSOS_L_eve_1_n_comboBox, self.CNOSSOS_L_nig_1_n_comboBox,
                                       self.CNOSSOS_L_gen_1_s_comboBox, self.CNOSSOS_L_day_1_s_comboBox,
                                       self.CNOSSOS_L_eve_1_s_comboBox, self.CNOSSOS_L_nig_1_s_comboBox,
                                       self.CNOSSOS_L_gen_2_n_comboBox, self.CNOSSOS_L_day_2_n_comboBox,
                                       self.CNOSSOS_L_eve_2_n_comboBox, self.CNOSSOS_L_nig_2_n_comboBox,
                                       self.CNOSSOS_L_gen_2_s_comboBox, self.CNOSSOS_L_day_2_s_comboBox,
                                       self.CNOSSOS_L_eve_2_s_comboBox, self.CNOSSOS_L_nig_2_s_comboBox,
                                       self.CNOSSOS_L_gen_3_n_comboBox, self.CNOSSOS_L_day_3_n_comboBox,
                                       self.CNOSSOS_L_eve_3_n_comboBox, self.CNOSSOS_L_nig_3_n_comboBox,
                                       self.CNOSSOS_L_gen_3_s_comboBox, self.CNOSSOS_L_day_3_s_comboBox,
                                       self.CNOSSOS_L_eve_3_s_comboBox, self.CNOSSOS_L_nig_3_s_comboBox,
                                       self.CNOSSOS_L_gen_4a_n_comboBox, self.CNOSSOS_L_day_4a_n_comboBox,
                                       self.CNOSSOS_L_eve_4a_n_comboBox, self.CNOSSOS_L_nig_4a_n_comboBox,
                                       self.CNOSSOS_L_gen_4a_s_comboBox, self.CNOSSOS_L_day_4a_s_comboBox,
                                       self.CNOSSOS_L_eve_4a_s_comboBox, self.CNOSSOS_L_nig_4a_s_comboBox,
                                       self.CNOSSOS_L_gen_4b_n_comboBox, self.CNOSSOS_L_day_4b_n_comboBox,
                                       self.CNOSSOS_L_eve_4b_n_comboBox, self.CNOSSOS_L_nig_4b_n_comboBox,
                                       self.CNOSSOS_L_gen_4b_s_comboBox, self.CNOSSOS_L_day_4b_s_comboBox,
                                       self.CNOSSOS_L_eve_4b_s_comboBox, self.CNOSSOS_L_nig_4b_s_comboBox,
                                       self.CNOSSOS_slope_comboBox
                                       ]

        self.string_comboBoxes = [      self.NMPB_L_gen_type_comboBox, self.NMPB_L_day_type_comboBox,
                                        self.NMPB_L_eve_type_comboBox, self.NMPB_L_nig_type_comboBox,
                                        self.NMPB_slope_comboBox, self.NMPB_surface_comboBox, self.CNOSSOS_surface_comboBox
                                        ]

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

        self.POWER_R_radioButton.toggled.connect(self.road_stackedWidget_update)
        self.NMPB_radioButton.toggled.connect(self.road_stackedWidget_update)
        self.CNOSSOS_radioButton.toggled.connect(self.road_stackedWidget_update)
        self.HelpNMPB_traffic.clicked.connect(self.HelpNMPB_traffic_show)
        self.HelpNMPB.hide()
        #self.HelpNMPB.clicked.connect(self.HelpNMPB_show)
        self.HelpCNOSSOS.clicked.connect(self.HelpCNOSSOS_show)

        for source_checkBox in self.source_checkBoxes:
            source_checkBox.setChecked(0)
            source_checkBox.toggled.connect(self.source_checkBox_update)

        self.setToolTips()

        self.HelpNMPB.hide()

        self.reload_settings()

    def uniques_feat_item(self,layer, namefield,casesensitive=False):
        features = layer.getFeatures()
        all_item = []
        for feature in features:
            # if feature[namefield] is None or feature[namefield] == "NULL" or feature[namefield] == "":
            #     all_item.append(feature[namefield])
            # else:
            #     all_item.append(feature[namefield].lower())
            try:
                all_item.append(feature[namefield].lower())
            except:
                all_item.append(feature[namefield])
            # all_item.append(feature[namefield])

        example_type = list(set(all_item))
        return example_type

    def test_field(self,all_types,unique_field_values,namefield):
        result = all(elem in all_types for elem in unique_field_values)
        if result:
            return (True,'OK')
        else:
            difference = set(unique_field_values) - set(all_types)
            error = self.tr('Errors in field: ')+namefield+self.tr(' for values: ')+str(difference)
            return (False,error)

    def HelpNMPB_show(self):
        QMessageBox.information(self, self.tr("opeNoise - Help"), self.tr('''Help NMPB traffic mode'''))

    def HelpNMPB_traffic_show(self):
        QMessageBox.information(self, self.tr("opeNoise - Help NMPB"), self.tr('''
        <p><span lang="en-US"><strong>Light vehicles number:</strong></span><span lang="en-US"> loaded weight &lt; 3,5 t. Average hourly value.</span></p>
<p><span lang="en-US"><strong>Heavy vehicles number:</strong></span><span lang="en-US"> loaded weight </span><span lang="en-US">&ge; </span><span lang="en-US">3,5 t. Average hourly value.</span></p>
<p>&nbsp;</p>
<p><span lang="en-US"><strong>Light vehicles speed</strong></span><span lang="en-US">: average speed (20-130 km/h)</span></p>
<p><span lang="en-US"><strong>Heavy vehicles speed</strong></span><span lang="en-US">: average speed (20-100 km/h)</span></p>
<p>&nbsp;</p>
<p><span lang="en-US"><strong>Type of Traffic:</strong></span></p>
<p><span lang="en-US"><strong>Continuous</strong></span><span lang="en-US"> (i.e. Motorway, Interurban road; Urban expressway (off)rush hours; Major roads in urban environment) </span></p>
<p><span lang="en-US"><strong>Non-differentiated pulsed</strong></span><span lang="en-US"> (i.e. Urban city-centre roads; Major roads close to saturation; Dispatching or connecting roads with numerous crossings, car parks, pedestrian crossings, junctions to dwellings) </span></p>
<p><span lang="en-US"><strong>Pulsed accelerated </strong></span><span lang="en-US">(i.e.</span><span lang="en-US">Expressway after a crossing; Motorway entrance; Tollbooth)</span></p>
<p><span lang="en-US"><strong>Pulsed decelerated </strong></span><span lang="en-US">(i.e.</span><span lang="en-US">Expressway before a crossing; Motorway exit; Approach of tollbooth) </span></p>
<p>&nbsp;</p>
<p><span lang="en-US"><strong>Road slope: </strong></span></p>
<p><span lang="en-US"><strong>Down</strong></span><span lang="en-US"> Road gradient &gt; 2% downward </span></p>
<p><span lang="en-US"><strong>Up </strong></span><span lang="en-US"> Road gradient &gt; 2% upward </span></p>
<p><span lang="en-US"><strong>Flat</strong></span><span lang="en-US"> Road gradient &le; 2% </span></p>
<p>&nbsp;</p>
<p><span lang="en-US"><strong>Road surface:</strong></span></p>
<table border="1" width="642" cellspacing="0" cellpadding="7">
<tbody>
<tr>
<td style="text-align: center;" width="79" height="10">
<p><span lang="en-US"><strong>Id</strong></span></p>
</td>
<td style="text-align: center;" width="320">
<p><span lang="en-US"><strong>Road Surface Categories</strong></span></p>
</td>
<td style="text-align: center;" colspan="3" width="199">
<p><span lang="en-US"><strong>Noise Level Correction</strong></span></p>
</td>
</tr>
<tr>
<td style="text-align: center;" rowspan="2" width="79" height="12">
<p><span lang="en-US">porous</span></p>
</td>
<td style="text-align: center;" rowspan="2" width="320">
<p><span lang="en-US">Porous Surface</span></p>
</td>
<td style="text-align: center;" width="57">
<p><span lang="en-US">0-60 km/h</span></p>
</td>
<td style="text-align: center;" width="57">
<p><span lang="en-US">61-80 km/h</span></p>
</td>
<td style="text-align: center;" width="56">
<p><span lang="en-US">81-130 km/h</span></p>
</td>
</tr>
<tr>
<td style="text-align: center;" width="57">
<p><span lang="en-US">-1 dB</span></p>
</td>
<td style="text-align: center;" width="57">
<p><span lang="en-US">-2 dB</span></p>
</td>
<td style="text-align: center;" width="56">
<p><span lang="en-US">-3 dB</span></p>
</td>
</tr>
<tr>
<td style="text-align: center;" width="79">
<p><span lang="en-US">smooth</span></p>
</td>
<td style="text-align: center;" width="320">
<p><span lang="en-US">Smooth asphalt (concrete or mastic)</span></p>
</td>
<td style="text-align: center;" colspan="3" width="199">
<p><span lang="en-US">0 dB</span></p>
</td>
</tr>
<tr>
<td style="text-align: center;" width="79">
<p><span lang="en-US">cement</span></p>
</td>
<td style="text-align: center;" width="320">
<p><span lang="en-US">Cement concrete</span></p>
</td>
<td style="text-align: center;" colspan="3" width="199">
<p><span lang="en-US">+2 dB</span></p>
</td>
</tr>
<tr>
<td style="text-align: center;" width="79">
<p><span lang="en-US">corrugated</span></p>
</td>
<td style="text-align: center;" width="320">
<p><span lang="en-US">Corrugated asphalt</span></p>
</td>
<td style="text-align: center;" colspan="3" width="199">
<p><span lang="en-US">+2 dB</span></p>
</td>
</tr>
<tr>
<td style="text-align: center;" width="79">
<p><span lang="en-US">stones</span></p>
</td>
<td style="text-align: center;" width="320">
<p><span lang="en-US">Paving stones</span></p>
</td>
<td style="text-align: center;" colspan="3" width="199">
<p><span lang="en-US">+3 dB</span></p>
</td>
</tr>
</tbody>
</table>
        '''))

    def HelpCNOSSOS_show(self):
        string_list = [
            '''
           <p><strong>Vehicles type (average hourly value):</strong></p><p>&nbsp;</p>
<table border="1">
<tbody>
<tr>
<td style="height: 56px; text-align: center;">
<p><strong>Name</strong></p>
</td>
<td style="height: 56px; text-align: center;">
<p><strong>Description</strong></p>
</td>
<td style="height: 56px; text-align: center;">
<p><strong>Vehicle category in EC</strong></p>
<p>&nbsp;<strong>Whole Vehicle Type Approval</strong></p>
<p><strong>(1)</strong></p>
</td>
</tr>
<tr style="height: 29px;">
<td style="height: 29px; text-align: center;">
<p>LIGHT</p>
</td>
<td style="height: 29px; text-align: center;">
<p>Passenger cars,<br />Delivery vans &le; 3.5 tons,<br />SUVs (2), MPVs (3) including<br />trailers and caravans</p>
</td>
<td style="height: 29px; text-align: center;">
<p>M1 and N1</p>
</td>
</tr>
<tr style="height: 59px;">
<td style="height: 59px; text-align: center;">
<p>MEDIUM HEAVY</p>
</td>
<td style="height: 59px; text-align: center;">
<p>Medium heavy vehicles,<br /> delivery vans &gt;3.5tons,<br /> buses, touring cars,<br />etc. with two axles and<br />twin-tyre mounting on rear axle</p>
</td>
<td style="height: 59px; text-align: center;">
<p>M2, M3 and N2, N3</p>
</td>
</tr>
<tr style="height: 35px;">
<td style="height: 35px; text-align: center;">
<p>HEAVY</p>
</td>
<td style="height: 35px; text-align: center;">
<p>Heavy duty vehicles, touring cars, buses,<br />with three or more axles</p>
</td>
<td style="height: 35px; text-align: center;">
<p>M2 and N2 with trailer,<br />M3 and N3</p>
</td>
</tr>
<tr style="height: 35px;">
<td style="height: 35px; text-align: center;">
<p>2-WHEEL &le; 50 cc</p>
</td>
<td style="height: 35px; text-align: center;">
<p>mopeds, tricycles or quads &le; 50cc</p>
</td>
<td style="height: 35px; text-align: center;">
<p>L1, L2, L6</p>
</td>
</tr>
<tr style="height: 35px;">
<td style="height: 35px; text-align: center;">
<p>2-WHEEL &gt; 50 cc</p>
</td>
<td style="height: 35px; text-align: center;">
<p>motorcycles, tricycles or quads &gt; 50cc</p>
</td>
<td style="height: 35px; text-align: center;">
<p>L3, L4, L5, L7</p>
</td>
</tr>
</tbody>
</table>
''','''

<p>(1) Directive 2007/46/EC of the European Parliament and of the Council of 5 September 2007<br>(OJ L263/19/10/2007) establishing a framework for the approval of motor vehicles and their trailers,<br>and of systems, components and separate technical <br>units intended for such vehicles</p>

<p>(2) Sport Utility Vehicles</p>
<p>(3) Multi‐Purpose Vehicles</p><br>
''','''
<p><strong>Road slope: </strong>road gradient (%)</p>
<br>
<p><strong>Road surface:</strong></p>
<p>&nbsp;</p>
<table border="1">
<tbody>
<tr>
<td style="text-align: center;">
<p><strong>Id</strong></p>
</td>
<td style="text-align: center;">
<p><strong>Description</strong></p>
</td>
</tr>
<tr>
<td style="text-align: center;">
<p>0</p>
</td>
<td style="text-align: center; padding:5px">
<p>Reference road surface<br />consisting of an average of dense asphalt concrete 0/11<br />and stone mastic asphalt 0/11, between 2 and 7 years old<br />and in a representative maintenance condition</p>
</td>
</tr>
<tr>
<td style="text-align: center;">
<p>NL01</p>
</td>
<td style="text-align: center;">
<p>1-layer ZOAB</p>
</td>
</tr>
<tr>
<td style="text-align: center;">
<p>&nbsp; &nbsp; NL02 &nbsp; &nbsp;</p>
</td>
<td style="text-align: center;">
<p>2-layer ZOAB</p>
</td>
</tr>
<tr>
<td style="text-align: center;">
<p>NL03</p>
</td>
<td style="text-align: center;">
<p>2-layer ZOAB (fine)</p>
</td>
</tr>
<tr>
<td style="text-align: center;">
<p>NL04</p>
</td>
<td style="text-align: center;">
<p>SMA-NL5</p>
</td>
</tr>
<tr>
<td style="text-align: center;">
<p>NL05</p>
</td>
<td style="text-align: center;">
<p>SMA-NL8</p>
</td>
</tr>
<tr>
<td style="text-align: center;">
<p>NL06</p>
</td>
<td style="text-align: center;">
<p>Brushed down concrete</p>
</td>
</tr>
<tr>
<td style="text-align: center;">
<p>NL07</p>
</td>
<td style="text-align: center;">
<p>Optimized brushed down concrete</p>
</td>
</tr>
<tr>
<td style="text-align: center;">
<p>NL08</p>
</td>
<td style="text-align: center;">
<p>Fine broomed concrete</p>
</td>
</tr>
<tr>
<td style="text-align: center;">
<p>NL09</p>
</td>
<td style="text-align: center;">
<p>Worked surface</p>
</td>
</tr>
<tr>
<td style="text-align: center;">
<p>NL10</p>
</td>
<td style="text-align: center;">
<p>Hard elements in herring-bone</p>
</td>
</tr>
<tr>
<td style="text-align: center;">
<p>NL11</p>
</td>
<td style="text-align: center;">
<p>Hard elements not in herring-bone</p>
</td>
</tr>
<tr>
<td style="text-align: center;">
<p>NL12</p>
</td>
<td style="text-align: center;">
<p>Quiet hard elements</p>
</td>
</tr>
<tr>
<td style="text-align: center;">
<p>NL13</p>
</td>
<td style="text-align: center;">
<p>Thin layer A</p>
</td>
</tr>
<tr>
<td style="text-align: center;">
<p>NL14</p>
</td>
<td style="text-align: center;">
<p>Thin layer B</p>
</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
            '''
        ]
        result = ScrollMessageBox(string_list, None)
        result.exec_()




    def road_stackedWidget_update( self ):

        if self.POWER_R_radioButton.isChecked():
            self.road_stackedWidget.setCurrentIndex(0)

            self.NMPB_L_gen_checkBox.setChecked(0)
            self.NMPB_L_day_checkBox.setChecked(0)
            self.NMPB_L_eve_checkBox.setChecked(0)
            self.NMPB_L_nig_checkBox.setChecked(0)

            self.CNOSSOS_L_gen_checkBox.setChecked(0)
            self.CNOSSOS_L_day_checkBox.setChecked(0)
            self.CNOSSOS_L_eve_checkBox.setChecked(0)
            self.CNOSSOS_L_nig_checkBox.setChecked(0)


        if self.NMPB_radioButton.isChecked():
            self.road_stackedWidget.setCurrentIndex(1)

            self.POWER_R_L_gen_checkBox.setChecked(0)
            self.POWER_R_L_day_checkBox.setChecked(0)
            self.POWER_R_L_eve_checkBox.setChecked(0)
            self.POWER_R_L_nig_checkBox.setChecked(0)

            self.CNOSSOS_L_gen_checkBox.setChecked(0)
            self.CNOSSOS_L_day_checkBox.setChecked(0)
            self.CNOSSOS_L_eve_checkBox.setChecked(0)
            self.CNOSSOS_L_nig_checkBox.setChecked(0)


        if self.CNOSSOS_radioButton.isChecked():
            self.road_stackedWidget.setCurrentIndex(2)

            self.POWER_R_L_gen_checkBox.setChecked(0)
            self.POWER_R_L_day_checkBox.setChecked(0)
            self.POWER_R_L_eve_checkBox.setChecked(0)
            self.POWER_R_L_nig_checkBox.setChecked(0)

            self.NMPB_L_gen_checkBox.setChecked(0)
            self.NMPB_L_day_checkBox.setChecked(0)
            self.NMPB_L_eve_checkBox.setChecked(0)
            self.NMPB_L_nig_checkBox.setChecked(0)

        self.source_checkBox_update()


    def source_fields_update(self):

        source_layer = QgsProject.instance().mapLayersByName(self.layer_name)[0]
        source_layer_fields = list(source_layer.dataProvider().fields())

        source_layer_fields_labels = [""]

        for f in source_layer_fields:
#            if f.type() == QVariant.Int or f.type() == QVariant.Double:
                source_layer_fields_labels.append(str(f.name()))


        for comboBox in self.all_emission_comboBoxes:
            comboBox.clear()
            comboBox.setEnabled(False)

            comboBox.setLayer(source_layer)

        #load only fields type according to the required input
        for comboBox in self.decimal_comboBoxes:
            comboBox.setFilters(QgsFieldProxyModel.Numeric | QgsFieldProxyModel.Double | QgsFieldProxyModel.Int)
        for comboBox in self.int_comboBoxes:
            comboBox.setFilters(QgsFieldProxyModel.Numeric | QgsFieldProxyModel.Double | QgsFieldProxyModel.Int)
        for comboBox in self.string_comboBoxes:
            comboBox.setFilters(QgsFieldProxyModel.String)


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
                string = self.tr("Choose from a numeric field of the source layer")
                comboBox.setToolTip(string)
            else:
                comboBox.setToolTip("")

        string1 = self.tr("Choose from a string field of the source layer.")

        string2 = self.tr("Possible Values: 'continuous', 'pulsed accelerated', 'pulsed decelerated', 'non-differentiated pulsed'.")
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

        string2 = self.tr("Possible Values:  'down', 'flat', 'up'.")
        if self.NMPB_slope_comboBox.isEnabled() == True:
            self.NMPB_slope_comboBox.setToolTip(string1 + "<br>" + string2)
        else:
            self.NMPB_slope_comboBox.setToolTip("")

        string2 = self.tr("Possible Values: 'smooth', 'porous', 'stones', 'cement', 'corrugated'.")
        if self.NMPB_surface_comboBox.isEnabled() == True:
            self.NMPB_surface_comboBox.setToolTip(string1 + "<br>" + string2)
        else:
            self.NMPB_surface_comboBox.setToolTip("")


        if self.CNOSSOS_surface_comboBox.isEnabled() == True:
            self.CNOSSOS_surface_comboBox.setToolTip(string1)
        else:
            self.CNOSSOS_surface_comboBox.setToolTip("")



    def check(self):

        for comboBox in self.all_emission_comboBoxes:

            if comboBox.isEnabled() == True and comboBox.currentText() == "":
                QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("Please select a field"))
                return False


        if self.POWER_R_radioButton.isChecked():
            count = 0
            for key in list(self.POWER_R_emission_comboBoxes_dict.keys()):
                comboBox = self.POWER_R_emission_comboBoxes_dict[key]
                if comboBox.isEnabled():
                    count = 1
            if count == 0:
                QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("Please specify at least one power for a reference period."))
                return False

        if self.NMPB_radioButton.isChecked():
            count = 0
            for key in list(self.NMPB_emission_comboBoxes_dict.keys()):
                comboBox = self.NMPB_emission_comboBoxes_dict[key]
                field = comboBox.currentField()
                layer = comboBox.layer()
                if key != 'NMPB_gen_type' and key != 'NMPB_day_type' and key != 'NMPB_eve_type' and key != 'NMPB_nig_type' and key != 'NMPB_slope' and key != 'NMPB_surface':
                    if comboBox.isEnabled():
                        count = 1
                if field != "":
                    #check on Traffic type NMBP
                    if key == 'NMPB_gen_type' or key == 'NMPB_day_type' or key == 'NMPB_eve_type' or key == 'NMPB_nig_type' :
                        elem_unici = self.uniques_feat_item(layer, field)
                        traffic_type = ['continuous', 'pulsed accelerated', 'pulsed decelerated',
                                        'non-differentiated pulsed']
                        test = self.test_field(traffic_type,elem_unici,field)
#                        if test[0]:
#                            count = 1
#                        else:
                        if not test[0]:
                            QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr(
                                "Error in NMPB Traffic type: ") +'\n'+ test[1])
                            return False
                    # check on Slope type NMBP
                    if key == 'NMPB_slope':
                        elem_unici = self.uniques_feat_item(layer, field)
                        slope_type = ['down', 'flat', 'up']
                        test = self.test_field(slope_type,elem_unici,field)
#                        if test[0]:
#                            count = 1
#                        else:
                        if not test[0]:
                            QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr(
                                "Error in NMPB Slope type: ") +'\n'+  test[1])
                            return False

                    # check on Surface type NMBP
                    if key == 'NMPB_surface':
                        elem_unici = self.uniques_feat_item(layer, field)
                        surface_type = ['porous', 'smooth', 'cement', 'corrugated', 'stones']
                        test = self.test_field(surface_type, elem_unici, field)
#                        if test[0]:
#                            count = 1
#                        else:
                        if not test[0]:
                            QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr(
                                "Error in NMPB Surface type: ") + '\n' + test[1])
                            return False


            if count == 0:
                QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("Please specify at least one type of vehicle and reference period."))
                return False


        if self.CNOSSOS_radioButton.isChecked():
            count = 0
            for key in list(self.CNOSSOS_emission_comboBoxes_dict.keys()):
                comboBox = self.CNOSSOS_emission_comboBoxes_dict[key]
                field = comboBox.currentField()
                layer = comboBox.layer()
                if key != 'CNOSSOS_surface' and key != 'CNOSSOS_slope':
                    if comboBox.isEnabled():
                        count = 1
                if field != "":
                    #check on Surface type CNOSSOS
                    if key == 'CNOSSOS_surface' :
                        elem_unici = self.uniques_feat_item(layer, field)
                        #surface_type = ['0', 'NL01', 'NL02', 'NL03', 'NL04', 'NL05', 'NL06',
                        #                  'NL07', 'NL08', 'NL09', 'NL10', 'NL11',
                        #                 'NL12', 'NL13', 'NL14']
                        surface_type = ['0', 'nl01', 'nl02', 'nl03', 'nl04', 'nl05', 'nl06',
                                        'nl07', 'nl08', 'nl09', 'nl10', 'nl11',
                                        'nl12', 'nl13', 'nl14']
                        test = self.test_field(surface_type,elem_unici,field)
#                        if test[0]:
#                            count = 1
#                        else:
                        if not test[0]:
                            QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr(
                                "Error in CNOSSOS Surface  type: ") +'\n'+ test[1])
                            return False
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
            for key in list(self.POWER_R_emission_comboBoxes_dict.keys()):
                if self.POWER_R_emission_comboBoxes_dict[key].isEnabled():
                    settings[key] = self.POWER_R_emission_comboBoxes_dict[key].currentText()
                else:
                    settings[key] = ''
        if self.NMPB_radioButton.isChecked():
            for key in list(self.NMPB_emission_comboBoxes_dict.keys()):
                if self.NMPB_emission_comboBoxes_dict[key].isEnabled():
                    settings[key] = self.NMPB_emission_comboBoxes_dict[key].currentText()
                else:
                    settings[key] = ''
        if self.CNOSSOS_radioButton.isChecked():
            for key in list(self.CNOSSOS_emission_comboBoxes_dict.keys()):
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

                for key in list(self.POWER_R_emission_comboBoxes_dict.keys()):
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

                for key in list(self.NMPB_emission_comboBoxes_dict.keys()):
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

                for key in list(self.CNOSSOS_emission_comboBoxes_dict.keys()):
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
            QMessageBox.information(self, self.tr("opeNoise - Calculate Noise Levels"), self.tr("Sorry, but somethigs wrong importing last settings."))


    def accept(self):

        if self.check() == False:
            return

        self.write_settings()

        self.close()





class ScrollMessageBox(QMessageBox):
   def __init__(self, l, *args, **kwargs):
      QMessageBox.__init__(self, *args, **kwargs)
      QMessageBox.setWindowTitle(self,self.tr("opeNoise - Help CNOSSOS"))
      scroll = QScrollArea(self)
      scroll.setWidgetResizable(True)
      self.content = QWidget()
      scroll.setWidget(self.content)
      lay = QVBoxLayout(self.content)
      for item in l:
         lay.addWidget(QLabel(item, self))
      self.layout().addWidget(scroll, 0, 0, 1, self.layout().columnCount())
      self.setStyleSheet("QScrollArea{min-width:800 px; min-height: 400px}")
