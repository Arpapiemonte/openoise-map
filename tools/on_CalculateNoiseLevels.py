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

#from PyQt4.QtGui import *
#from PyQt4.QtCore import *
from builtins import str

from qgis.PyQt.QtCore import QVariant
from qgis.core import QgsVectorLayer, QgsField, QgsProject, QgsVectorFileWriter, QgsWkbTypes, QgsFields, Qgis
from qgis.core import QgsGeometry, QgsFeature, QgsPointXY, QgsRectangle, QgsFeatureRequest,edit
from math import sqrt,log10
from qgis.utils import iface

import os,shutil
from numpy import  unique as npunique

from datetime import datetime

from . import on_RaysSearch
from . import on_Acoustics
from . import on_CreateEmissionPoints
from . import on_CreateDiffractionPoints
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

def create_wkt_from_list(li_points):
    # li_points must be a python list() of QgsPoint objects.

    wkt = 'MULTIPOINT('
    for point in li_points:
        x = point.x()
        y = point.y()
        wkt += '({} {}), '.format(x, y)
    wkt = wkt[:-1] + ')'
    return wkt


# computes distance (input two QgsPoints, return a float)
def compute_distance(QgsPoint1,QgsPoint2):
    return sqrt((QgsPoint1.x()-QgsPoint2.x())**2+(QgsPoint1.y()-QgsPoint2.y())**2)

def duration(time_start, time_end):
    duration = time_end - time_start
    duration_h = duration.seconds//3600
    duration_m = (duration.seconds//60)%60
    duration_s = duration.seconds
    duration_string = str(format(duration_h, '02')) + ':' + str(format(duration_m, '02')) + ':' + str(format(duration_s, '02'))
    return duration_string

def get_levels(settings,source_layer,source_feat):

    level_global = {}
    level_bands = {}

    # POWER_P
    if source_layer.geometryType() == QgsWkbTypes.PointGeometry and settings['implementation_pts'] == 'True':
        if settings['POWER_P_gen'] != None:
            level_global['Lgeneric'] = source_feat[ settings['POWER_P_gen'] ]
        if settings['POWER_P_day'] != None:
            level_global['Lday'] = source_feat[ settings['POWER_P_day'] ]
        if settings['POWER_P_eve'] != None:
            level_global['Levening'] = source_feat[ settings['POWER_P_eve'] ]
        if settings['POWER_P_nig'] != None:
            level_global['Lnight'] = source_feat[ settings['POWER_P_nig'] ]


        for key in list(level_global.keys()):
            level_bands[key] = on_Acoustics.GlobalToOctaveBands('pink',level_global[key])

    # POWER_R
    elif source_layer.geometryType() == QgsWkbTypes.LineGeometry and settings['implementation_roads'] == 'POWER_R':
        if settings['POWER_R_gen'] != None:
            level_global['Lgeneric'] = source_feat[ settings['POWER_R_gen'] ]
        if settings['POWER_R_day'] != None:
            level_global['Lday'] = source_feat[ settings['POWER_R_day'] ]
        if settings['POWER_R_eve'] != None:
            level_global['Levening'] = source_feat[ settings['POWER_R_eve'] ]
        if settings['POWER_R_nig'] != None:
            level_global['Lnight'] = source_feat[ settings['POWER_R_nig'] ]


        for key in list(level_global.keys()):
            # fix_print_with_import

            level_bands[key] = on_Acoustics.GlobalToOctaveBands('ISO_traffic_road',level_global[key])

    # NMPB
    elif source_layer.geometryType() == QgsWkbTypes.LineGeometry and settings['implementation_roads'] == 'NMPB':

        NMPB_keys = ['l_n','l_s','h_n','h_s','type']

        input_dict = {}

        if settings['NMPB_slope']:
            input_dict['slope'] = source_feat.attributes()[source_layer.dataProvider().fieldNameIndex(settings['NMPB_slope'])]
        else:
            input_dict['slope'] = 'flat'

        if settings['NMPB_surface']:
            input_dict['surface'] = source_feat.attributes()[source_layer.dataProvider().fieldNameIndex(settings['NMPB_surface'])]
        else:
            input_dict['surface'] = 'smooth'

        if settings['period_roads_gen'] == 'True':
            for key in NMPB_keys:
                key_setting = 'NMPB_gen_' + key
                if settings[key_setting] is not None:
                    input_dict[key] = source_feat.attributes()[source_layer.dataProvider().fieldNameIndex(settings[key_setting])]

            level_bands['Lgeneric'] = on_Acoustics.NMPB(input_dict).bands()
            level_global['Lgeneric'] = on_Acoustics.OctaveBandsToGlobal(level_bands['Lgeneric'])



        if settings['period_roads_day'] == 'True':
            for key in NMPB_keys:
                key_setting = 'NMPB_day_' + key
                if settings[key_setting] is not None:
                    input_dict[key] = source_feat.attributes()[source_layer.dataProvider().fieldNameIndex(settings[key_setting])]

            level_bands['Lday'] = on_Acoustics.NMPB(input_dict).bands()
            level_global['Lday'] = on_Acoustics.OctaveBandsToGlobal(level_bands['Lday'])

        if settings['period_roads_eve'] == 'True':
            for key in NMPB_keys:
                key_setting = 'NMPB_eve_' + key
                if settings[key_setting] is not None:
                    input_dict[key] = source_feat.attributes()[source_layer.dataProvider().fieldNameIndex(settings[key_setting])]

            level_bands['Levening'] = on_Acoustics.NMPB(input_dict).bands()
            level_global['Levening'] = on_Acoustics.OctaveBandsToGlobal(level_bands['Levening'])

        if settings['period_roads_nig'] == 'True':
            for key in NMPB_keys:
                key_setting = 'NMPB_nig_' + key
                if settings[key_setting] is not None:
                    input_dict[key] = source_feat.attributes()[source_layer.dataProvider().fieldNameIndex(settings[key_setting])]

            level_bands['Lnight'] = on_Acoustics.NMPB(input_dict).bands()
            level_global['Lnight'] = on_Acoustics.OctaveBandsToGlobal(level_bands['Lnight'])

    # CNOSSOS
    elif source_layer.geometryType() == QgsWkbTypes.LineGeometry and settings['implementation_roads'] == 'CNOSSOS':

        CNOSSOS_keys = ['1_n','1_s','2_n','2_s','3_n','3_s','4a_n','4a_s','4b_n','4b_s']

        input_dict = {}

        if settings['CNOSSOS_slope']:
            try:
                input_dict['slope'] = float(source_feat.attributes()[source_layer.dataProvider().fieldNameIndex(settings['CNOSSOS_slope'])])
            except:
                input_dict['slope'] = 0

        if settings['CNOSSOS_surface']:
            try:
                input_dict['surface'] = source_feat.attributes()[source_layer.dataProvider().fieldNameIndex(settings['CNOSSOS_surface'])]
            except:
                input_dict['surface'] = '0'

        input_dict['5_s'] = 0
        input_dict['5_n'] = 0
        input_dict['1_qstudd'] = 0
        input_dict['Ts'] = 0
        input_dict['k'] = 'k=1'
        input_dict['dist_intersection'] = 100
        input_dict['temperature'] = int(settings['temperature'])

        if settings['period_roads_gen'] == 'True':
            for key in CNOSSOS_keys:
                key_setting = 'CNOSSOS_gen_' + key
                if settings[key_setting] is not None:
                    input_dict[key] = source_feat.attributes()[source_layer.dataProvider().fieldNameIndex(settings[key_setting])]

            level_bands['Lgeneric'] = on_Acoustics.CNOSSOS(input_dict).bands()
            level_global['Lgeneric'] = on_Acoustics.OctaveBandsToGlobalA(level_bands['Lgeneric'])


        if settings['period_roads_day'] == 'True':
            for key in CNOSSOS_keys:
                key_setting = 'CNOSSOS_day_' + key
                if settings[key_setting] is not None:
                    input_dict[key] = source_feat.attributes()[source_layer.dataProvider().fieldNameIndex(settings[key_setting])]

            level_bands['Lday'] = on_Acoustics.CNOSSOS(input_dict).bands()
            level_global['Lday'] = on_Acoustics.OctaveBandsToGlobalA(level_bands['Lday'])

        if settings['period_roads_eve'] == 'True':
            for key in CNOSSOS_keys:
                key_setting = 'CNOSSOS_eve_' + key
                if settings[key_setting] is not None:
                    input_dict[key] = source_feat.attributes()[source_layer.dataProvider().fieldNameIndex(settings[key_setting])]

            level_bands['Levening'] = on_Acoustics.CNOSSOS(input_dict).bands()
            level_global['Levening'] = on_Acoustics.OctaveBandsToGlobalA(level_bands['Levening'])

        if settings['period_roads_nig'] == 'True':
            for key in CNOSSOS_keys:
                key_setting = 'CNOSSOS_nig_' + key
                if settings[key_setting] is not None:
                    input_dict[key] = source_feat.attributes()[source_layer.dataProvider().fieldNameIndex(settings[key_setting])]

            level_bands['Lnight'] = on_Acoustics.CNOSSOS(input_dict).bands()
            level_global['Lnight'] = on_Acoustics.OctaveBandsToGlobalA(level_bands['Lnight'])


    levels = {}
    levels['global'] = level_global
    levels['bands'] = level_bands

    # print("levels",levels)
    return levels


def calc(progress_bars, totalBar,receiver_layer, source_pts_layer, source_roads_layer, settings, level_field_index, obstacles_layer, rays_writer, diff_rays_writer, diff3D_rays_writer):

    # partialPercBar store the corresponding partial for each progressbar. Six in total and grouped un one main ProgressBar is 100/
    partialPercBar = 100/6.
    research_ray = int(settings['research_ray'])
    temperature = int(settings['temperature'])
    humidity = int(settings['humidity'])

    time = datetime.now()

    # create variable if skip diffraction flag is active
    if settings['skip_diffraction'] == "True":
        skip_diffraction = True
    else:
        skip_diffraction = False

    print('Diffraction')

    # 3D calculation tool
    if settings['threedglobal'] == 'True':
        Diff3d = True
    else:
        Diff3d =False

    ## create diffraction points
    print(obstacles_layer is not None)
    print(skip_diffraction is False)
    if obstacles_layer is not None and skip_diffraction is False:
        print('create diffraction points')
        bar = progress_bars['create_dif']['bar']

        diffraction_points_layer_path = os.path.abspath(os.path.join(temp_dir + os.sep + "diffraction_pts.shp"))

        on_CreateDiffractionPoints.run(bar,obstacles_layer.source(),diffraction_points_layer_path,totalBar)
        diffraction_layer_name = 'diff'
        diffraction_layer = QgsVectorLayer(diffraction_points_layer_path,diffraction_layer_name,"ogr")

        progress_bars['create_dif']['label'].setText('Done in ' + duration(time,datetime.now()) )
#        print 'crea diffraction points ',datetime.now() - time
        time = datetime.now()
    else:
        totalBar.setValue(partialPercBar)


    # Create emission layer that will contain all the emission pts from source_pts and source_roads
    emission_pts_layer_path = os.path.abspath(os.path.join(temp_dir + os.sep + "emission_pts.shp"))
    # emission_pts_fields = [QgsField("type", QVariant.String),
    #                        QgsField("id_source", QVariant.Int),
    #                        QgsField("segment", QVariant.String),]
    emission_pts_fields = QgsFields()
    emission_pts_fields.append(QgsField("type", QVariant.String))
    emission_pts_fields.append(QgsField("id_source", QVariant.Int))
    emission_pts_fields.append(QgsField("segment", QVariant.String))


    emission_pts_writer = QgsVectorFileWriter(emission_pts_layer_path, "System",
                                              emission_pts_fields, QgsWkbTypes.Point,
                                              receiver_layer.crs(), "ESRI Shapefile")

    bar = progress_bars['prepare_emi']['bar']
    bar.setValue(1)

    source_feat_all_dict = {}

    # pts source layer to emission pts layer
    if source_pts_layer is not None:
        # get emission levels and add feat to emission pts layer
        source_pts_levels_dict = {}
        source_pts_feat_all = source_pts_layer.dataProvider().getFeatures()
        for source_feat in source_pts_feat_all:
            # get emission values
            levels = get_levels(settings,source_pts_layer,source_feat)
            source_pts_levels_dict[source_feat.id()] = levels

            # add feat to emission pts layer
            source_feat.setAttributes(['pt',source_feat.id(),None])
            emission_pts_writer.addFeature(source_feat)


    # roads source layer to emission pts layer
    # output emission_pts_writer layer
    if source_roads_layer is not None:

        if settings['save_emission'] == 'True':
            saveEmi = True
        else:
            saveEmi = False

        ## create emission points from roads source
        emission_pts_roads_layer_path = os.path.abspath(os.path.join(temp_dir + os.sep + "emission_pts_roads.shp"))
        on_CreateEmissionPoints.run(source_roads_layer.source(),receiver_layer.source(),emission_pts_roads_layer_path,research_ray)

        emission_pts_roads_layer = QgsVectorLayer(emission_pts_roads_layer_path,'emission_pts_roads',"ogr")

        # get levels from the road source
        source_roads_levels_dict = {}
        source_roads_feat_all = source_roads_layer.dataProvider().getFeatures()
        for source_feat in source_roads_feat_all:
            levels = get_levels(settings, source_roads_layer, source_feat)
            source_roads_levels_dict[source_feat.id()] = levels

        if saveEmi == True:
            # check thathe the field Emission is not already present, in case I will create it
            if settings['period_pts_gen'] == "True" or settings['period_roads_gen'] == "True":
                if 'Lgeneric' not in source_roads_layer.fields().names():
                    source_roads_dataprovider = source_roads_layer.dataProvider()
                    source_roads_dataprovider.addAttributes([QgsField('Lgeneric',
                                                                      QVariant.Double, len=5, prec=1)])
                    source_roads_layer.updateFields()
            if settings['period_pts_day'] == "True" or settings['period_roads_day'] == "True":
                if 'Lday' not in source_roads_layer.fields().names():
                    source_roads_dataprovider = source_roads_layer.dataProvider()
                    source_roads_dataprovider.addAttributes([QgsField('Lday',
                                                                      QVariant.Double, len=5, prec=1)])
                    source_roads_layer.updateFields()
            if settings['period_pts_eve'] == "True" or settings['period_roads_eve'] == "True":
                if 'Levening' not in source_roads_layer.fields().names():
                    source_roads_dataprovider = source_roads_layer.dataProvider()
                    source_roads_dataprovider.addAttributes([QgsField('Levening',
                                                                      QVariant.Double, len=5, prec=1)])
                    source_roads_layer.updateFields()
            if settings['period_pts_nig'] == "True" or settings['period_roads_nig'] == "True":
                if 'Lnight' not in source_roads_layer.fields().names():
                    source_roads_dataprovider = source_roads_layer.dataProvider()
                    source_roads_dataprovider.addAttributes([QgsField('Lnight',
                                                                      QVariant.Double, len=5, prec=1)])
                    source_roads_layer.updateFields()

            with edit(source_roads_layer):
                for source_feat in source_roads_layer.getFeatures():
                    levelsEmi = source_roads_levels_dict[source_feat.id()]
                    if settings['period_pts_gen'] == "True" or settings['period_roads_gen'] == "True":
                        source_feat['Lgeneric'] = levelsEmi['global']['Lgeneric']
                        source_roads_layer.updateFeature(source_feat)
                    if settings['period_pts_day'] == "True" or settings['period_roads_day'] == "True":
                        source_feat['Lday'] = levelsEmi['global']['Lday']
                        source_roads_layer.updateFeature(source_feat)
                    if settings['period_pts_eve'] == "True" or settings['period_roads_eve'] == "True":
                        source_feat['Levening'] = levelsEmi['global']['Levening']
                        source_roads_layer.updateFeature(source_feat)
                    if settings['period_pts_nig'] == "True" or settings['period_roads_nig'] == "True":
                        source_feat['Lnight'] = levelsEmi['global']['Lnight']
                        source_roads_layer.updateFeature(source_feat)






        # add roads pts to emission pts layer
        source_pts_roads_feat_all = emission_pts_roads_layer.dataProvider().getFeatures()

        for source_feat in source_pts_roads_feat_all:
            id_source = source_feat['id_source']
            segment_source = source_feat['d_rTOe'] # Pierluigi -- corretto perchè chiamava segment

            # add feat to emission pts layer
            source_feat.setAttributes(['road',id_source,segment_source])
            emission_pts_writer.addFeature(source_feat)

    del emission_pts_writer

    # Create dict with all the data
    source_feat_all_dict = {}
    source_layer = QgsVectorLayer(emission_pts_layer_path,'emission pts',"ogr")
    source_feat_all = source_layer.dataProvider().getFeatures()
    source_feat_total = source_layer.dataProvider().featureCount()
    source_feat_number = 0

    for source_feat in source_feat_all:

        source_feat_number = source_feat_number + 1
        barValue = source_feat_number/float(source_feat_total)*100
        bar.setValue(barValue)

        # totalbar prepare_emi
        totalBar.setValue(barValue/6+100/6)


        type_source = source_feat['type']
        id_source = source_feat['id_source']
        segment = source_feat['segment']

        if type_source == 'pt':
            levels = source_pts_levels_dict[id_source]

        if type_source == 'road':
            levels = source_roads_levels_dict[id_source]

        value = {}
        value['type'] = type_source
        value['feat'] = source_feat
        value['global'] = levels['global']
        value['bands'] = levels['bands']
        value['segment'] = segment
        source_feat_all_dict[source_feat.id()] = value

    ## get data
    # receiver layer
    receiver_feat_all = receiver_layer.dataProvider().getFeatures()
    receiver_feat_total = receiver_layer.dataProvider().featureCount()
    receiver_feat_number = 0


    # obstacles layer
    if obstacles_layer is not None:
        obstacles_feat_all = obstacles_layer.dataProvider().getFeatures()
        obstacles_feat_all_dict = {}
        for obstacles_feat in obstacles_feat_all:
            obstacles_feat_all_dict[obstacles_feat.id()] = obstacles_feat

        # diffraction layer
        if skip_diffraction is False:
            print('skip diffraction deactivate')
            diff_feat_all = diffraction_layer.dataProvider().getFeatures()
            diff_feat_all_dict = {}
            for diff_feat in diff_feat_all:
                diff_feat_all_dict[diff_feat.id()] = diff_feat

    progress_bars['prepare_emi']['label'].setText('Done in ' + duration(time,datetime.now()) )
    # fix_print_with_import
    print('get acoustic data',datetime.now() - time)
    time = datetime.now()

    if obstacles_layer is None:

        bar = progress_bars['recTOsou']['bar']

        recTOsource_dict,dict3D = on_RaysSearch.run(bar,receiver_layer.source(),source_layer.source(),None,research_ray,totalBar,False)


        progress_bars['recTOsou']['label'].setText('Done in ' + duration(time,datetime.now()) )

        # fix_print_with_import
        print('find connections receivers sources ',datetime.now() - time)
        time = datetime.now()
        diffTOsource_dict = {}
        recTOdiff_dict = {}

    else:
        ### recTOsou
        bar = progress_bars['recTOsou']['bar']
        recTOsource_dict,dict3D = on_RaysSearch.run(bar,receiver_layer.source(),source_layer.source(),obstacles_layer.source(),research_ray,totalBar,False)

        progress_bars['recTOsou']['label'].setText('Done in ' + duration(time,datetime.now()) )

        # fix_print_with_import
        print('find connections receceivers sources ',datetime.now() - time)
        time = datetime.now()

        ### difTOsou
        bar = progress_bars['difTOsou']['bar']

        # skip diffraction here
        if skip_diffraction is False:
            diffTOsource_dict, dict3Dnotused = on_RaysSearch.run(bar,diffraction_layer.source(),source_layer.source(),obstacles_layer.source(),research_ray,totalBar,True)

        else:
            diffTOsource_dict = {}
            totalBar.setValue(100 / 6 * 4)
        progress_bars['difTOsou']['label'].setText('Done in ' + duration(time,datetime.now()) )

        # fix_print_with_import
        print('find connections diffraction points - sources',datetime.now() - time)
        time = datetime.now()

        ### recTOdif
        bar = progress_bars['recTOdif']['bar']

#        recTOdiff_dict = on_RaysSearch.run_selection_distance(bar,receiver_layer.source(),diffraction_layer.source(),obstacles_layer.source(),research_ray,diffTOsource_dict,source_layer.source())
        if skip_diffraction is False:
            recTOdiff_dict = on_RaysSearch.run_selection(bar,receiver_layer.source(),diffraction_layer.source(),obstacles_layer.source(),research_ray,diffTOsource_dict,totalBar)

        else:
            recTOdiff_dict = {}
            totalBar.setValue(100 / 6. * 5)
        progress_bars['recTOdif']['label'].setText('Done in ' + duration(time,datetime.now()) )

        # fix_print_with_import
        print('find connections receivers - diffraction points',datetime.now() - time)
        time = datetime.now()


    ray_id = 0
    diff_ray_id = 0
    diff3D_ray_id = 0

    receiver_feat_all_new_fields =  {}

    bar = progress_bars['calculate']['bar']

    for receiver_feat in receiver_feat_all:
        # Bug correction in case of receiver inside a building
        # we exclude the receiver from calculus
        Skip_intersection = False
        if obstacles_layer is not None:
            obstacles_feat_all = obstacles_layer.dataProvider().getFeatures()
            for obstacles_feat in obstacles_feat_all:
                if receiver_feat.geometry().intersects(obstacles_feat.geometry()):
                    Skip_intersection = True



        receiver_feat_number = receiver_feat_number + 1
        barValue = receiver_feat_number/float(receiver_feat_total)*100
        bar.setValue(barValue)
        # totalbar calculate
        totalBar.setValue(barValue/6+100/6*5)

        receiver_feat_new_fields = {}

        # initializes the receiver point lin level
        receiver_point_lin_level = {}
        receiver_point_lin_level['Lgeneric'] = 0
        receiver_point_lin_level['Lday'] = 0
        receiver_point_lin_level['Levening'] = 0
        receiver_point_lin_level['Lnight'] = 0

        if Skip_intersection == False:

            if receiver_feat.id() in recTOsource_dict:

                    source_ids = recTOsource_dict[receiver_feat.id()]

                    for source_id in source_ids:

                        source_feat_value = source_feat_all_dict[source_id]

                        source_feat = source_feat_value['feat']

                        ray_geometry = QgsGeometry.fromPolylineXY( [ receiver_feat.geometry().asPoint() , source_feat.geometry().asPoint() ] )

                        d_recTOsource = compute_distance(receiver_feat.geometry().asPoint(),source_feat.geometry().asPoint())
                        # length with receiver points height fixed to 4 m

                        if settings['custom3d'] == "True":
                            receiver_height= float(receiver_feat[settings['custom3dfield']])
                            d_recTOsource_4m = sqrt(d_recTOsource ** 2 + receiver_height**2)
                        else:
                            d_recTOsource_4m = sqrt(d_recTOsource**2 + 16)

                        feat_type = source_feat_value['type']
                        level_emi = source_feat_value['global']
                        level_emi_bands = source_feat_value['bands']
                        segment = source_feat_value['segment']

                        level_dir = {}
                        level_atm_bands = {}

                        geo_attenuation = on_Acoustics.GeometricalAttenuation('spherical',d_recTOsource_4m)
                        # print("d_recTOsource_4m",d_recTOsource_4m)
                        # print("geo_attenuation",geo_attenuation)

                        for key in list(level_emi.keys()):
                            if level_emi[key] > 0:
                                level_atm_bands[key] = on_Acoustics.AtmosphericAbsorption(d_recTOsource_4m,temperature,humidity,level_emi_bands[key]).level()
                                #level_dir[key] = on_Acoustics.OctaveBandsToGlobal(level_atm_bands[key]) - geo_attenuation

                                # print("level_atm_bands[key]",level_atm_bands[key])
                                if settings['implementation_roads'] == 'CNOSSOS':
                                    level_dir[key] = on_Acoustics.OctaveBandsToGlobalA(level_atm_bands[key]) - geo_attenuation
                                else:
                                    level_dir[key] = on_Acoustics.OctaveBandsToGlobal(level_atm_bands[key]) - geo_attenuation
                                    # print("level_dir[key]",level_dir[key])

                                # correction for the segment lenght
                                if feat_type == 'road':
                                    if (settings['implementation_roads'] == 'POWER_R' or settings['implementation_roads'] == 'NMPB'):
                                        level_dir[key] = level_dir[key] + 20 + 10*log10(float(segment)) + 3
                                    if settings['implementation_roads'] == 'CNOSSOS':
                                        level_dir[key] = level_dir[key] + 10*log10(float(segment)) + 3

                                receiver_point_lin_level[key] = receiver_point_lin_level[key] + 10**(level_dir[key]/float(10))
                            else:
                                #
                                level_dir[key] = -1


                        if rays_writer is not None:
                            ray = QgsFeature()
                            ray.setGeometry(ray_geometry)
                            attributes = [ray_id, receiver_feat.id(), source_feat.id(), d_recTOsource, d_recTOsource_4m]

                            if settings['period_pts_gen'] == "True" or settings['period_roads_gen'] == "True":
                                if 'Lgeneric' in level_emi:
                                    attributes.append(level_emi['Lgeneric'])
                                    attributes.append(level_dir['Lgeneric'])
                                else:
                                    attributes.append(None)
                                    attributes.append(None)
                            if settings['period_pts_day'] == "True" or settings['period_roads_day'] == "True":
                                if 'Lday' in level_emi:
                                    attributes.append(level_emi['Lday'])
                                    attributes.append(level_dir['Lday'])
                                else:
                                    attributes.append(None)
                                    attributes.append(None)
                            if settings['period_pts_eve'] == "True" or settings['period_roads_eve'] == "True":
                                if 'Levening' in level_emi:
                                    attributes.append(level_emi['Levening'])
                                    attributes.append(level_dir['Levening'])
                                else:
                                    attributes.append(None)
                                    attributes.append(None)
                            if settings['period_pts_nig'] == "True" or settings['period_roads_nig'] == "True":
                                if 'Lnight' in level_emi:
                                    attributes.append(level_emi['Lnight'])
                                    attributes.append(level_dir['Lnight'])
                                else:
                                    attributes.append(None)
                                    attributes.append(None)

                            ray.setAttributes(attributes)
                            rays_writer.addFeature(ray)
                            ray_id = ray_id + 1


            # added condition skip for diffraction
            if skip_diffraction is False:
                if receiver_feat.id() in recTOdiff_dict:

                    diff_ids = recTOdiff_dict[receiver_feat.id()]

                    for diff_id in diff_ids:

                        diff_feat = diff_feat_all_dict[diff_id]

                        if diff_feat.id() in diffTOsource_dict:

                            source_ids = diffTOsource_dict[diff_feat.id()]

                            for source_id in source_ids:

                                source_feat_value = source_feat_all_dict[source_id]

                                source_feat = source_feat_value['feat']

                                if receiver_feat.id() in recTOsource_dict:
                                    source_ids = recTOsource_dict[receiver_feat.id()]
                                    if source_feat.id() in source_ids:
                                        shadow = 0
                                    else:
                                        shadow = 1
                                else:
                                    shadow = 1

                                if shadow == 1:

                                    ray_geometry = QgsGeometry.fromPolylineXY( [ receiver_feat.geometry().asPoint() , diff_feat.geometry().asPoint() , source_feat.geometry().asPoint()] )

                                    d_recTOdiff = compute_distance(receiver_feat.geometry().asPoint(),diff_feat.geometry().asPoint())
                                    d_diffTOsource = compute_distance(diff_feat.geometry().asPoint(),source_feat.geometry().asPoint())
                                    # case of custom height receiver only difftction point to source is affected
                                    if settings['custom3d'] == "True":
                                        receiver_height = float(receiver_feat[settings['custom3dfield']])
                                    else:
                                        receiver_height = 4
                                    d_diffTOsource = sqrt(d_diffTOsource ** 2 + receiver_height ** 2)
                                    d_recTOsource =  compute_distance(receiver_feat.geometry().asPoint(),source_feat.geometry().asPoint())
                                    d_recPLUSsource = d_recTOdiff + d_diffTOsource

                                    if d_recPLUSsource <= research_ray:

                                        feat_type = source_feat_value['type']
                                        level_emi = source_feat_value['global']
                                        level_emi_bands = source_feat_value['bands']
                                        segment = source_feat_value['segment']

                                        level_dif = {}
                                        level_dif_bands = {}
                                        level_atm_bands = {}

                                        for key in list(level_emi_bands.keys()):
                                            if level_emi[key] > 0:

                                                level_dif_bands[key] = on_Acoustics.Diffraction('CNOSSOS',level_emi_bands[key],d_diffTOsource,d_recTOsource,d_recTOdiff,temperature).level()
                                                level_atm_bands[key] = on_Acoustics.AtmosphericAbsorption(d_recPLUSsource,temperature,humidity,level_emi_bands[key]).attenuation()
                                                level_dif_bands[key] = on_Acoustics.DiffBands(level_dif_bands[key],
                                                                                              level_atm_bands[key])
                                                #level_dif[key] = on_Acoustics.OctaveBandsToGlobal(level_dif_bands[key])

                                                #print("settings: ", settings['implementation_roads'])

                                                if settings['implementation_roads'] == 'CNOSSOS':
                                                    level_dif[key] = on_Acoustics.OctaveBandsToGlobalA(level_dif_bands[key])
                                                else:
                                                    level_dif[key] = on_Acoustics.OctaveBandsToGlobal(level_dif_bands[key])

                                                # correction for the segment lenght
                                                if feat_type == 'road':
                                                    if (settings['implementation_roads'] == 'POWER_R' or settings['implementation_roads'] == 'NMPB'):
                                                        level_dif[key] = level_dif[key] + 20 + 10*log10(float(segment)) + 3
                                                    if settings['implementation_roads'] == 'CNOSSOS':
                                                        level_dif[key] = level_dif[key] + 10*log10(float(segment)) + 3

                                                receiver_point_lin_level[key] = receiver_point_lin_level[key] + 10**(level_dif[key]/float(10))

                                            else:
                                                level_dif[key] = -1


                                        if diff_rays_writer is not None:
                                            ray = QgsFeature()
                                            ray.setGeometry(ray_geometry)
                                            attributes = [diff_ray_id, receiver_feat.id(), diff_feat.id(), source_feat.id(),
                                                          d_recTOdiff, d_diffTOsource, d_recTOsource]

                                            if settings['period_pts_gen'] == "True" or settings['period_roads_gen'] == "True":
                                                if 'Lgeneric' in level_emi:
                                                    attributes.append(level_emi['Lgeneric'])
                                                    attributes.append(level_dif['Lgeneric'])
                                                else:
                                                    attributes.append(None)
                                                    attributes.append(None)
                                            if settings['period_pts_day'] == "True" or settings['period_roads_day'] == "True":
                                                if 'Lday' in level_emi:
                                                    attributes.append(level_emi['Lday'])
                                                    attributes.append(level_dif['Lday'])
                                                else:
                                                    attributes.append(None)
                                                    attributes.append(None)
                                            if settings['period_pts_eve'] == "True" or settings['period_roads_eve'] == "True":
                                                if 'Levening' in level_emi:
                                                    attributes.append(level_emi['Levening'])
                                                    attributes.append(level_dif['Levening'])
                                                else:
                                                    attributes.append(None)
                                                    attributes.append(None)
                                            if settings['period_pts_nig'] == "True" or settings['period_roads_nig'] == "True":
                                                if 'Lnight' in level_emi:
                                                    attributes.append(level_emi['Lnight'])
                                                    attributes.append(level_dif['Lnight'])
                                                else:
                                                    attributes.append(None)
                                                    attributes.append(None)

                                            ray.setAttributes(attributes)
                                            diff_rays_writer.addFeature(ray)
                                            diff_ray_id = diff_ray_id + 1

            # calcolo in 3D
            if Diff3d is True:
                if receiver_feat.id() in dict3D:
                    source_ids = npunique(dict3D[receiver_feat.id()]).tolist()
                    for source_id in source_ids:

                        source_feat_value = source_feat_all_dict[source_id]
                        sor_feat = source_feat_value['feat']


                        # build 2D plane line
                        sorgente_punto = sor_feat.geometry().asPoint()
                        ricevitori_punto = receiver_feat.geometry().asPoint()
                        line = QgsGeometry.fromPolylineXY([sorgente_punto, ricevitori_punto])

                        p1 = QgsPointXY(0, 0)
                        punti_hull = [p1]

                        if settings['custom3d'] == "True":
                            receiver_height3D = float(receiver_feat[settings['custom3dfield']])
                            pLast = QgsPointXY(line.length(), receiver_height3D)
                        else:
                            pLast = QgsPointXY(line.length(), 4)
                        # definisco un rettangolo di ricerca per optimizing loop
                        x_min = min(sorgente_punto.x(), ricevitori_punto.x())
                        x_max = max(sorgente_punto.x(), ricevitori_punto.x())
                        y_min = min(sorgente_punto.y(), ricevitori_punto.y())
                        y_max = max(sorgente_punto.y(), ricevitori_punto.y())
                        rect = QgsRectangle(x_min, y_min, x_max, y_max)
                        request = QgsFeatureRequest().setFilterRect(rect).setFlags(QgsFeatureRequest.ExactIntersect)

                        # cycle to intersect the line with obstacles
                        # output is a 3D vertical line
                        for f in obstacles_layer.getFeatures(request):
                            if f.geometry().intersects(line):
                                intersezione = line.intersection(f.geometry())

                                # prendo i punti della intersezione
                                if intersezione.isMultipart():
                                    poly=intersezione.asMultiPolyline()
                                    for ii in poly:
                                        for jj in ii:
                                            distanza = line.lineLocatePoint(QgsGeometry().fromPointXY((jj)))
                                            # call column contaning 3D building height
                                            fieldH = settings['field3D']
                                            elev = f[fieldH]
                                            if elev <= 3.:
                                                elev = 3.
                                            punti_hull.append(QgsPointXY(distanza, elev))

                                else:
                                    poly = intersezione.asPolyline()

                                    # distanza dal punto iniziale
                                    for pti in poly:
                                        distanza = line.lineLocatePoint(QgsGeometry().fromPointXY((pti)))
                                        # call column contaning 3D building height
                                        fieldH = settings['field3D']
                                        elev = f[fieldH]
                                        if elev <= 3.:
                                            elev = 3.
                                        punti_hull.append(QgsPointXY(distanza, elev))

                        punti_hull.append(pLast)
                        polygon_wkt = create_wkt_from_list(punti_hull)
                        multipoint = QgsGeometry.fromWkt(polygon_wkt)
                        out_ring = multipoint.convexHull()

                        dInclinata = compute_distance(p1,pLast)
                        distSUP3D = out_ring.length() - dInclinata
                        # determination of epsilon
                        if len(out_ring.asPolygon()[0][1:-2])==1:
                            ePoints = out_ring.asPolygon()[0][1:-1]
                        else:
                            ePoints = out_ring.asPolygon()[0][1:-2]
                        eLine = QgsGeometry.fromPolylineXY(ePoints)
                        epsilon=eLine.length()


                        level_emi = source_feat_value['global']
                        level_emi_bands = source_feat_value['bands']


                        level_dif = {}
                        level_dif_bands = {}
                        level_atm_bands = {}

                        # LA PARTE SEGUENTE CALCOLA I LIVELLI E SOMMA I DB
                        for key in list(level_emi_bands.keys()):
                            if level_emi[key] > 0:
                                level_dif_bands[key] = on_Acoustics.Diffraction3D(level_emi_bands[key],
                                                                                distSUP3D, epsilon,dInclinata,
                                                                                temperature).level3D()
                                level_atm_bands[key] = on_Acoustics.AtmosphericAbsorption(distSUP3D, temperature,
                                                                                          humidity, level_emi_bands[
                                                                                              key]).attenuation()
                                level_dif_bands[key] = on_Acoustics.DiffBands(level_dif_bands[key], level_atm_bands[key])


                                if settings['implementation_roads'] == 'CNOSSOS':
                                    level_dif[key] = on_Acoustics.OctaveBandsToGlobalA(level_dif_bands[key])
                                else:
                                    level_dif[key] = on_Acoustics.OctaveBandsToGlobal(level_dif_bands[key])

                                # correction for the segment lenght
                                if feat_type == 'road':
                                    if (settings['implementation_roads'] == 'POWER_R' or settings['implementation_roads'] == 'NMPB'):
                                        level_dif[key] = level_dif[key] + 20 + 10 * log10(float(segment)) + 3
                                    if settings['implementation_roads'] == 'CNOSSOS':
                                        level_dif[key] = level_dif[key] + 10 * log10(float(segment)) + 3
                                #         add noise to final value
                                receiver_point_lin_level[key] = receiver_point_lin_level[key] + 10**(level_dif[key] / float(10))
                            else:
                                level_dif[key] = -1

                        if diff3D_rays_writer is not None:
                            ray = QgsFeature()
                            ray.setGeometry(line)
                            attributes = [diff3D_ray_id,
                                          receiver_feat.id(),
                                          sor_feat.id(),
                                          distSUP3D,
                                          epsilon]

                            if settings['period_pts_gen'] == "True" or settings['period_roads_gen'] == "True":
                                if 'Lgeneric' in level_emi:
                                    attributes.append(level_emi['Lgeneric'])
                                    attributes.append(level_dif['Lgeneric'])
                                else:
                                    attributes.append(None)
                                    attributes.append(None)
                            if settings['period_pts_day'] == "True" or settings['period_roads_day'] == "True":
                                if 'Lday' in level_emi:
                                    attributes.append(level_emi['Lday'])
                                    attributes.append(level_dif['Lday'])
                                else:
                                    attributes.append(None)
                                    attributes.append(None)
                            if settings['period_pts_eve'] == "True" or settings['period_roads_eve'] == "True":
                                if 'Levening' in level_emi:
                                    attributes.append(level_emi['Levening'])
                                    attributes.append(level_dif['Levening'])
                                else:
                                    attributes.append(None)
                                    attributes.append(None)
                            if settings['period_pts_nig'] == "True" or settings['period_roads_nig'] == "True":
                                if 'Lnight' in level_emi:
                                    attributes.append(level_emi['Lnight'])
                                    attributes.append(level_dif['Lnight'])
                                else:
                                    attributes.append(None)
                                    attributes.append(None)

                            ray.setAttributes(attributes)
                            diff3D_rays_writer.addFeature(ray)

                            #update counter ID rays
                            diff3D_ray_id = diff3D_ray_id +1

            if settings['period_pts_gen'] == "True" or settings['period_roads_gen'] == "True":
                    if receiver_point_lin_level['Lgeneric'] > 0:
                        Lgen = 10*log10(receiver_point_lin_level['Lgeneric'])
                        if Lgen < 0:
                            Lgen = 0
                        receiver_feat_new_fields[level_field_index['Lgeneric']] =  Lgen
                    else:
                        receiver_feat_new_fields[level_field_index['Lgeneric']] = -99

            Lday = 0
            Leve = 0
            Lnig = 0

            #added control on final data if negative set to zero
            if settings['period_pts_day'] == "True" or settings['period_roads_day'] == "True":
                    if receiver_point_lin_level['Lday'] > 0:
                        Lday = 10*log10(receiver_point_lin_level['Lday'])
                        if Lday < 0:
                            Lday = 0
                        receiver_feat_new_fields[level_field_index['Lday']] = Lday
                    else:
                        receiver_feat_new_fields[level_field_index['Lday']] = -99

            if settings['period_pts_eve'] == "True" or settings['period_roads_eve'] == "True":
                    if receiver_point_lin_level['Levening'] > 0:
                        Leve = 10*log10(receiver_point_lin_level['Levening'])
                        if Leve <0:
                            Leve=0
                        receiver_feat_new_fields[level_field_index['Levening']] = Leve
                    else:
                        receiver_feat_new_fields[level_field_index['Levening']] = -99

            if settings['period_pts_nig'] == "True" or settings['period_roads_nig'] == "True":
                    if receiver_point_lin_level['Lnight'] > 0:
                        Lnig = 10*log10(receiver_point_lin_level['Lnight'])
                        if Lnig <0:
                            Lnig=0
                        receiver_feat_new_fields[level_field_index['Lnight']] = Lnig

                    else:
                        receiver_feat_new_fields[level_field_index['Lnight']] = -99

            if settings['period_den'] == "True":
                    receiver_feat_new_fields[level_field_index['Lden']] = on_Acoustics.Lden(Lday,Leve,Lnig,
                                                                                           int(settings['day_hours']),
                                                                                           int(settings['eve_hours']),
                                                                                           int(settings['nig_hours']),
                                                                                           int(settings['day_penalty']),
                                                                                           int(settings['eve_penalty']),
                                                                                           int(settings['nig_penalty'])
                                                                                           )
            receiver_feat_all_new_fields[receiver_feat.id()] = receiver_feat_new_fields

    progress_bars['calculate']['label'].setText('Done in ' + duration(time,datetime.now()) )

    # fix_print_with_import
    print('calculate levels and, if selected, draw rays',datetime.now() - time)
    time = datetime.now()

    return receiver_feat_all_new_fields


def run(settings,progress_bars,totalBar):

    for key in list(progress_bars.keys()):
        bar = progress_bars[key]
        bar['bar'].setValue(0)
        bar['label'].setText('')

    CreateTempDir()

    receiver_layer_name = os.path.splitext(os.path.basename(settings['receivers_path']))[0]
    receiver_layer = QgsVectorLayer(settings['receivers_path'],receiver_layer_name,"ogr")

    if settings['sources_pts_path'] is not None:
        source_pts_layer_name = os.path.splitext(os.path.basename(settings['sources_pts_path']))[0]
        source_pts_layer = QgsVectorLayer(settings['sources_pts_path'],source_pts_layer_name,"ogr")
    else:
        source_pts_layer = None

    if settings['sources_roads_path'] is not None:
        source_roads_layer_name = os.path.splitext(os.path.basename(settings['sources_roads_path']))[0]
        source_roads_layer = QgsVectorLayer(settings['sources_roads_path'],source_roads_layer_name,"ogr")

    else:
        source_roads_layer = None

    if settings['buildings_path'] is not None:
        obstacles_layer_name = os.path.splitext(os.path.basename(settings['buildings_path']))[0]
        obstacles_layer = QgsVectorLayer(settings['buildings_path'],obstacles_layer_name,"ogr")
    else:
        obstacles_layer = None

    rays_layer_path = settings['rays_path']
    diff_rays_layer_path = settings['diff_rays_path']
    diff3D_layer_path = settings['diff3D_rays_path']

    # defines rays layer
    if rays_layer_path is not None:

        rays_fields = QgsFields()
        rays_fields.append(QgsField("id_ray", QVariant.Int))
        rays_fields.append(QgsField("id_rec", QVariant.Int))
        rays_fields.append(QgsField("id_emi", QVariant.Int))
        rays_fields.append(QgsField("d_rTOe", QVariant.Double,len=10,prec=2))
        rays_fields.append(QgsField("d_rTOe_4m", QVariant.Double,len=10,prec=2))

        if settings['period_pts_gen'] == "True" or settings['period_roads_gen'] == "True":
            rays_fields.append(QgsField("gen_emi", QVariant.Double,len=5,prec=1))
            rays_fields.append(QgsField("Lgeneric", QVariant.Double,len=5,prec=1))
        if settings['period_pts_day'] == "True" or settings['period_roads_day'] == "True":
            rays_fields.append(QgsField("day_emi", QVariant.Double,len=5,prec=1))
            rays_fields.append(QgsField("Lday", QVariant.Double,len=5,prec=1))
        if settings['period_pts_eve'] == "True" or settings['period_roads_eve'] == "True":
            rays_fields.append(QgsField("eve_emi", QVariant.Double,len=5,prec=1))
            rays_fields.append(QgsField("Levening", QVariant.Double,len=5,prec=1))
        if settings['period_pts_nig'] == "True" or settings['period_roads_nig'] == "True":
            rays_fields.append(QgsField("nig_emi", QVariant.Double,len=5,prec=1))
            rays_fields.append(QgsField("Lnight", QVariant.Double,len=5,prec=1))

        rays_writer = QgsVectorFileWriter(rays_layer_path,"System",rays_fields,QgsWkbTypes.LineString,
                                          receiver_layer.crs(), "ESRI Shapefile")



    else:
        rays_writer = None

    # defines diff rays layer
    if diff_rays_layer_path is not None:

        rays_fields = QgsFields()
        rays_fields.append(QgsField("id_ray", QVariant.Int))
        rays_fields.append(QgsField("id_rec", QVariant.Int))
        rays_fields.append(QgsField("id_dif", QVariant.Int))
        rays_fields.append(QgsField("id_emi", QVariant.Int))
        rays_fields.append(QgsField("d_rTOd", QVariant.Double, len=10, prec=2))
        rays_fields.append(QgsField("d_dTOe", QVariant.Double, len=10, prec=2))
        rays_fields.append(QgsField("d_rTOe", QVariant.Double, len=10, prec=2))

        if settings['period_pts_gen'] == "True" or settings['period_roads_gen'] == "True":
            rays_fields.append(QgsField("gen_emi", QVariant.Double,len=5,prec=1))
            rays_fields.append(QgsField("Lgeneric", QVariant.Double,len=5,prec=1))
        if settings['period_pts_day'] == "True" or settings['period_roads_day'] == "True":
            rays_fields.append(QgsField("day_emi", QVariant.Double,len=5,prec=1))
            rays_fields.append(QgsField("Lday", QVariant.Double,len=5,prec=1))
        if settings['period_pts_eve'] == "True" or settings['period_roads_eve'] == "True":
            rays_fields.append(QgsField("eve_emi", QVariant.Double,len=5,prec=1))
            rays_fields.append(QgsField("Levening", QVariant.Double,len=5,prec=1))
        if settings['period_pts_nig'] == "True" or settings['period_roads_nig'] == "True":
            rays_fields.append(QgsField("nig_emi", QVariant.Double,len=5,prec=1))
            rays_fields.append(QgsField("Lnight", QVariant.Double,len=5,prec=1))

        diff_rays_writer = QgsVectorFileWriter(diff_rays_layer_path, "System", rays_fields, QgsWkbTypes.LineString,
                                               receiver_layer.crs(), "ESRI Shapefile")


    else:
        diff_rays_writer = None

    if diff3D_layer_path is not None:

        # add fields
        rays_fields = QgsFields()
        rays_fields.append(QgsField("id_dif_ray", QVariant.Int))
        rays_fields.append(QgsField("id_rec", QVariant.Int))
        rays_fields.append(QgsField("id_emi", QVariant.Int))
        rays_fields.append(QgsField("delta3d", QVariant.Double, len=10, prec=2))
        rays_fields.append(QgsField("epsilon", QVariant.Double, len=10, prec=2))

        if settings['period_pts_gen'] == "True" or settings['period_roads_gen'] == "True":
            rays_fields.append(QgsField("gen_emi", QVariant.Double,len=5,prec=1))
            rays_fields.append(QgsField("Lgeneric", QVariant.Double,len=5,prec=1))
        if settings['period_pts_day'] == "True" or settings['period_roads_day'] == "True":
            rays_fields.append(QgsField("day_emi", QVariant.Double,len=5,prec=1))
            rays_fields.append(QgsField("Lday", QVariant.Double,len=5,prec=1))
        if settings['period_pts_eve'] == "True" or settings['period_roads_eve'] == "True":
            rays_fields.append(QgsField("eve_emi", QVariant.Double,len=5,prec=1))
            rays_fields.append(QgsField("Levening", QVariant.Double,len=5,prec=1))
        if settings['period_pts_nig'] == "True" or settings['period_roads_nig'] == "True":
            rays_fields.append(QgsField("nig_emi", QVariant.Double,len=5,prec=1))
            rays_fields.append(QgsField("Lnight", QVariant.Double,len=5,prec=1))

        diff3D_rays_writer = QgsVectorFileWriter(diff3D_layer_path, "System", rays_fields, QgsWkbTypes.LineString,
                                               receiver_layer.crs(), "ESRI Shapefile")


    else:
        diff3D_rays_writer = None



    # puts the sound level in the receivers points attribute table
    # gets fields from recever point layer and initializes the final receiver_point_field_level to populate the receiver points layer attribute table
    fields_number = int(receiver_layer.fields().count())

    level_field_index = {}

    #modified version in creating fields on existing layer in qgis 3.x
    receiver_layer.startEditing()
    #level_fields = []
    if settings['period_pts_gen'] == "True" or settings['period_roads_gen'] == "True":
        receiver_layer.addAttribute(QgsField('Lgeneric', QVariant.Double, len=5, prec=1))
        level_field_index['Lgeneric'] = fields_number
        fields_number = fields_number + 1
    if settings['period_pts_day'] == "True" or settings['period_roads_day'] == "True":
        receiver_layer.addAttribute((QgsField('Lday', QVariant.Double, len=5, prec=1)))
        level_field_index['Lday'] = fields_number
        fields_number = fields_number + 1
    if settings['period_pts_eve'] == "True" or settings['period_roads_eve'] == "True":
        receiver_layer.addAttribute(QgsField('Levening', QVariant.Double,len=5,prec=1))
        level_field_index['Levening'] = fields_number
        fields_number = fields_number + 1
    if settings['period_pts_nig'] == "True" or settings['period_roads_nig'] == "True":
        receiver_layer.addAttribute(QgsField('Lnight', QVariant.Double,len=5,prec=1))
        level_field_index['Lnight'] = fields_number
        fields_number = fields_number + 1
    if settings['period_den'] == "True":
        receiver_layer.addAttribute(QgsField('Lden', QVariant.Double,len=5,prec=1))
        level_field_index['Lden'] = fields_number
        fields_number = fields_number + 1


    #receiver_layer.dataProvider().addAttributes( level_fields )
    receiver_layer.updateFields()


    #calculation
    receiver_feat_new_fields = calc(progress_bars,totalBar,receiver_layer,source_pts_layer,source_roads_layer,settings,level_field_index,obstacles_layer,rays_writer,diff_rays_writer,diff3D_rays_writer)

    #old way to insert data in table
    # receiver_layer.dataProvider().changeAttributeValues(receiver_feat_new_fields)

    #new way to insert data in table
    for f in receiver_layer.getFeatures():
        # Bug correction in case of receiver inside a building
        # we exclude the receiver from calculus
        Skip_intersectionDD = False
        if obstacles_layer is not None:
            obstacles_feat_all = obstacles_layer.dataProvider().getFeatures()
            for obstacles_feat in obstacles_feat_all:
                if f.geometry().intersects(obstacles_feat.geometry()):
                    Skip_intersectionDD = True


        if 'Lgeneric' in level_field_index:
            if Skip_intersectionDD is False:
                f['Lgeneric'] = receiver_feat_new_fields[f.id()][level_field_index['Lgeneric']]
                #print(receiver_feat_new_fields,f.id(),f['Lgeneric'])
            else:
                f['Lgeneric'] = -99
        if 'Lday' in level_field_index:
            if Skip_intersectionDD is False:
                f['Lday'] = receiver_feat_new_fields[f.id()][level_field_index['Lday']]
            else:
                f['Lday'] = -99
        if 'Levening' in level_field_index:
            if Skip_intersectionDD is False:
                f['Levening'] = receiver_feat_new_fields[f.id()][level_field_index['Levening']]
            else:
                f['Levening'] = -99
        if 'Lnight' in level_field_index:
            if Skip_intersectionDD is False:
                f['Lnight'] = receiver_feat_new_fields[f.id()][level_field_index['Lnight']]
            else:
                f['Lnight'] = -99
        if 'Lden' in level_field_index:
            if Skip_intersectionDD is False:
                f['Lden'] = receiver_feat_new_fields[f.id()][level_field_index['Lden']]
            else:
                f['Lden'] = -99
        receiver_layer.updateFeature(f)

    receiver_layer.updateExtents()

    receiver_layer.commitChanges()

    #reload all layers to see the updates of shapefile of receivers
    QgsProject.instance().reloadAllLayers()

    if rays_layer_path is not None:
        del rays_writer
        rays_layer_name = os.path.splitext(os.path.basename(rays_layer_path))[0]
        rays_layer = QgsVectorLayer(rays_layer_path, str(rays_layer_name), "ogr")

        QgsProject.instance().addMapLayers([rays_layer])

    if diff_rays_layer_path is not None:
        del diff_rays_writer
        diff_rays_layer_name = os.path.splitext(os.path.basename(diff_rays_layer_path))[0]
        diff_rays_layer = QgsVectorLayer(diff_rays_layer_path, str(diff_rays_layer_name), "ogr")

        QgsProject.instance().addMapLayers([diff_rays_layer])

        QgsProject.instance().reloadAllLayers()

    if diff3D_layer_path is not None:
        del diff3D_rays_writer
        diff3D_rays_layer_name = os.path.splitext(os.path.basename(diff3D_layer_path))[0]
        diff3D_rays_layer = QgsVectorLayer(diff3D_layer_path, str(diff3D_rays_layer_name), "ogr")

        QgsProject.instance().addMapLayers([diff3D_rays_layer])
        QgsProject.instance().reloadAllLayers()

    # render receivers with noise colours
    level_fields_new = list(receiver_layer.dataProvider().fields())

    if len(level_fields_new) > 0:
        receiver_layer_name = settings['receivers_name']
        layer = QgsProject.instance().mapLayersByName(receiver_layer_name)[0]
        on_ApplyNoiseSymbology.renderizeXY(layer, level_fields_new[len(level_fields_new) - 1].name())


    DeleteTempDir()
