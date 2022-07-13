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

#from PyQt4.QtCore import *
import pandas as pd
import numpy as np
from builtins import str
from statistics import median
from qgis.PyQt.QtCore import QObject
from qgis.PyQt.QtCore import QVariant
from qgis.PyQt.QtWidgets import QDialog
#from qgis.core import *
from qgis.PyQt.QtWidgets import QDialogButtonBox
from qgis.PyQt.QtWidgets import QMessageBox

from qgis.core import (QgsProject,QgsVectorLayer,QgsFeature,
                       QgsWkbTypes,QgsFieldProxyModel,
                       QgsField, QgsMapLayerProxyModel,NULL as qgisnull)
try:
    from qgis.core import Qgis
except ImportError:
    from qgis.core import QGis as Qgis
from qgis.PyQt import uic
import os, sys, shutil
import traceback

#from math import *
from datetime import datetime
sys.path.append(os.path.dirname(__file__))
Ui_AssignNoiseToBuildings_window, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui_NoiseExposure.ui'), resource_suffix='')

from . import on_ApplyNoiseSymbology

def CreateTempDir():

    global temp_dir

    currentPath = os.path.dirname(__file__)
    temp_dir = os.path.abspath(os.path.join(currentPath + os.sep +'temp'))

    if os.path.isdir(temp_dir):
        DeleteTempDir()

    os.mkdir(temp_dir)


def DeleteTempDir():

    shutil.rmtree(temp_dir)

def myround(x, base=100):
    '''
    function to round following the directive
    :param base:
    :return: rounded value required
    '''
    x = float(x)
    return base * round(x/base)

class Dialog(QDialog, Ui_AssignNoiseToBuildings_window):

    def __init__(self, iface):
        QDialog.__init__(self, iface.mainWindow())
        self.iface = iface
        # Set up the user interface from Designer.
        self.setupUi(self)

        string = self.tr("<b>WARNING:</b>") + '\n' +\
                 self.tr("This tool works correctly only if the receiver points layer ") + '\n' +\
                 self.tr("is created from a buildings layer with opeNoise") + '\n' +\
                 self.tr("and its structure is not modified.")
        QMessageBox.information(self, self.tr("opeNoise - Noise Exposure"), self.tr(string))

        self.populate_comboBox()

        self.progressBar.setValue(0)

        self.run_buttonBox.button( QDialogButtonBox.Ok )

        self.receiver_points_layer_comboBox.currentIndexChanged.connect(self.update_field_receiver_points_layer)



        self.helpNoiseExp.clicked.connect(self.HelpNoiseExposure_show)

        self.receiver_points_population_field.setFilters(
            QgsFieldProxyModel.Double | QgsFieldProxyModel.Int | QgsFieldProxyModel.Numeric)
        self.dwellingCombobox.setFilters(
            QgsFieldProxyModel.Double | QgsFieldProxyModel.Int | QgsFieldProxyModel.Numeric)
        self.methodComboBox.setFilters(
            QgsFieldProxyModel.String)

    def HelpNoiseExposure_show(self):
            QMessageBox.information(self, self.tr("opeNoise - Help"), self.tr('''
            <p><b>According to §2.8 Directive 2002/49/EC Annex II</b></p><p></p>    
            <p><i>For more information see also Help -> How it Works -> Noise Exposure</i></p>   
            <p><strong>People: </strong>the estimated number of people living in each building </p>
            <p><strong>Dwellings: </strong>the estimated number of dwellings for each building</p>
            <p><strong>Façade type Exposition: </strong>type of exposition for each building (type string)</p>
            <p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;"<b>1</b>" single dwellings</p>
           <p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;"<b>2</b>" apartment building - single façade type exposition</p>
           <p>&nbsp; &nbsp; &nbsp; &nbsp; &nbsp;"<b>3</b>" apartment building - multi façade type exposition</p>
           
           <html><head/><body></body></html>
            '''))



    def checkdata(self):
        if self.buildings_layer_comboBox.currentText() == "":
            QMessageBox.information(self, self.tr("opeNoise - Assign levels to people"),
                                    self.tr("Please specify buildings layer"))
            return False

        if self.receiver_points_population_field.currentText() == "":
            QMessageBox.information(self, self.tr("opeNoise - Assign levels to people"),
                                    self.tr("Please specify people field"))
            return False

        if self.dwellingCombobox.currentText() == "":
            QMessageBox.information(self, self.tr("opeNoise - Assign levels to people"),
                                    self.tr("Please specify dwellings field"))
            return False

        if self.methodComboBox.currentText() == "":
            QMessageBox.information(self, self.tr("opeNoise - Assign levels to people"),
                                    self.tr("Please specify façade type exposition field (type string)"))
            return False

    def populate_comboBox( self ):
        if Qgis.QGIS_VERSION_INT < 31401:
            self.receiver_points_layer_comboBox.clear()
        #self.receiver_points_layer_comboBox.setAllowEmptyLayer(True)
        self.receiver_points_layer_comboBox.setFilters(QgsMapLayerProxyModel.PointLayer)

        self.update_field_receiver_points_layer()

        if Qgis.QGIS_VERSION_INT < 31401:
            self.buildings_layer_comboBox.clear()
        self.buildings_layer_comboBox.setFilters(QgsMapLayerProxyModel.PolygonLayer)

        self.receiver_points_population_field.setLayer(self.buildings_layer_comboBox.currentLayer())
        self.dwellingCombobox.setLayer(self.buildings_layer_comboBox.currentLayer())
        self.methodComboBox.setLayer(self.buildings_layer_comboBox.currentLayer())
        # possibility to have a null field
        # self.receiver_points_population_field.setAllowEmptyFieldName(True)
        # self.dwellingCombobox.setAllowEmptyFieldName(True)
        # self.methodComboBox.setAllowEmptyFieldName(True)



        #self.buildings_layer_comboBox.addItems(buildings_layers)

    def outputTempTable(self,pddf,tablename,filedname,roundHundreds):
        vl = QgsVectorLayer("None", tablename, "memory")
        pr = vl.dataProvider()
        pr.addAttributes([QgsField("level_band", QVariant.String),
                          QgsField(filedname, QVariant.Double)])
        vl.updateFields()
        labelsLev = ["No level","<=35.0 dB(A)", "35 - 39 dB(A)", "40 - 44 dB(A)", "45 - 49 dB(A)",
                     "50 - 54 dB(A)", "55 - 59 dB(A)", "60 - 64 dB(A)", "65 - 69 dB(A)",
                     "70 - 74 dB(A)", "75 - 79 dB(A)", ">= 80 dB(A)"]
        for idx in range(len(pddf.values)):
            f = QgsFeature()
            if roundHundreds == True:
                f.setAttributes([labelsLev[idx], myround(pddf.values[idx])])
            else:
                f.setAttributes([labelsLev[idx], round(float(pddf.values[idx]), 2)])
            pr.addFeature(f)
        QgsProject.instance().addMapLayer(vl)

    def DETable(self,DF,tablename,fieldnames,type):
        vl = QgsVectorLayer("None", tablename, "memory")
        pr = vl.dataProvider()
        pr.addAttributes([QgsField("TOT_People", QVariant.Int)])
        for field in fieldnames:
            pr.addAttributes([QgsField(field, QVariant.Double)])
        vl.updateFields()

        totPopulation = DF.sum()["population"]

        f = QgsFeature()
        # doseeffetto
        # aggiungo colonna
        DF['level_half'] = [32, 32, 37, 42, 47, 52, 57, 62, 67, 72, 77, 82]
        if type == "den":

            # Lden
            DF['ARHA'] = (78.927 - 3.1162 * DF['level_half'] + 0.0342 * np.power((DF['level_half']), 2)) / 100
            DF['NHA'] = DF['population'] * DF['ARHA']
            # sommo solo gli ultimi 6
            NHAtotal = DF.iloc[-6:].sum()
            NHAperc = NHAtotal['NHA'] / totPopulation * 100
            #  write data in table
            f.setAttributes([float(round(totPopulation,0)),
                             float(round(NHAtotal['NHA'],0)),
                             float(round(NHAperc,1))])


        else:
            # Lnight
            DF['ARHSD'] = (19.4312 - 0.9336 * DF['level_half'] + 0.0126 * np.power(DF['level_half'], 2)) / 100
            DF['NHSD'] = DF['population'] * DF['ARHSD']
            # sommo gli ultimi 7 valori
            NHSDtotal = DF.iloc[-7:].sum()
            NHSDperc = NHSDtotal['NHSD'] / totPopulation * 100
            #  write data in table
            f.setAttributes([float(round(totPopulation,0)),
                             float(round(NHSDtotal["NHSD"],0)),
                             float(round(NHSDperc,1))])
        pr.addFeature(f)
        QgsProject.instance().addMapLayer(vl)



    def update_field_receiver_points_layer(self):

        if str(self.receiver_points_layer_comboBox.currentText()) == "":
            return

        receiver_points_layer = QgsProject.instance().mapLayersByName(self.receiver_points_layer_comboBox.currentText())[0]
        receiver_points_layer_fields = list(receiver_points_layer.dataProvider().fields())


        #self.id_field_comboBox.clear()
        self.level_1_comboBox.clear()
        self.level_2_comboBox.clear()


        receiver_points_layer_fields_number = [""]

        for f in receiver_points_layer_fields:
            if f.type() == QVariant.Int or f.type() == QVariant.Double:
                receiver_points_layer_fields_number.append(str(f.name()))

        if Qgis.QGIS_VERSION_INT < 31401:
            for f_label in receiver_points_layer_fields_number:
                #self.id_field_comboBox.addItem(f_label)
                self.level_1_comboBox.addItem(f_label)
                self.level_2_comboBox.addItem(f_label)



    def controls(self):
        self.run_buttonBox.setEnabled( False )
        if self.receiver_points_layer_comboBox.currentText() == "":
            QMessageBox.information(self, self.tr("opeNoise - Noise Exposure"), self.tr("Please specify receiver points layer"))
            return 0

        if self.level_1_comboBox.currentText() == "" and self.level_2_comboBox.currentText() == "":
               message = self.tr("Please specify noise level")
               QMessageBox.information(self, self.tr("opeNoise - Noise Exposure"), self.tr(message))
               return 0

        if self.buildings_layer_comboBox.currentText() == "":
            QMessageBox.information(self, self.tr("opeNoise - Noise Exposure"), self.tr("Please specify buildings layer"))
            return 0

        return 1

    def populate_receiver_points_fields(self):

        receiver_points_dict = {}

        receiver_points_dict['id_field'] = 'id_bui'

        if self.level_1_comboBox.currentText() == '':
            receiver_points_dict['level_1'] = 'none'
        else:
            receiver_points_dict['level_1'] = self.level_1_comboBox.currentText()

        if self.level_2_comboBox.currentText() == '':
            receiver_points_dict['level_2'] = 'none'
        else:
            receiver_points_dict['level_2'] = self.level_2_comboBox.currentText()



        return receiver_points_dict


    def check_oldFields(self):
        buildings_layer = QgsProject.instance().mapLayersByName(self.buildings_layer_comboBox.currentText())[0]
        buildings_layer = self.buildings_layer_comboBox.currentLayer()
        buildings_layer_fields = buildings_layer.fields()
        fields = [x.name() for x in buildings_layer_fields.toList()]

        # get period to assign
        fields_to_calculate = []
        if self.level_1_comboBox.currentText() != "":
            fields_to_calculate.append(self.level_1_comboBox.currentText())
        if self.level_2_comboBox.currentText() != "":
            fields_to_calculate.append(self.level_2_comboBox.currentText())


        #print("fields_to_calculate",fields_to_calculate)
        #personal_fields = ['Lgeneric', 'Lday', 'Levening', 'Lnight','Lden']
        fields_already_present = list(set(fields_to_calculate) & set(fields))
        if fields_already_present:
            overwrite_begin = self.tr("In buildings layer you already have the fields: ")
            overwrite_end = self.tr(" . Do you want to overwrite data in attribute table?")
            reply = QMessageBox.question(self, self.tr("opeNoise - Noise Exposure"),
                                           overwrite_begin + '\n' + str(fields_already_present) + overwrite_end, QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.No:
                reply2 = QMessageBox.question(self, self.tr("opeNoise - Noise Exposure"),
                                               self.tr("To mantain old data, copy them in a new field"), QMessageBox.Ok)
                return False
            else:
                fList = []
                for field_to_delete in fields_already_present:
                    idx_field = buildings_layer.dataProvider().fieldNameIndex(field_to_delete)
                    fList.append(idx_field)

                buildings_layer.dataProvider().deleteAttributes(fList)
                buildings_layer.updateFields()
                return True
        else:
            return True



    def accept(self):

        if self.checkdata() == False:
            return

        if self.controls() == 0:
            self.run_buttonBox.setEnabled( True )
            return

        self.run_buttonBox.setEnabled( False )


        self.log_start()
        receiver_points_layer = QgsProject.instance().mapLayersByName(self.receiver_points_layer_comboBox.currentText())[0]
        receiver_points_layer_details = self.populate_receiver_points_fields()
        buildings_layer = QgsProject.instance().mapLayersByName(self.buildings_layer_comboBox.currentText())[0]
        building_pop_Field = self.receiver_points_population_field.currentText()
        dwelling_Field = self.dwellingCombobox.currentText()
        methodPopField = self.methodComboBox.currentText()
        # checkbox controls
        if self.applyNoiseSimbology.isChecked():
            applySimbology = True
        else:
            applySimbology = False

        if self.hundredsCheck.isChecked():
            roundHundreds = True
        else:
            roundHundreds = False

        if self.checkDoseEffetto.isChecked():
            doseffetto = True
        else:
            doseffetto = False


        # CRS control (each layer must have the same CRS)
        if receiver_points_layer.crs().authid() != buildings_layer.crs().authid():
            QMessageBox.information(self, self.tr("opeNoise - Noise Exposure"), self.tr("The layers don't have the same CRS (Coordinate Reference System). Please use layers with same CRS"))
            self.run_buttonBox.setEnabled( True )
            return


        # check old fields in buildings
        if self.check_oldFields() == False:
            return


        self.time_start = datetime.now()

        # Run
        try:
            self.runLevelBuilding(receiver_points_layer,receiver_points_layer_details,buildings_layer,building_pop_Field,dwelling_Field,methodPopField,applySimbology,roundHundreds,doseffetto)
            run = 1
        except:
            error= traceback.format_exc()
            log_errors.write(error)
            run = 0

        self.time_end = datetime.now()

        if run == 1:
            log_errors.write(self.tr("No errors.") + "\n\n")
            result_string = self.tr("Noise exposure assigned successfully,\n in temporary scratch layer,\n with followings input settings:") + "\n\n" +\
                            self.tr("Receiver Points: ")+receiver_points_layer.name()+"\n"+ \
                            self.tr("Noise Levels Lden: ") + receiver_points_layer_details['level_1'] +"\n"+ \
                            self.tr("Noise Levels Lnight: ") + receiver_points_layer_details['level_2'] +"\n"+ \
                            self.tr("Buildings: ") + buildings_layer.name() + "\n"+ \
                            self.tr("People: ") + building_pop_Field + "\n" + \
                            self.tr("Dwellings: ") + dwelling_Field + "\n" + \
                            self.tr("Façade type exposition: ") + methodPopField + "\n\n" + \
                            self.tr("Start: ") + self.time_start.strftime("%a %d/%b/%Y %H:%M:%S") + "\n" +\
                            self.tr("End: ") + self.time_end.strftime("%a %d/%b/%Y %H:%M:%S") + "\n"+\
                            self.tr("Duration: ") + str(self.duration())
            QMessageBox.information(self, self.tr("opeNoise - Noise Exposure"), self.tr(result_string))
#            self.iface.messageBar().pushMessage(self.tr("opeNoise - Noise Exposure"), self.tr("Process complete"))
        else:
            result_string = self.tr("Sorry, process not complete.") + "\n\n" +\
                            self.tr("View the log file to understand the problem:") + "\n" +\
                            str(log_errors_path_name) + "\n\n" +\
                            self.tr("Start: ") + self.time_start.strftime("%a %d/%b/%Y %H:%M:%S.%f") + "\n" +\
                            self.tr("End: ") + self.time_end.strftime("%a %d/%b/%Y %H:%M:%S.%f") + "\n"+\
                            self.tr("Duration: ") + str(self.duration())
            QMessageBox.information(self, self.tr("opeNoise - Noise Exposure"), self.tr(result_string))
#            self.iface.messageBar().pushMessage(self.tr("opeNoise - Noise Exposure"), self.tr("Process not complete"))

        self.log_end()

        self.run_buttonBox.setEnabled( True )

#        self.iface.mainWindow().statusBar().clearMessage()
#        self.iface.mapCanvas().refresh()
        self.close()


    def duration(self):
        duration = self.time_end - self.time_start
        duration_h = duration.seconds // 3600
        duration_m = (duration.seconds // 60) % 60
        duration_s = duration.seconds
        duration_string = str(format(duration_h, '02')) + ':' + str(format(duration_m, '02')) + ':' + str(
            format(duration_s, '02'))
        return duration_string



    def log_start(self):

        global log_errors, log_errors_path_name
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        log_errors_path_name = os.path.join(dir_path,"log_AssignLevelsToBuildings_errors.txt")
        log_errors = open(log_errors_path_name,"w")
        log_errors.write(self.tr("opeNoise") + " - " + self.tr("Noise Exposure") + " - " + self.tr("Errors") + "\n\n")

    def log_end(self):

        log_errors.close()


    def EUpopCalculationMethod(self, popDic, buildingLevel,dwellings,Method,receiverFacadeDic):
        outPop = list()
        outDewlling = list()
        for id_bui in buildingLevel.keys():
            livelli = buildingLevel[id_bui]
            if popDic[id_bui] == qgisnull:
                abitanti = 0
            else:
                abitanti = popDic[id_bui]
            if dwellings[id_bui] == qgisnull:
                ndwelling = 0
            else:
                ndwelling = dwellings[id_bui]
            method = Method[id_bui]
            facade = receiverFacadeDic[id_bui]
            # metodo 1
            if method.endswith('1'):
                # method 1
                outPop.append([max(livelli), abitanti, id_bui])
                outDewlling.append([max(livelli), ndwelling, id_bui])

            # metodo 2
            elif method.endswith('2'):
                if len(receiverFacadeDic[id_bui]) == 0:
                    outPop.append([0, abitanti, id_bui])
                    outDewlling.append([0, ndwelling, id_bui])
                else:
                    for facadeLev in receiverFacadeDic[id_bui]:
                        facadeP = facadeLev[0]
                        livello = facadeLev[1]
                        outPop.append([livello, abitanti*facadeP/100., id_bui])
                        outDewlling.append([livello, ndwelling*facadeP/100., id_bui])

            else:
                # method 3
                # method3 - part1 - remove minimum value in case even receivers
                if len(livelli) % 2 != 0:
                    livelli.remove(min(livelli))

                # livelliFiltered = [x for x in livelli if x > mediane[id_bui][0]]
                a_list = sorted(livelli)
                half = len(a_list) // 2
                livelliFilteredLow = a_list[:half]
                livelliFilteredHi = a_list[half:]
                if len(livelliFilteredHi) == 0:
                    outPop.append([0, abitanti, id_bui])
                    outDewlling.append([0, ndwelling, id_bui])
                else:
                    for livello in livelliFilteredHi:
                        outPop.append([livello, abitanti / len(livelliFilteredHi), id_bui])
                        outDewlling.append([livello, ndwelling / len(livelliFilteredHi), id_bui])

        df1 = pd.DataFrame(outPop, columns=['levels', 'popolazione', 'id_bui'])
        df1Dwelling = pd.DataFrame(outDewlling, columns=['levels', 'dwellings', 'id_bui'])
        bins = pd.cut(df1['levels'], [-np.inf,0, 34.4, 39.4, 44.4, 49.4, 54.4, 59.4, 64.4, 69.4, 74.4, 79.4, np.inf])
        binsDwell = pd.cut(df1Dwelling['levels'], [-np.inf,0, 34.4, 39.4, 44.4, 49.4, 54.4, 59.4, 64.4, 69.4, 74.4, 79.4, np.inf])
        df2=df1.groupby(bins)['popolazione'].agg(['sum'])
        print('bins:',bins)
        print('df1',df1)
        df2Dwell = df1Dwelling.groupby(bins)['dwellings'].agg(['sum'])
        df3 = df2.rename({'sum': 'population'}, axis=1)
        df3Dwell = df2Dwell.rename({'sum': 'dwellings'}, axis=1)
        return df3,df3Dwell



    def runLevelBuilding(self,receiver_points_layer,receiver_points_layer_details,buildings_layer,building_pop_Field,dwelling_Field,method,applySimbology,roundHundreds,doseeffetto):

        CreateTempDir()

        # gets vector layers, features receiver points
        receiver_points_feat_total = receiver_points_layer.dataProvider().featureCount()
        receiver_points_feat_all = receiver_points_layer.dataProvider().getFeatures()

        # gets fields index from receiver points layer
        receiver_points_fields_index = {}
        receiver_points_fields_index['id_field'] = receiver_points_layer.dataProvider().fieldNameIndex(str(receiver_points_layer_details['id_field']))
        if receiver_points_layer_details['level_1'] != 'none':
            level_1_name = receiver_points_layer_details['level_1']
            receiver_points_fields_index['level_1'] = receiver_points_layer.dataProvider().fieldNameIndex(receiver_points_layer_details['level_1'])
        if receiver_points_layer_details['level_2'] != 'none':
            level_2_name = receiver_points_layer_details['level_2']
            receiver_points_fields_index['level_2'] = receiver_points_layer.dataProvider().fieldNameIndex(receiver_points_layer_details['level_2'])

        # gets fields from buildings layer and initializes the final buildings_levels_fields to populate the buildings layer attribute table
        buildings_fields_index = {}
        buildings_fields_number = int(buildings_layer.dataProvider().fields().count())
        if receiver_points_layer_details['level_1'] != 'none':
            buildings_fields_index['level_1'] = buildings_fields_number
            buildings_fields_number = buildings_fields_number + 1
        if receiver_points_layer_details['level_2'] != 'none':
            buildings_fields_index['level_2'] = buildings_fields_number
            buildings_fields_number = buildings_fields_number + 1


        receiver_points_feat_number = 0

        buildings_levels_fields = {}

        # dict storing values for building
        buildings_levels_from_receiverL1 = {}
        buildings_levels_from_receiverL2 = {}
        buildings_levels_from_receiverL3 = {}
        buildings_levels_from_receiverL4 = {}
        buildings_levels_from_receiverL5 = {}

        for featReceiver in receiver_points_feat_all:

            receiver_points_feat_number = receiver_points_feat_number + 1
            bar = receiver_points_feat_number/float(receiver_points_feat_total)*100
            self.progressBar.setValue(bar)

            feat_levels_fields = {}

            id_edi = featReceiver.attributes()[receiver_points_fields_index['id_field']]



            if receiver_points_layer_details['level_1'] != 'none':
                level_1 = featReceiver.attributes()[receiver_points_fields_index['level_1']]
                feat_levels_fields[buildings_fields_index['level_1']] = level_1
            if receiver_points_layer_details['level_2'] != 'none':
                level_2 = featReceiver.attributes()[receiver_points_fields_index['level_2']]
                feat_levels_fields[buildings_fields_index['level_2']] = level_2


            # assing maximum value level to building
            if (id_edi in buildings_levels_fields) == True:
                if receiver_points_layer_details['level_1'] != 'none':
                    if (buildings_levels_fields[id_edi][buildings_fields_index['level_1']] < level_1 and level_1 != None) or\
                      buildings_levels_fields[id_edi][buildings_fields_index['level_1']] == None:
                        buildings_levels_fields[id_edi][buildings_fields_index['level_1']] = level_1
                if receiver_points_layer_details['level_2'] != 'none':
                    if (buildings_levels_fields[id_edi][buildings_fields_index['level_2']] < level_2 and level_2 != None) or\
                      buildings_levels_fields[id_edi][buildings_fields_index['level_2']] == None:
                        buildings_levels_fields[id_edi][buildings_fields_index['level_2']] = level_2

            else:
                buildings_levels_fields[id_edi] = feat_levels_fields
        #     --------------
            if building_pop_Field != '':
                # Assigning dwellings and people living in dwellings to receiver points PAG 37 Directive 2020
                # creo dizionario che contiene per ogni edificio i livelli di ogni ricettore
                if receiver_points_layer_details['level_1'] != 'none':
                    if level_1 > 0: # filter in case level is -99
                        # add to dict only receiver different from -99
                        if id_edi in buildings_levels_from_receiverL1:
                            buildings_levels_from_receiverL1[id_edi].append(level_1)
                        else:
                            buildings_levels_from_receiverL1[id_edi] = [level_1]
                # print('buildingLelev:',buildings_levels_from_receiverL1)
                if receiver_points_layer_details['level_2'] != 'none':
                    if level_2 > 0:

                        if id_edi in buildings_levels_from_receiverL2:
                            buildings_levels_from_receiverL2[id_edi].append(level_2)
                        else:
                            buildings_levels_from_receiverL2[id_edi] = [level_2]


        # POPULATION PART -- ADDED PART
        if building_pop_Field != '':

            # extract population from building layer and store in
            buildingPop = dict()
            buildingDwell = dict()
            buildingMethod = dict()
            for bFeat in buildings_layer.getFeatures():
                buildingPop[bFeat.id()] = bFeat[building_pop_Field]
                buildingDwell[bFeat.id()] = bFeat[dwelling_Field]
                buildingMethod[bFeat.id()] = bFeat[method]

            # create a dict sto store facade perc for each receiver
            receiverFacadeDicL1 = dict()
            receiverFacadeDicL2 = dict()
            receiverFacadeDicL3 = dict()
            receiverFacadeDicL4 = dict()
            receiverFacadeDicL5 = dict()

            for recFeat in receiver_points_layer.getFeatures():
                key = recFeat['id_bui']
                if receiver_points_layer_details['level_1'] != 'none':
                    receiverFacadeDicL1.setdefault(key, [])
                    level_1 = recFeat.attributes()[receiver_points_fields_index['level_1']]
                    if level_1 > 0:
                        receiverFacadeDicL1[key].append([recFeat['facadeP'],level_1])

                if receiver_points_layer_details['level_2'] != 'none':
                    receiverFacadeDicL2.setdefault(key, [])
                    level_2 = recFeat.attributes()[receiver_points_fields_index['level_2']]
                    if level_2 > 0:
                        receiverFacadeDicL2[key].append([recFeat['facadeP'],level_2])

            # print('receiverFacadeDic: ',receiverFacadeDicL1)


            if receiver_points_layer_details['level_1'] != 'none':
                print('buildingPop: ',buildingPop,
                                                  'buildings_levels_from_receiverL1',buildings_levels_from_receiverL1,
                                                  'buildingDwell',buildingDwell,
                                                  'buildingMethod',buildingMethod,
                      'receiverFacadeDicL1',receiverFacadeDicL1)
                df1,df1Dwell = self.EUpopCalculationMethod(buildingPop,
                                                  buildings_levels_from_receiverL1,
                                                  buildingDwell,
                                                  buildingMethod,receiverFacadeDicL1)
                self.outputTempTable(df1,"People Exposure - Lden","people",roundHundreds)
                self.outputTempTable(df1Dwell, "Dwellings Exposure - Lden","dwellings",roundHundreds)
                if doseeffetto:
                    self.DETable(df1,"High Annoyance - Lden",["NHA","%NHA"],"den")
                print('L1 pop',df1)
            if receiver_points_layer_details['level_2'] != 'none':
                df2,df2Dwell = self.EUpopCalculationMethod(buildingPop,
                                                  buildings_levels_from_receiverL2,
                                                  buildingDwell,
                                                  buildingMethod,receiverFacadeDicL2)
                self.outputTempTable(df2,"People Exposure - Lnight","people",roundHundreds)
                self.outputTempTable(df2Dwell, "Dwellings Exposure - Lnight","dwellings",roundHundreds)
                if doseeffetto:
                    self.DETable(df2,"High Sleep Disturbance - Lnight",["NHSD","%NHSD"],"night")
                print('L2 pop',df2)
                print('Dose-Effetto: ',df2)

            #     print('L5 pop',df5)



            # del buildings_levels_from_receiverL2
            # del buildings_levels_from_receiverL3
            # del buildings_levels_from_receiverL4
            # del buildings_levels_from_receiverL5


        # -- end new part

        # puts the sound level in the buildings attribute table
        new_level_fields = []
        if receiver_points_layer_details['level_1'] != 'none':
            new_level_fields.append(QgsField(level_1_name, QVariant.Double,len=5,prec=1))
        if receiver_points_layer_details['level_2'] != 'none':
            new_level_fields.append(QgsField(level_2_name, QVariant.Double,len=5,prec=1))


        buildings_layer.dataProvider().addAttributes( new_level_fields )
        buildings_layer.updateFields()
        buildings_layer.dataProvider().changeAttributeValues(buildings_levels_fields)

        # render with noise colours
        level_fields_new = list(buildings_layer.dataProvider().fields())
        if len(level_fields_new) > 0 and applySimbology == True:
            on_ApplyNoiseSymbology.renderizeXY(buildings_layer, level_fields_new[len(level_fields_new) - 1].name())
