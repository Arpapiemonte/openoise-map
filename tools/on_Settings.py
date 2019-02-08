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


import xml.etree.ElementTree as ET

import os
from shutil import copyfile



def keys_traduction():
    keys_traduction =  {'directory_last' : 'directory/last',
                        'receivers_name' : 'layers/receivers/name',
                        'receivers_path' : 'layers/receivers/path',
                        'sources_pts_name' : 'layers/sources/pts/name',
                        'sources_pts_path' : 'layers/sources/pts/path',
                        'sources_roads_name' : 'layers/sources/roads/name',
                        'sources_roads_path' : 'layers/sources/roads/path',
                        'buildings_name' : 'layers/buildings/name',
                        'buildings_path' : 'layers/buildings/path',
                        'rays_path' : 'layers/rays/path',
                        'diff_rays_path' : 'layers/diff_rays/path',
                        'research_ray' : 'options/research_ray',
                        'temperature' : 'options/temperature',
                        'humidity' : 'options/humidity',
                        'implementation_pts': 'emission/implementation/pts',
                        'implementation_roads': 'emission/implementation/roads',
                        'period_pts_gen' : 'emission/period/pts/gen',
                        'period_pts_day' : 'emission/period/pts/day',
                        'period_pts_eve' : 'emission/period/pts/eve',
                        'period_pts_nig' : 'emission/period/pts/nig',                    
                        'period_roads_gen' : 'emission/period/roads/gen',
                        'period_roads_day' : 'emission/period/roads/day',
                        'period_roads_eve' : 'emission/period/roads/eve',
                        'period_roads_nig' : 'emission/period/roads/nig',                    
                        'period_den' : 'emission/period/den',
                        'day_hours' : 'options/den/day_hours',
                        'eve_hours' : 'options/den/eve_hours',                    
                        'nig_hours' : 'options/den/nig_hours',                                      
                        'day_penalty' : 'options/den/day_penalty',
                        'eve_penalty' : 'options/den/eve_penalty',                    
                        'nig_penalty' : 'options/den/nig_penalty',                                      
                        'POWER_P_gen' :'emission/POWER_P/gen',
                        'POWER_P_day' : 'emission/POWER_P/day',
                        'POWER_P_eve' : 'emission/POWER_P/eve',
                        'POWER_P_nig' : 'emission/POWER_P/nig',
                        'POWER_R_gen' : 'emission/POWER_R/gen',
                        'POWER_R_day' : 'emission/POWER_R/day',
                        'POWER_R_eve' : 'emission/POWER_R/eve',
                        'POWER_R_nig' : 'emission/POWER_R/nig',
                        'NMPB_gen_l_n' : 'emission/NMPB/gen_l_n',
                        'NMPB_gen_l_s' : 'emission/NMPB/gen_l_s',
                        'NMPB_gen_h_n' : 'emission/NMPB/gen_h_n',
                        'NMPB_gen_h_s' : 'emission/NMPB/gen_h_s',
                        'NMPB_gen_type' : 'emission/NMPB/gen_type',
                        'NMPB_day_l_n' : 'emission/NMPB/day_l_n',
                        'NMPB_day_l_s' : 'emission/NMPB/day_l_s',
                        'NMPB_day_h_n' : 'emission/NMPB/day_h_n',
                        'NMPB_day_h_s' : 'emission/NMPB/day_h_s',
                        'NMPB_day_type' : 'emission/NMPB/day_type',
                        'NMPB_eve_l_n' : 'emission/NMPB/eve_l_n',
                        'NMPB_eve_l_s' : 'emission/NMPB/eve_l_s',
                        'NMPB_eve_h_n' : 'emission/NMPB/eve_h_n',
                        'NMPB_eve_h_s' : 'emission/NMPB/eve_h_s',
                        'NMPB_eve_type' : 'emission/NMPB/eve_type',
                        'NMPB_nig_l_n' : 'emission/NMPB/nig_l_n',
                        'NMPB_nig_l_s' : 'emission/NMPB/nig_l_s',
                        'NMPB_nig_h_n' : 'emission/NMPB/nig_h_n',
                        'NMPB_nig_h_s' : 'emission/NMPB/nig_h_s',
                        'NMPB_nig_type' : 'emission/NMPB/nig_type',
                        'NMPB_surface' : 'emission/NMPB/surface',
                        'NMPB_slope' : 'emission/NMPB/slope',
                        'CNOSSOS_gen_1_n' : 'emission/CNOSSOS/gen_1_n',
                        'CNOSSOS_gen_1_s' : 'emission/CNOSSOS/gen_1_s',
                        'CNOSSOS_gen_2_n' : 'emission/CNOSSOS/gen_2_n',
                        'CNOSSOS_gen_2_s' : 'emission/CNOSSOS/gen_2_s',
                        'CNOSSOS_gen_3_n' : 'emission/CNOSSOS/gen_3_n',
                        'CNOSSOS_gen_3_s' : 'emission/CNOSSOS/gen_3_s',
                        'CNOSSOS_gen_4a_n' : 'emission/CNOSSOS/gen_4a_n',
                        'CNOSSOS_gen_4a_s' : 'emission/CNOSSOS/gen_4a_s',
                        'CNOSSOS_gen_4b_n' : 'emission/CNOSSOS/gen_4b_n',
                        'CNOSSOS_gen_4b_s' : 'emission/CNOSSOS/gen_4b_s',
                        'CNOSSOS_day_1_n' : 'emission/CNOSSOS/day_1_n',
                        'CNOSSOS_day_1_s' : 'emission/CNOSSOS/day_1_s',
                        'CNOSSOS_day_2_n' : 'emission/CNOSSOS/day_2_n',
                        'CNOSSOS_day_2_s' : 'emission/CNOSSOS/day_2_s',
                        'CNOSSOS_day_3_n' : 'emission/CNOSSOS/day_3_n',
                        'CNOSSOS_day_3_s' : 'emission/CNOSSOS/day_3_s',
                        'CNOSSOS_day_4a_n' : 'emission/CNOSSOS/day_4a_n',
                        'CNOSSOS_day_4a_s' : 'emission/CNOSSOS/day_4a_s',
                        'CNOSSOS_day_4b_n' : 'emission/CNOSSOS/day_4b_n',
                        'CNOSSOS_day_4b_s' : 'emission/CNOSSOS/day_4b_s',
                        'CNOSSOS_eve_1_n' : 'emission/CNOSSOS/eve_1_n',
                        'CNOSSOS_eve_1_s' : 'emission/CNOSSOS/eve_1_s',
                        'CNOSSOS_eve_2_n' : 'emission/CNOSSOS/eve_2_n',
                        'CNOSSOS_eve_2_s' : 'emission/CNOSSOS/eve_2_s',
                        'CNOSSOS_eve_3_n' : 'emission/CNOSSOS/eve_3_n',
                        'CNOSSOS_eve_3_s' : 'emission/CNOSSOS/eve_3_s',
                        'CNOSSOS_eve_4a_n' : 'emission/CNOSSOS/eve_4a_n',
                        'CNOSSOS_eve_4a_s' : 'emission/CNOSSOS/eve_4a_s',
                        'CNOSSOS_eve_4b_n' : 'emission/CNOSSOS/eve_4b_n',
                        'CNOSSOS_eve_4b_s' : 'emission/CNOSSOS/eve_4b_s',
                        'CNOSSOS_nig_1_n' : 'emission/CNOSSOS/nig_1_n',
                        'CNOSSOS_nig_1_s' : 'emission/CNOSSOS/nig_1_s',
                        'CNOSSOS_nig_2_n' : 'emission/CNOSSOS/nig_2_n',
                        'CNOSSOS_nig_2_s' : 'emission/CNOSSOS/nig_2_s',
                        'CNOSSOS_nig_3_n' : 'emission/CNOSSOS/nig_3_n',
                        'CNOSSOS_nig_3_s' : 'emission/CNOSSOS/nig_3_s',
                        'CNOSSOS_nig_4a_n' : 'emission/CNOSSOS/nig_4a_n',
                        'CNOSSOS_nig_4a_s' : 'emission/CNOSSOS/nig_4a_s',
                        'CNOSSOS_nig_4b_n' : 'emission/CNOSSOS/nig_4b_n',
                        'CNOSSOS_nig_4b_s' : 'emission/CNOSSOS/nig_4b_s',
                        'CNOSSOS_surface' : 'emission/CNOSSOS/surface',
                        'CNOSSOS_slope' : 'emission/CNOSSOS/slope'
                        }
                    
    return keys_traduction


def PtsEmission_keys_traduction():
    keys_traduction =  {'implementation_pts': 'emission/implementation/pts',
                        'period_pts_gen' : 'emission/period/pts/gen',
                        'period_pts_day' : 'emission/period/pts/day',
                        'period_pts_eve' : 'emission/period/pts/eve',
                        'period_pts_nig' : 'emission/period/pts/nig',                    
                        'POWER_P_gen' :'emission/POWER_P/gen',
                        'POWER_P_day' : 'emission/POWER_P/day',
                        'POWER_P_eve' : 'emission/POWER_P/eve',
                        'POWER_P_nig' : 'emission/POWER_P/nig',
                        }
                    
    return keys_traduction
    
    
def RoadsEmission_keys_traduction():
    keys_traduction =  {'implementation_roads': 'emission/implementation/roads',
                        'period_roads_gen' : 'emission/period/roads/gen',
                        'period_roads_day' : 'emission/period/roads/day',
                        'period_roads_eve' : 'emission/period/roads/eve',
                        'period_roads_nig' : 'emission/period/roads/nig',                          
                        'POWER_R_gen' : 'emission/POWER_R/gen',
                        'POWER_R_day' : 'emission/POWER_R/day',
                        'POWER_R_eve' : 'emission/POWER_R/eve',
                        'POWER_R_nig' : 'emission/POWER_R/nig',
                        'NMPB_gen_l_n' : 'emission/NMPB/gen_l_n',
                        'NMPB_gen_l_s' : 'emission/NMPB/gen_l_s',
                        'NMPB_gen_h_n' : 'emission/NMPB/gen_h_n',
                        'NMPB_gen_h_s' : 'emission/NMPB/gen_h_s',
                        'NMPB_gen_type' : 'emission/NMPB/gen_type',
                        'NMPB_day_l_n' : 'emission/NMPB/day_l_n',
                        'NMPB_day_l_s' : 'emission/NMPB/day_l_s',
                        'NMPB_day_h_n' : 'emission/NMPB/day_h_n',
                        'NMPB_day_h_s' : 'emission/NMPB/day_h_s',
                        'NMPB_day_type' : 'emission/NMPB/day_type',
                        'NMPB_eve_l_n' : 'emission/NMPB/eve_l_n',
                        'NMPB_eve_l_s' : 'emission/NMPB/eve_l_s',
                        'NMPB_eve_h_n' : 'emission/NMPB/eve_h_n',
                        'NMPB_eve_h_s' : 'emission/NMPB/eve_h_s',
                        'NMPB_eve_type' : 'emission/NMPB/eve_type',
                        'NMPB_nig_l_n' : 'emission/NMPB/nig_l_n',
                        'NMPB_nig_l_s' : 'emission/NMPB/nig_l_s',
                        'NMPB_nig_h_n' : 'emission/NMPB/nig_h_n',
                        'NMPB_nig_h_s' : 'emission/NMPB/nig_h_s',
                        'NMPB_nig_type' : 'emission/NMPB/nig_type',
                        'NMPB_surface' : 'emission/NMPB/surface',
                        'NMPB_slope' : 'emission/NMPB/slope',
                        'CNOSSOS_gen_1_n' : 'emission/CNOSSOS/gen_1_n',
                        'CNOSSOS_gen_1_s' : 'emission/CNOSSOS/gen_1_s',
                        'CNOSSOS_gen_2_n' : 'emission/CNOSSOS/gen_2_n',
                        'CNOSSOS_gen_2_s' : 'emission/CNOSSOS/gen_2_s',
                        'CNOSSOS_gen_3_n' : 'emission/CNOSSOS/gen_3_n',
                        'CNOSSOS_gen_3_s' : 'emission/CNOSSOS/gen_3_s',
                        'CNOSSOS_gen_4a_n' : 'emission/CNOSSOS/gen_4a_n',
                        'CNOSSOS_gen_4a_s' : 'emission/CNOSSOS/gen_4a_s',
                        'CNOSSOS_gen_4b_n' : 'emission/CNOSSOS/gen_4b_n',
                        'CNOSSOS_gen_4b_s' : 'emission/CNOSSOS/gen_4b_s',
                        'CNOSSOS_day_1_n' : 'emission/CNOSSOS/day_1_n',
                        'CNOSSOS_day_1_s' : 'emission/CNOSSOS/day_1_s',
                        'CNOSSOS_day_2_n' : 'emission/CNOSSOS/day_2_n',
                        'CNOSSOS_day_2_s' : 'emission/CNOSSOS/day_2_s',
                        'CNOSSOS_day_3_n' : 'emission/CNOSSOS/day_3_n',
                        'CNOSSOS_day_3_s' : 'emission/CNOSSOS/day_3_s',
                        'CNOSSOS_day_4a_n' : 'emission/CNOSSOS/day_4a_n',
                        'CNOSSOS_day_4a_s' : 'emission/CNOSSOS/day_4a_s',
                        'CNOSSOS_day_4b_n' : 'emission/CNOSSOS/day_4b_n',
                        'CNOSSOS_day_4b_s' : 'emission/CNOSSOS/day_4b_s',
                        'CNOSSOS_eve_1_n' : 'emission/CNOSSOS/eve_1_n',
                        'CNOSSOS_eve_1_s' : 'emission/CNOSSOS/eve_1_s',
                        'CNOSSOS_eve_2_n' : 'emission/CNOSSOS/eve_2_n',
                        'CNOSSOS_eve_2_s' : 'emission/CNOSSOS/eve_2_s',
                        'CNOSSOS_eve_3_n' : 'emission/CNOSSOS/eve_3_n',
                        'CNOSSOS_eve_3_s' : 'emission/CNOSSOS/eve_3_s',
                        'CNOSSOS_eve_4a_n' : 'emission/CNOSSOS/eve_4a_n',
                        'CNOSSOS_eve_4a_s' : 'emission/CNOSSOS/eve_4a_s',
                        'CNOSSOS_eve_4b_n' : 'emission/CNOSSOS/eve_4b_n',
                        'CNOSSOS_eve_4b_s' : 'emission/CNOSSOS/eve_4b_s',
                        'CNOSSOS_nig_1_n' : 'emission/CNOSSOS/nig_1_n',
                        'CNOSSOS_nig_1_s' : 'emission/CNOSSOS/nig_1_s',
                        'CNOSSOS_nig_2_n' : 'emission/CNOSSOS/nig_2_n',
                        'CNOSSOS_nig_2_s' : 'emission/CNOSSOS/nig_2_s',
                        'CNOSSOS_nig_3_n' : 'emission/CNOSSOS/nig_3_n',
                        'CNOSSOS_nig_3_s' : 'emission/CNOSSOS/nig_3_s',
                        'CNOSSOS_nig_4a_n' : 'emission/CNOSSOS/nig_4a_n',
                        'CNOSSOS_nig_4a_s' : 'emission/CNOSSOS/nig_4a_s',
                        'CNOSSOS_nig_4b_n' : 'emission/CNOSSOS/nig_4b_n',
                        'CNOSSOS_nig_4b_s' : 'emission/CNOSSOS/nig_4b_s',
                        'CNOSSOS_surface' : 'emission/CNOSSOS/surface',
                        'CNOSSOS_slope' : 'emission/CNOSSOS/slope'
                        }
                    
    return keys_traduction


def setSettings(settings):
    '''
    settings has to be a dict
    '''
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    settingsFile_path = os.path.join(dir_path,"on_Settings.xml")
    settingsFile = ET.parse(settingsFile_path)
    
    translated_keys = keys_traduction()
    
    for key in list(settings.keys()):
        settingsFile.find(translated_keys[key]).text = settings[key]
        settingsFile.write(settingsFile_path)    
    
    return

def getAllSettings():
    '''
    the output is a dict
    '''
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path) 
    settingsFile = ET.parse(os.path.join(dir_path,"on_Settings.xml"))
    
    translated_keys = keys_traduction()
    
    settings = {}
    
    for key in list(translated_keys.keys()):
        settings[key] = settingsFile.find(translated_keys[key]).text
    
    return settings


def setOneSetting(key,value):

    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    settingsFile_path = os.path.join(dir_path,"on_Settings.xml")
    settingsFile = ET.parse(settingsFile_path)
    
    translated_keys = keys_traduction()

    settingsFile.find(translated_keys[key]).text = value
    settingsFile.write(settingsFile_path)    
        
    return


def getOneSetting(key):
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path) 
    settingsFile = ET.parse(os.path.join(dir_path,"on_Settings.xml"))
    
    translated_keys = keys_traduction()
    
    return settingsFile.find(translated_keys[key]).text


def clearPtsEmissionSettings():
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    settingsFile_path = os.path.join(dir_path,"on_Settings.xml")
    settingsFile = ET.parse(settingsFile_path)
    
    translated_keys = PtsEmission_keys_traduction()
    
    for key in list(translated_keys.keys()):
        settingsFile.find(translated_keys[key]).text = None
        settingsFile.write(settingsFile_path)    
    
    return        


def clearRoadsEmissionSettings():
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    settingsFile_path = os.path.join(dir_path,"on_Settings.xml")
    settingsFile = ET.parse(settingsFile_path)
    
    translated_keys = RoadsEmission_keys_traduction()
    
    for key in list(translated_keys.keys()):
        settingsFile.find(translated_keys[key]).text = None
        settingsFile.write(settingsFile_path)    
    
    return    

def copyLastSettingsToSettings():

    currentPath = os.path.dirname(__file__)
    settings_path = currentPath + '/on_Settings.xml'
    settings_last_path = currentPath + '/on_SettingsLast.xml'

    copyfile(settings_last_path,settings_path)    

def copySettingsToLastSettings():

    currentPath = os.path.dirname(__file__)
    settings_path = currentPath + '/on_Settings.xml'
    settings_last_path = currentPath + '/on_SettingsLast.xml'

    copyfile(settings_path, settings_last_path)

def copySavedSettingsToSettings(saved_settings_path):

    currentPath = os.path.dirname(__file__)
    settings_path = currentPath + '/on_Settings.xml'

    copyfile(saved_settings_path,settings_path)    

def copySettingsToSavedSettings(saved_settings_path):

    currentPath = os.path.dirname(__file__)
    settings_path = currentPath + '/on_Settings.xml'

    copyfile(settings_path,saved_settings_path)    


#
#def clearAllSettings():
#    path = os.path.abspath(__file__)
#    dir_path = os.path.dirname(path)
#    settingsFile_path = os.path.join(dir_path,"on_Settings.xml")
#    settingsFile = ET.parse(settingsFile_path)
#    
#    translated_keys = keys_traduction()
#    
#    for key in translated_keys.keys():
#        if key <> 'directory_last' or key <> 'reload':
#            settingsFile.find(translated_keys[key]).text = None
#            settingsFile.write(settingsFile_path)    
#    
#    return    
#
#
#def setSettingsTemp(settings):
#    '''
#    settings has to be a dict
#    '''
#    path = os.path.abspath(__file__)
#    dir_path = os.path.dirname(path)
#    settingsFile_path = os.path.join(dir_path,"openoise_settings_temp.xml")
#    settingsFile = ET.parse(settingsFile_path)
#    
#    translated_keys = keys_traduction()
#    
#    for key in settings.keys():
#        settingsFile.find(translated_keys[key]).text = settings[key]
#        settingsFile.write(settingsFile_path)    
#        print 'scrivo', key,settings[key]
#    
#    return
#
#def getAllSettingsTemp():
#    '''
#    the output is a dict
#    '''
#    path = os.path.abspath(__file__)
#    dir_path = os.path.dirname(path) 
#    settingsFile = ET.parse(os.path.join(dir_path,"openoise_settings_temp.xml"))
#    
#    translated_keys = keys_traduction()
#    
#    settings = {}
#    
#    for key in translated_keys.keys():
#        settings[key] = settingsFile.find(translated_keys[key]).text
#    
#    return settings
#
#def copyEmissionSettingsFromTemp():
#    path = os.path.abspath(__file__)
#    dir_path = os.path.dirname(path) 
#    settingsFile = ET.parse(os.path.join(dir_path,"openoise_settings_temp.xml"))
#    
#    Pts_translated_keys = PtsEmission_keys_traduction()
#    Roads_translated_keys = RoadsEmission_keys_traduction()
#    
#    settings = {}
#    
#    for key in Pts_translated_keys.keys():
#        settings[key] = settingsFile.find(Pts_translated_keys[key]).text
#
#    for key in Roads_translated_keys.keys():
#        settings[key] = settingsFile.find(Roads_translated_keys[key]).text   
#        
#    setSettings(settings)
#    
#    
#def copyEmissionSettingsToTemp():
#    path = os.path.abspath(__file__)
#    dir_path = os.path.dirname(path) 
#    settingsFile = ET.parse(os.path.join(dir_path,"on_Settings.xml"))
#    
#    Pts_translated_keys = PtsEmission_keys_traduction()
#    Roads_translated_keys = RoadsEmission_keys_traduction()
#    
#    settings = {}
#    
#    for key in Pts_translated_keys.keys():
#        settings[key] = settingsFile.find(Pts_translated_keys[key]).text
#
#    for key in Roads_translated_keys.keys():
#        settings[key] = settingsFile.find(Roads_translated_keys[key]).text   
#        
#    print settings
#        
#    setSettingsTemp(settings)
#        
#   
 
#    
#def clearPtsEmissionSettingsTemp():
#    path = os.path.abspath(__file__)
#    dir_path = os.path.dirname(path)
#    settingsFile_path = os.path.join(dir_path,"openoise_settings_temp.xml")
#    settingsFile = ET.parse(settingsFile_path)
#    
#    translated_keys = PtsEmission_keys_traduction()
#    
#    for key in translated_keys.keys():
#        settingsFile.find(translated_keys[key]).text = None
#        settingsFile.write(settingsFile_path)    
#    
#    return        
#
#
#def clearRoadsEmissionSettingsTemp():
#    path = os.path.abspath(__file__)
#    dir_path = os.path.dirname(path)
#    settingsFile_path = os.path.join(dir_path,"openoise_settings_temp.xml")
#    settingsFile = ET.parse(settingsFile_path)
#    
#    translated_keys = RoadsEmission_keys_traduction()
#    
#    for key in translated_keys.keys():
#        settingsFile.find(translated_keys[key]).text = None
#        settingsFile.write(settingsFile_path)    
#    
#    return 
