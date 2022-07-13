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

from builtins import object
from math import sqrt,log10,pi,tanh,atan,exp

from . import on_Acoustics_CNOSSOS
from . import on_Acoustics_NMPB

def GlobalToOctaveBands(model,level_input):
    '''
    the output is a dict:
    - pink noise: with keys [63, 125, 250, 500, 1000 , 2000, 4000, 8000] and value the levels in bands
    - ISO traffic road: with {125 : -10.2, 250 : -10.2, 500 : -7.2, 1000 : -3.9, 2000 : -6.4, 4000 : -11.4}
    '''
    level_output = {}

    bands = [63, 125, 250, 500, 1000, 2000, 4000, 8000]

    if level_input > 0:

        # ISO 1793-3
        if model == 'ISO_traffic_road':
            levels_to_subctract_bands = {125 : -10.2, 250 : -10.2, 500 : -7.2, 1000 : -3.9, 2000 : -6.4, 4000 : -11.4}

            for band in list(levels_to_subctract_bands.keys()):
                level_output[band] = round(level_input + levels_to_subctract_bands[band],1)

        # pink noise
        if model == 'pink':
            level_band_linear = float(10**(level_input/10.)) / float(len(bands))
            level_band = 10 * log10(level_band_linear)

            for band in bands:
                level_output[band] = round(level_band,1)

    else:
        for band in bands:
            level_output[band] = round(0,1)

    return level_output


def OctaveBandsToGlobal(level_input):
    '''
    level_input: has to be a dict with keys [63, 125, 250, 500, 1000 , 2000, 4000, 8000] and value the levels in bands
    '''

    level_output = 0

    for band in level_input:
        level_output = level_output + 10**(level_input[band]/10.)


    if level_output > 0:
        level_output = round(10*log10(level_output),1)

    return level_output


def OctaveBandsToGlobalA(level_input):
    '''
    level_input: has to be a dict with keys [63, 125, 250, 500, 1000 , 2000, 4000, 8000] and value the levels in bands
    '''
    #print("OctaveBandsToGlobalA")
    level_output = 0
    weightA = {63: -26.2, 125 : -16.1, 250 : -8.6, 500 : -3.2, 1000 : 0, 2000 : 1.2, 4000 : 1, 8000: -1.1}

    for band in level_input:
        #print(band,level_input[band],weightA[band])
        level_output = level_output + 10**((level_input[band] + weightA[band])/10.)


    if level_output > 0:
        level_output = round(10*log10(level_output),1)

    return level_output


def DiffBands(dict1,dict2):
    output = {}
    for key in dict1:
        output[key] = round(dict1[key] - dict2[key],1)

    return output

def Lden(Lday,Leve,Lnig,day_hours,eve_hours,nig_hours,day_penalty,eve_penalty,nig_penalty):

    if Lday > 0:
        day_part = 10**(float(Lday + day_penalty)/ float(10))
    else:
        day_part = 0
    if Leve > 0:
        eve_part = 10**(float(Leve + eve_penalty)/ float(10))
    else:
        eve_part = 0
    if Lnig > 0:
        nig_part = 10**(float(Lnig + nig_penalty)/ float(10))
    else:
        nig_part = 0

    if day_part > 0 and eve_part > 0 and eve_part > 0:
        Lden = round(10*log10(1/24.0*(float(day_hours)*day_part + float(eve_hours)*eve_part + float(nig_hours)*nig_part)),1)
    else:
        Lden = -99

    return round(Lden,1)

def Lden_ITA(Lday,Leve,Lnig):

    if Lday > 0:
        day_part = 10**(float(Lday + 0)/ float(10))
    else:
        day_part = 0
    if Leve > 0:
        eve_part = 10**(float(Leve + 5)/ float(10))
    else:
        eve_part = 0
    if Lnig > 0:
        nig_part = 10**(float(Lnig + 10)/ float(10))
    else:
        nig_part = 0

    if day_part > 0 or eve_part > 0 or eve_part > 0:
        round(10*log10(1/24.0*(float(14)*day_part + float(2)*eve_part + float(8)*nig_part)),1)
    else:
        Lden = 0

    return round(Lden,1)


def GeometricalAttenuation(source_type,distance):

    if source_type == 'spherical':
        attenuation = 20 * log10(distance) + 11

    elif source_type == 'cylindrical':
        attenuation = 10 * log10(distance) + 8

    if attenuation < 0:
        attenuation = 0

    return round(attenuation,1)

class AtmosphericAbsorption(object):

    def __init__(self,distance,temp,rel_humidity,level_input):
        self.level_input = level_input
        self.distance = distance
        self.temp = temp
        self.rel_humidity = rel_humidity

    def level(self):
        level_atm = {}
        attenuation = self.attenuation()

        for band in self.level_input:
            level_atm[band] = round(self.level_input[band] - attenuation[band],1)
        return level_atm

    def attenuation(self):

        if self.temp == -20:
            if self.rel_humidity == 10:
                alfa = {63: 0.8, 125: 1.2, 250: 1.4, 500: 1.5, 1000: 1.6, 2000: 2.1, 4000: 3.9, 8000: 10.9}
            if self.rel_humidity == 20:
                alfa = {63: 0.6, 125: 1.5, 250: 2.4, 500: 2.9, 1000: 3.1, 2000: 3.6, 4000: 5.4, 8000: 12.4}
            if self.rel_humidity == 30:
                alfa = {63: 0.4, 125: 1.3, 250: 2.9, 500: 4.4, 1000: 5.1, 2000: 5.7, 4000: 7.4, 8000: 14.6}
            if self.rel_humidity == 40:
                alfa = {63: 0.3, 125: 1, 250: 2.8, 500: 5.4, 1000: 7.2, 2000: 8.2, 4000: 10.2, 8000: 17.2}
            if self.rel_humidity == 50:
                alfa = {63: 0.2, 125: 0.8, 250: 2.5, 500: 5.9, 1000: 9.1, 2000: 11, 4000: 13.2, 8000: 20.3}
            if self.rel_humidity == 60:
                alfa = {63: 0.2, 125: 0.6, 250: 2, 500: 5.7, 1000: 10.6, 2000: 13.9, 4000: 16.6, 8000: 23.9}
            if self.rel_humidity == 70:
                alfa = {63: 0.2, 125: 0.5, 250: 1.7, 500: 5.2, 1000: 11.5, 2000: 16.6, 4000: 20.2, 8000: 27.8}
            if self.rel_humidity == 80:
                alfa = {63: 0.2, 125: 0.4, 250: 1.5, 500: 4.8, 1000: 11.7, 2000: 19, 4000: 24, 8000: 32}
            if self.rel_humidity == 90:
                alfa = {63: 0.1, 125: 0.4, 250: 1.2, 500: 4.2, 1000: 11.6, 2000: 21, 4000: 27.8, 8000: 36.5}
            if self.rel_humidity == 100:
                alfa = {63: 0.1, 125: 0.3, 250: 1, 500: 3.8, 1000: 11.1, 2000: 22.4, 4000: 31.4, 8000: 41.1}

        if self.temp == -15:
            if self.rel_humidity == 10:
                alfa = {63: 0.8, 125: 1.6, 250: 2.2, 500: 2.5, 1000: 2.6, 2000: 3.1, 4000: 4.9, 8000: 12}
            if self.rel_humidity == 20:
                alfa = {63: 0.5, 125: 1.4, 250: 3.3, 500: 5, 1000: 5.9, 2000: 6.5, 4000: 8.3, 8000: 15.5}
            if self.rel_humidity == 30:
                alfa = {63: 0.3, 125: 1, 250: 3, 500: 6.5, 1000: 9.4, 2000: 11, 4000: 13.1, 8000: 20.3}
            if self.rel_humidity == 40:
                alfa = {63: 0.2, 125: 0.7, 250: 2.3, 500: 6.4, 1000: 12.1, 2000: 15.9, 4000: 18.9, 8000: 26.3}
            if self.rel_humidity == 50:
                alfa = {63: 0.2, 125: 0.5, 250: 1.8, 500: 5.6, 1000: 13.2, 2000: 20.5, 4000: 25.2, 8000: 33.2}
            if self.rel_humidity == 60:
                alfa = {63: 0.2, 125: 0.4, 250: 1.4, 500: 4.7, 1000: 13, 2000: 23.9, 4000: 31.8, 8000: 40.9}
            if self.rel_humidity == 70:
                alfa = {63: 0.1, 125: 0.4, 250: 1.1, 500: 3.9, 1000: 12.1, 2000: 26, 4000: 37.9, 8000: 49}
            if self.rel_humidity == 80:
                alfa = {63: 0.1, 125: 0.3, 250: 1, 500: 3.3, 1000: 10.9, 2000: 26.7, 4000: 43.4, 8000: 57.4}
            if self.rel_humidity == 90:
                alfa = {63: 0.1, 125: 0.3, 250: 0.8, 500: 2.8, 1000: 9.7, 2000: 26.4, 4000: 47.8, 8000: 65.8}
            if self.rel_humidity == 100:
                alfa = {63: 0.1, 125: 0.3, 250: 0.8, 500: 2.5, 1000: 8.6, 2000: 25.4, 4000: 51.1, 8000: 73.9}

        if self.temp == -10:
            if self.rel_humidity == 10:
                alfa = {63: 0.7, 125: 1.86, 250: 3.36, 500: 4.24, 1000: 4.65, 2000: 5.18, 4000: 7, 8000: 14.2}
            if self.rel_humidity == 20:
                alfa = {63: 0.35, 125: 1.11, 250: 3.35, 500: 7.32, 1000: 10.6, 2000: 12.3, 4000: 14.5, 8000: 21.7}
            if self.rel_humidity == 30:
                alfa = {63: 0.23, 125: 0.68, 250: 2.27, 500: 6.82, 1000: 14.4, 2000: 20.5, 4000: 24.4, 8000: 32.2}
            if self.rel_humidity == 40:
                alfa = {63: 0.19, 125: 0.5, 250: 1.58, 500: 5.3, 1000: 14.6, 2000: 26.8, 4000: 35.4, 8000: 44.8}
            if self.rel_humidity == 50:
                alfa = {63: 0.17, 125: 0.4, 250: 1.2, 500: 4, 1000: 12.9, 2000: 29.7, 4000: 45.5, 8000: 58.6}
            if self.rel_humidity == 60:
                alfa = {63: 0.16, 125: 0.36, 250: 0.96, 500: 4, 1000: 10.9, 2000: 29.6, 4000: 53.5, 8000: 72.7}
            if self.rel_humidity == 70:
                alfa = {63: 0.15, 125: 0.33, 250: 0.82, 500: 2.65, 1000: 9.19, 2000: 27.8, 4000: 58.5, 8000: 86.2}
            if self.rel_humidity == 80:
                alfa = {63: 0.14, 125: 0.31, 250: 0.73, 500: 2.24, 1000: 7.82, 2000: 25.4, 4000: 60.7, 8000: 98.2}
            if self.rel_humidity == 90:
                alfa = {63: 0.13, 125: 0.3, 250: 0.67, 500: 1.95, 1000: 6.75, 2000: 22.9, 4000: 60.6, 8000: 108}
            if self.rel_humidity == 100:
                alfa = {63: 0.13, 125: 0.29, 250: 0.62, 500: 1.73, 1000: 5.91, 2000: 20.6, 4000: 59, 8000: 116}

        if self.temp == -5:
            if self.rel_humidity == 10:
                alfa = {63: 0.54, 125: 1.69, 250: 4.2, 500: 6.87, 1000: 8.29, 2000: 9.16, 4000: 11.1, 8000: 18.3}
            if self.rel_humidity == 20:
                alfa = {63: 0.27, 125: 0.79, 250: 2.6, 500: 7.72, 1000: 16, 2000: 22.4, 4000: 26.4, 8000: 34.4}
            if self.rel_humidity == 30:
                alfa = {63: 0.21, 125: 0.52, 250: 1.58, 500: 5.31, 1000: 15.7, 2000: 31.8, 4000: 44.2, 8000: 55.4}
            if self.rel_humidity == 40:
                alfa = {63: 0.19, 125: 0.42, 250: 1.12, 500: 3.71, 1000: 12.4, 2000: 33.2, 4000: 58.7, 8000: 78.6}
            if self.rel_humidity == 50:
                alfa = {63: 0.17, 125: 0.38, 250: 0.9, 500: 2.8, 1000: 9.68, 2000: 30.1, 4000: 66.4, 8000: 100}
            if self.rel_humidity == 60:
                alfa = {63: 0.16, 125: 0.36, 250: 0.78, 500: 2.25, 1000: 7.74, 2000: 26, 4000: 67.7, 8000: 118}
            if self.rel_humidity == 70:
                alfa = {63: 0.15, 125: 0.35, 250: 0.72, 500: 1.9, 1000: 6.38, 2000: 22.2, 4000: 65, 8000: 131}
            if self.rel_humidity == 80:
                alfa = {63: 0.14, 125: 0.34, 250: 0.68, 500: 1.68, 1000: 5.42, 2000: 19.1, 4000: 60.5, 8000: 138}
            if self.rel_humidity == 90:
                alfa = {63: 0.13, 125: 0.33, 250: 0.66, 500: 1.52, 1000: 4.72, 2000: 16.7, 4000: 55.5, 8000: 140}
            if self.rel_humidity == 100:
                alfa = {63: 0.12, 125: 0.33, 250: 0.65, 500: 1.42, 1000: 4.2, 2000: 14.8, 4000: 50.7, 8000: 139}

        if self.temp == 0:
            if self.rel_humidity == 10:
                alfa = {63: 0.42, 125: 1.3, 250: 40, 500: 9.25, 1000: 14, 2000: 16.6, 4000: 19, 8000: 26.4}
            if self.rel_humidity == 20:
                alfa = {63: 0.25, 125: 0.61, 250: 1.85, 500: 6.16, 1000: 17.7, 2000: 34.6, 4000: 47, 8000: 58.1}
            if self.rel_humidity == 30:
                alfa = {63: 0.21, 125: 0.46, 250: 1.17, 500: 3.73, 1000: 12.7, 2000: 36, 4000: 69, 8000: 95.2}
            if self.rel_humidity == 40:
                alfa = {63: 0.19, 125: 0.42, 250: 0.92, 500: 2.63, 1000: 9, 2000: 29.8, 4000: 75.2, 8000: 127}
            if self.rel_humidity == 50:
                alfa = {63: 0.18, 125: 0.41, 250: 0.82, 500: 2.08, 1000: 6.83, 2000: 23.8, 4000: 71, 8000: 147}
            if self.rel_humidity == 60:
                alfa = {63: 0.16, 125: 0.4, 250: 0.77, 500: 1.78, 1000: 5.5, 2000: 19.3, 4000: 63.3, 8000: 154}
            if self.rel_humidity == 70:
                alfa = {63: 0.15, 125: 0.39, 250: 0.76, 500: 1.61, 1000: 4.64, 2000: 16.1, 4000: 55.5, 8000: 153}
            if self.rel_humidity == 80:
                alfa = {63: 0.13, 125: 0.37, 250: 0.75, 500: 1.51, 1000: 4.06, 2000: 13.8, 4000: 48.8, 8000: 147}
            if self.rel_humidity == 90:
                alfa = {63: 0.12, 125: 0.36, 250: 0.76, 500: 1.45, 1000: 3.66, 2000: 12.1, 4000: 43.2, 8000: 129}
            if self.rel_humidity == 100:
                alfa = {63: 0.18, 125: 0.35, 250: 0.76, 500: 1.42, 1000: 3.37, 2000: 10.8, 4000: 28.6, 8000: 129}

        if self.temp == 5:
            if self.rel_humidity == 10:
                alfa = {63: 0.35, 125: 0.97, 250: 3.11, 500: 9.34, 1000: 20, 2000: 28.5, 4000: 33.5, 8000: 41.8}
            if self.rel_humidity == 20:
                alfa = {63: 0.26, 125: 0.55, 250: 1.38, 500: 4.42, 1000: 14.8, 2000: 40.5, 4000: 73.7, 8000: 98.7}
            if self.rel_humidity == 30:
                alfa = {63: 0.22, 125: 0.49, 250: 1.38, 500: 2.74, 1000: 9.18, 2000: 30.9, 4000: 82.6, 8000: 147}
            if self.rel_humidity == 40:
                alfa = {63: 0.19, 125: 0.47, 250: 0.91, 500: 2.1, 1000: 6.48, 2000: 22.7, 4000: 72.5, 8000: 169}
            if self.rel_humidity == 50:
                alfa = {63: 0.17, 125: 0.45, 250: 0.89, 500: 1.82, 1000: 5.08, 2000: 17.5, 4000: 60.2, 8000: 168}
            if self.rel_humidity == 60:
                alfa = {63: 0.15, 125: 0.43, 250: 0.89, 500: 1.69, 1000: 4.29, 2000: 14.2, 4000: 50.2, 8000: 156}
            if self.rel_humidity == 70:
                alfa = {63: 0.13, 125: 0.41, 250: 0.89, 500: 1.64, 1000: 3.8, 2000: 12, 4000: 42.7, 8000: 142}
            if self.rel_humidity == 80:
                alfa = {63: 0.12, 125: 0.39, 250: 0.89, 500: 1.63, 1000: 3.5, 2000: 10.5, 4000: 37, 8000: 128}
            if self.rel_humidity == 90:
                alfa = {63: 0.11, 125: 0.37, 250: 0.89, 500: 1.64, 1000: 3.31, 2000: 9.39, 4000: 32.7, 8000: 116}
            if self.rel_humidity == 100:
                alfa = {63: 0.1, 125: 0.34, 250: 0.88, 500: 1.66, 1000: 3.2, 2000: 8.58, 4000: 29.4, 8000: 105}

        if self.temp == 10:
            if self.rel_humidity == 10:
                alfa = {63: 0.34, 125: 0.78, 250: 2.29, 500: 7.52, 1000: 21.6, 2000: 42.3, 4000: 57.3, 8000: 69.4}
            if self.rel_humidity == 20:
                alfa = {63: 0.27, 125: 0.57, 250: 1.2, 500: 3.27, 1000: 11, 2000: 36.2, 4000: 91.5, 8000: 154}
            if self.rel_humidity == 30:
                alfa = {63: 0.22, 125: 0.55, 250: 1.05, 500: 2.28, 1000: 6.77, 2000: 23.5, 4000: 76.6, 8000: 187}
            if self.rel_humidity == 40:
                alfa = {63: 0.18, 125: 0.52, 250: 1.04, 500: 1.98, 1000: 5.07, 2000: 16.8, 4000: 59, 8000: 177}
            if self.rel_humidity == 50:
                alfa = {63: 0.16, 125: 0.48, 250: 1.05, 500: 1.9, 1000: 4.26, 2000: 13.2, 4000: 46.7, 8000: 155}
            if self.rel_humidity == 60:
                alfa = {63: 0.13, 125: 0.44, 250: 1.05, 500: 1.9, 1000: 3.86, 2000: 11, 4000: 38.4, 8000: 134}
            if self.rel_humidity == 70:
                alfa = {63: 0.12, 125: 0.41, 250: 1.04, 500: 1.93, 1000: 3.66, 2000: 9.66, 4000: 32.8, 8000: 117}
            if self.rel_humidity == 80:
                alfa = {63: 0.1, 125: 0.37, 250: 1.02, 500: 1.97, 1000: 3.57, 2000: 8.76, 4000: 28.7, 8000: 103}
            if self.rel_humidity == 90:
                alfa = {63: 0.09, 125: 0.34, 250: 0.99, 500: 2, 1000: 3.54, 2000: 8.14, 4000: 25.7, 8000: 92.4}
            if self.rel_humidity == 100:
                alfa = {63: 0.08, 125: 0.32, 250: 0.96, 500: 2.03, 1000: 3.55, 2000: 7.71, 4000: 23.5, 8000: 83.7}

        if self.temp == 15:
            if self.rel_humidity == 10:
                alfa = {63: 0.35, 125: 0.73, 250: 1.78, 500: 5.58, 1000: 18.4, 2000: 49.3, 4000: 87.3, 8000: 114}
            if self.rel_humidity == 20:
                alfa = {63: 0.27, 125: 0.64, 250: 1.22, 500: 2.7, 1000: 8.17, 2000: 28.2, 4000: 88.8, 8000: 202}
            if self.rel_humidity == 30:
                alfa = {63: 0.21, 125: 0.6, 250: 1.21, 500: 2.23, 1000: 5.45, 2000: 17.7, 4000: 62, 8000: 190}
            if self.rel_humidity == 40:
                alfa = {63: 0.17, 125: 0.53, 250: 1.23, 500: 2.18, 1000: 4.51, 2000: 13.1, 4000: 45.7, 8000: 156}
            if self.rel_humidity == 50:
                alfa = {63: 0.14, 125: 0.47, 250: 1.22, 500: 2.24, 1000: 4.16, 2000: 10.8, 4000: 36.2, 8000: 129}
            if self.rel_humidity == 60:
                alfa = {63: 0.12, 125: 0.42, 250: 1.18, 500: 2.31, 1000: 4.06, 2000: 9.5, 4000: 30.3, 8000: 108}
            if self.rel_humidity == 70:
                alfa = {63: 0.1, 125: 0.38, 250: 1.13, 500: 2.36, 1000: 40.8, 2000: 8.75, 4000: 26.4, 8000: 93.7}
            if self.rel_humidity == 80:
                alfa = {63: 0.09, 125: 0.34, 250: 1.07, 500: 2.4, 1000: 4.15, 2000: 8.31, 4000: 23.7, 8000: 82.8}
            if self.rel_humidity == 90:
                alfa = {63: 0.08, 125: 0.31, 250: 1.02, 500: 2.41, 1000: 4.25, 2000: 8.07, 4000: 21.7, 8000: 74.6}
            if self.rel_humidity == 100:
                alfa = {63: 0.07, 125: 0.28, 250: 0.95, 500: 2.41, 1000: 4.35, 2000: 7.95, 4000: 20.3, 8000: 68.1}

        if self.temp == 20:
            if self.rel_humidity == 10:
                alfa = {63: 0.37, 125: 0.77, 250: 1.58, 500: 4.25, 1000: 14.1, 2000: 45.3, 4000: 109, 8000: 175}
            if self.rel_humidity == 20:
                alfa = {63: 0.26, 125: 0.71, 250: 1.39, 500: 2.6, 1000: 6.53, 2000: 21.5, 4000: 74.1, 8000: 215}
            if self.rel_humidity == 30:
                alfa = {63: 0.19, 125: 0.61, 250: 1.42, 500: 2.52, 1000: 5.01, 2000: 14.1, 4000: 48.5, 8000: 166}
            if self.rel_humidity == 40:
                alfa = {63: 0.15, 125: 0.52, 250: 1.39, 500: 2.63, 1000: 4.65, 2000: 11.2, 4000: 36.1, 8000: 128}
            if self.rel_humidity == 50:
                alfa = {63: 0.12, 125: 0.44, 250: 1.32, 500: 2.73, 1000: 4.66, 2000: 9.86, 4000: 29.4, 8000: 104}
            if self.rel_humidity == 60:
                alfa = {63: 0.1, 125: 0.38, 250: 1.23, 500: 2.79, 1000: 4.8, 2000: 9.25, 4000: 25.4, 8000: 87.8}
            if self.rel_humidity == 70:
                alfa = {63: 0.08, 125: 0.33, 250: 1.13, 500: 2.8, 1000: 4.98, 2000: 9.02, 4000: 22.9, 8000: 76.6}
            if self.rel_humidity == 80:
                alfa = {63: 0.07, 125: 0.3, 250: 1.04, 500: 2.77, 1000: 5.15, 2000: 8.98, 4000: 21.3, 8000: 68.6}
            if self.rel_humidity == 90:
                alfa = {63: 0.07, 125: 0.27, 250: 0.9, 500: 2.71, 1000: 5.3, 2000: 9.06, 4000: 20.2, 8000: 62.6}
            if self.rel_humidity == 100:
                alfa = {63: 0.06, 125: 0.24, 250: 0.89, 500: 2.63, 1000: 5.42, 2000: 9.21, 4000: 19.4, 8000: 58.1}

        if self.temp == 25:
            if self.rel_humidity == 10:
                alfa = {63: 0.37, 125: 0.86, 250: 1.61, 500: 3.56, 1000: 10.7, 2000: 36.6, 4000: 110, 8000: 233}
            if self.rel_humidity == 20:
                alfa = {63: 0.23, 125: 0.74, 250: 1.64, 500: 2.86, 1000: 5.87, 2000: 17, 4000: 58.8, 8000: 196}
            if self.rel_humidity == 30:
                alfa = {63: 0.16, 125: 0.59, 250: 1.6, 500: 3.04, 1000: 5.27, 2000: 12.2, 4000: 38.8, 8000: 137}
            if self.rel_humidity == 40:
                alfa = {63: 0.13, 125: 0.47, 250: 1.47, 500: 3.19, 1000: 5.39, 2000: 10.7, 4000: 30.1, 8000: 104}
            if self.rel_humidity == 50:
                alfa = {63: 0.1, 125: 0.39, 250: 1.32, 500: 3.23, 1000: 5.68, 2000: 10.2, 4000: 25.7, 8000: 85.4}
            if self.rel_humidity == 60:
                alfa = {63: 0.08, 125: 0.34, 250: 1.18, 500: 3.18, 1000: 5.96, 2000: 10.2, 4000: 23.2, 8000: 73.4}
            if self.rel_humidity == 70:
                alfa = {63: 0.07, 125: 0.29, 250: 1.06, 500: 3.08, 1000: 6.19, 2000: 10.4, 4000: 21.9, 8000: 65.4}
            if self.rel_humidity == 80:
                alfa = {63: 0.06, 125: 0.26, 250: 0.96, 500: 2.95, 1000: 6.35, 2000: 10.7, 4000: 21.1, 8000: 59.8}
            if self.rel_humidity == 90:
                alfa = {63: 0.06, 125: 0.21, 250: 0.8, 500: 2.8, 1000: 6.44, 2000: 11, 4000: 20.8, 8000: 55.8}
            if self.rel_humidity == 100:
                alfa = {63: 0.05, 125: 0.21, 250: 0.8, 500: 2.66, 1000: 6.47, 2000: 11.4, 4000: 20.6, 8000: 52.8}

        if self.temp == 30:
            if self.rel_humidity == 10:
                alfa = {63: 0.36, 125: 0.95, 250: 1.82, 500: 3.4, 1000: 8.67, 2000: 28.5, 4000: 96, 8000: 260}
            if self.rel_humidity == 20:
                alfa = {63: 0.21, 125: 0.72, 250: 1.87, 500: 3.41, 1000: 6, 2000: 14.5, 4000: 47.1, 8000: 165}
            if self.rel_humidity == 30:
                alfa = {63: 0.14, 125: 0.54, 250: 1.68, 500: 3.67, 1000: 6.15, 2000: 11.8, 4000: 32.7, 8000: 113}
            if self.rel_humidity == 40:
                alfa = {63: 0.11, 125: 0.42, 250: 1.45, 500: 3.7, 1000: 6.63, 2000: 11.4, 4000: 27, 8000: 87.1}
            if self.rel_humidity == 50:
                alfa = {63: 0.09, 125: 0.35, 250: 1.25, 500: 3.57, 1000: 7.03, 2000: 11.7, 4000: 24.5, 8000: 73.1}
            if self.rel_humidity == 60:
                alfa = {63: 0.07, 125: 0.29, 250: 1.09, 500: 3.36, 1000: 7.29, 2000: 12.2, 4000: 23.4, 8000: 64.7}
            if self.rel_humidity == 70:
                alfa = {63: 0.06, 125: 0.25, 250: 0.96, 500: 3.14, 1000: 7.41, 2000: 12.7, 4000: 23.1, 8000: 59.3}
            if self.rel_humidity == 80:
                alfa = {63: 0.05, 125: 0.22, 250: 0.86, 500: 2.91, 1000: 7.41, 2000: 13.3, 4000: 23.1, 8000: 55.7}
            if self.rel_humidity == 90:
                alfa = {63: 0.05, 125: 0.2, 250: 0.77, 500: 2.71, 1000: 7.32, 2000: 13.8, 4000: 23.5, 8000: 53.3}
            if self.rel_humidity == 100:
                alfa = {63: 0.04, 125: 0.18, 250: 0.7, 500: 2.52, 1000: 7.17, 2000: 14.2, 4000: 24, 8000: 51.8}

        if self.temp == 35:
            if self.rel_humidity == 10:
                alfa = {63: 0.33, 125: 1.01, 250: 2.13, 500: 3.66, 1000: 7.71, 2000: 22.8, 4000: 78.3, 8000: 249}
            if self.rel_humidity == 20:
                alfa = {63: 0.18, 125: 0.67, 250: 2, 500: 4.12, 1000: 6.82, 2000: 13.7, 4000: 39.3, 8000: 136}
            if self.rel_humidity == 30:
                alfa = {63: 0.12, 125: 0.48, 250: 1.65, 500: 4.22, 1000: 7.55, 2000: 12.8, 4000: 29.7, 8000: 94.5}
            if self.rel_humidity == 40:
                alfa = {63: 0.09, 125: 0.37, 250: 1.36, 500: 4, 1000: 8.15, 2000: 13.4, 4000: 26.5, 8000: 75.9}
            if self.rel_humidity == 50:
                alfa = {63: 0.07, 125: 0.3, 250: 1.14, 500: 3.66, 1000: 8.43, 2000: 14.2, 4000: 25.7, 8000: 66.2}
            if self.rel_humidity == 60:
                alfa = {63: 0.06, 125: 0.25, 250: 0.97, 500: 3.32, 1000: 8.45, 2000: 15.1, 4000: 25.8, 8000: 60.7}
            if self.rel_humidity == 70:
                alfa = {63: 0.05, 125: 0.22, 250: 0.85, 500: 3.01, 1000: 8.3, 2000: 15.9, 4000: 26.5, 8000: 57.7}
            if self.rel_humidity == 80:
                alfa = {63: 0.04, 125: 0.19, 250: 0.75, 500: 2.73, 1000: 8.03, 2000: 16.4, 4000: 27.4, 8000: 56}
            if self.rel_humidity == 90:
                alfa = {63: 0.04, 125: 0.17, 250: 0.67, 500: 2.5, 1000: 7.71, 2000: 16.8, 4000: 28.3, 8000: 55.2}
            if self.rel_humidity == 100:
                alfa = {63: 0.03, 125: 0.15, 250: 0.61, 500: 2.3, 1000: 7.37, 2000: 17.1, 4000: 29.3, 8000: 55}

        if self.temp == 40:
            if self.rel_humidity == 10:
                alfa = {63: 0.3, 125: 1.01, 250: 2.45, 500: 4.28, 1000: 7.68, 2000: 19.3, 4000: 63.6, 8000: 217}
            if self.rel_humidity == 20:
                alfa = {63: 0.16, 125: 0.61, 250: 2.02, 500: 4.82, 1000: 8.25, 2000: 14.3, 4000: 35, 8000: 114}
            if self.rel_humidity == 30:
                alfa = {63: 0.11, 125: 0.42, 250: 1.55, 500: 4.56, 1000: 9.24, 2000: 15, 4000: 29.3, 8000: 82.8}
            if self.rel_humidity == 40:
                alfa = {63: 0.08, 125: 0.32, 250: 1.23, 500: 4.04, 1000: 9.62, 2000: 16.4, 4000: 28.5, 8000: 69.9}
            if self.rel_humidity == 50:
                alfa = {63: 0.06, 125: 0.26, 250: 1.02, 500: 3.54, 1000: 9.52, 2000: 17.7, 4000: 29.2, 8000: 64}
            if self.rel_humidity == 60:
                alfa = {63: 0.05, 125: 0.22, 250: 0.86, 500: 3.12, 1000: 9.14, 2000: 18.6, 4000: 30.6, 8000: 61.4}
            if self.rel_humidity == 70:
                alfa = {63: 0.04, 125: 0.19, 250: 0.74, 500: 2.77, 1000: 8.66, 2000: 19.2, 4000: 32.1, 8000: 60.5}
            if self.rel_humidity == 80:
                alfa = {63: 0.04, 125: 0.16, 250: 0.66, 500: 2.48, 1000: 8.14, 2000: 19.4, 4000: 33.7, 8000: 60.7}
            if self.rel_humidity == 90:
                alfa = {63: 0.03, 125: 0.15, 250: 0.59, 500: 2.25, 1000: 7.62, 2000: 19.4, 4000: 35.1, 8000: 61.5}
            if self.rel_humidity == 100:
                alfa = {63: 0.03, 125: 0.13, 250: 0.53, 500: 2.05, 1000: 7.14, 2000: 19.3, 4000: 36.3, 8000: 62.7}

        if self.temp == 45:
            if self.rel_humidity == 10:
                alfa = {63: 0.27, 125: 0.96, 250: 2.68, 500: 5.15, 1000: 8.45, 2000: 17.8, 4000: 53, 8000: 183}
            if self.rel_humidity == 20:
                alfa = {63: 0.14, 125: 0.54, 250: 1.93, 500: 5.34, 1000: 10.1, 2000: 16.3, 4000: 33.5, 8000: 98.9}
            if self.rel_humidity == 30:
                alfa = {63: 0.09, 125: 0.37, 250: 1.41, 500: 4.61, 1000: 10.9, 2000: 18.4, 4000: 31.5, 8000: 76.6}
            if self.rel_humidity == 40:
                alfa = {63: 0.07, 125: 0.28, 250: 1.1, 500: 3.88, 1000: 10.7, 2000: 20.2, 4000: 32.9, 8000: 68.8}
            if self.rel_humidity == 50:
                alfa = {63: 0.05, 125: 0.23, 250: 0.89, 500: 3.29, 1000: 10, 2000: 21.4, 4000: 35.2, 8000: 66.5}
            if self.rel_humidity == 60:
                alfa = {63: 0.04, 125: 0.19, 250: 0.75, 500: 2.84, 1000: 9.27, 2000: 21.9, 4000: 37.5, 8000: 66.6}
            if self.rel_humidity == 70:
                alfa = {63: 0.04, 125: 0.16, 250: 0.65, 500: 2.49, 1000: 8.51, 2000: 21.9, 4000: 39.7, 8000: 68}
            if self.rel_humidity == 80:
                alfa = {63: 0.03, 125: 0.14, 250: 0.57, 500: 2.22, 1000: 7.82, 2000: 21.6, 4000: 41.5, 8000: 70}
            if self.rel_humidity == 90:
                alfa = {63: 0.03, 125: 0.13, 250: 0.51, 500: 1.99, 1000: 7.2, 2000: 21, 4000: 42.9, 8000: 72.4}
            if self.rel_humidity == 100:
                alfa = {63: 0.02, 125: 0.11, 250: 0.46, 500: 1.81, 1000: 6.65, 2000: 20.3, 4000: 43.9, 8000: 74.8}

        if self.temp == 50:
            if self.rel_humidity == 10:
                alfa = {63: 0.24, 125: 0.89, 250: 2.78, 500: 6.09, 1000: 9.95, 2000: 17.9, 4000: 46.4, 8000: 155}
            if self.rel_humidity == 20:
                alfa = {63: 0.12, 125: 0.48, 250: 1.79, 500: 5.55, 1000: 12.1, 2000: 19.6, 4000: 34.9, 8000: 89.7}
            if self.rel_humidity == 30:
                alfa = {63: 0.08, 125: 0.33, 250: 1.27, 500: 4.44, 1000: 12.1, 2000: 22.6, 4000: 36.3, 8000: 75.4}
            if self.rel_humidity == 40:
                alfa = {63: 0.06, 125: 0.25, 250: 0.97, 500: 3.6, 1000: 11.1, 2000: 24.3, 4000: 39.8, 8000: 72.6}
            if self.rel_humidity == 50:
                alfa = {63: 0.05, 125: 0.2, 250: 0.78, 500: 2.99, 1000: 10, 2000: 24.8, 4000: 43.2, 8000: 73.8}
            if self.rel_humidity == 60:
                alfa = {63: 0.04, 125: 0.16, 250: 0.66, 500: 2.55, 1000: 8.94, 2000: 24.4, 4000: 46.1, 8000: 76.7}
            if self.rel_humidity == 70:
                alfa = {63: 0.03, 125: 0.14, 250: 0.57, 500: 2.22, 1000: 8.03, 2000: 23.6, 4000: 48.2, 8000: 80.3}
            if self.rel_humidity == 80:
                alfa = {63: 0.03, 125: 0.12, 250: 0.5, 500: 1.96, 1000: 7.25, 2000: 22.5, 4000: 49.6, 8000: 84.1}
            if self.rel_humidity == 90:
                alfa = {63: 0.02, 125: 0.13, 250: 0.44, 500: 1.76, 1000: 6.6, 2000: 21.4, 4000: 50.4, 8000: 87.8}
            if self.rel_humidity == 100:
                alfa = {63: 0.02, 125: 0.1, 250: 0.4, 500: 1.59, 1000: 6.05, 2000: 20.3, 4000: 50.6, 8000: 91.2}

        attenuation_atm = {}
        for band in self.level_input:
           attenuation_atm[band] = (alfa[band] * self.distance)/1000.

        return attenuation_atm

class Diffraction(object):
    '''
    CLASS TO CALCULATE DIFFRACTION
    Input data:
    - model: KURZEANDERSON, STEPHENSON, MAEKAWA1, MAEKAWA2, CNOSSOS
    - level_input: has to be a dict with keys [63, 125, 250, 500, 1000 , 2000, 4000, 8000] and value the levels in bands
    - d_diffTOsource: distance in meters from diffraction point to source point
    - d_recTOsource: distance in meters from receiver point to source point
    - d_recTOdiff: distance in meters from receiver point to diffraction point

    The output is dict:
    - function finale_level: initial level - attenuation
    - attenuation: only the attenuation
    '''

    def __init__(self, model,level_input,d_diffTOsource,d_recTOsource,d_recTOdiff,temp):

        self.model = model
        self.level_input = level_input
        self.d_diffTOsource = d_diffTOsource
        self.d_recTOsource = d_recTOsource
        self.d_recTOdiff = d_recTOdiff
        self.temp = float(temp)


        self.sound_speed = 331.6+0.6*self.temp  # Expressed in m/s
        self.delta =  float (d_recTOdiff + d_diffTOsource - d_recTOsource)


    def level(self):

        level_diff = {}

        attenuation = self.attenuation()

        # version 1.4
        # level_diff consider the total distance
        d_recPLUSsource = self.d_recTOdiff+self.d_diffTOsource
        for band in self.level_input:
            level_diff[band] = round(self.level_input[band] - GeometricalAttenuation('spherical',d_recPLUSsource) - attenuation[band],1)


        return level_diff



    def attenuation(self):

        if self.model == 'KURZEANDERSON':
            attenuation = self.KURZEANDERSON()
        elif self.model == 'STEPHENSON':
            attenuation = self.STEPHENSON()
        elif self.model == 'MAEKAWA1':
            attenuation = self.MAEKAWA1()
        elif self.model == 'MAEKAWA2':
            attenuation = self.MAEKAWA2()
        elif self.model == 'CNOSSOS':
            attenuation = self.CNOSSOS()

        return attenuation

    def fresnel_number(self):
        N ={}               # Fresnel Number Dict
        for band in self.level_input:
            wave_length = self.sound_speed / float(band)
#            print 'delta ', self.delta
            N[band]= 2 * self.delta / wave_length
        return N

    def KURZEANDERSON(self):
        N = self.fresnel_number()
        KA = {}
        for band in self.level_input:
#            print 'xxxxxxxxxxxxxxxxxxxxxxx'
#            print N[band]
#            print tanh(sqrt(2*pi*abs(N[band])))
            KurzeAnderson = 5 + 20* log10((sqrt(2*pi*abs(N[band])))/(tanh(sqrt(2*pi*abs(N[band])))))  # Kurze-Anderson formula
            KA[band] = round(KurzeAnderson,1)

        return KA

    def STEPHENSON(self):
        N = self.fresnel_number()
        Step = {}
        for band in self.level_input:
            Stephensons = 10* log10 (.5 - (atan((1./sqrt(3.))+6*abs(N[band])*(1+exp(-3.*abs(N[band]))))/pi)) # Stephenson formula
            Step[band] = round(-1*Stephensons,2)

        return Step

    def MAEKAWA1(self):
        N = self.fresnel_number()
        Maek1 = {}
        for band in self.level_input:
            Maekawa1 = 10* log10(20*abs(N[band])) # Maekawa Correction formula
            Maek1[band] = round(Maekawa1,2)

        return Maek1

    def MAEKAWA2(self):
        N = self.fresnel_number()
        Maek2 = {}
        for band in self.level_input:
            Maekawa2 = 10.* log10(2. + 5.5*abs(N[band])) # Maekawa formula
            Maek2[band] = round(Maekawa2,2)

        return Maek2

    def CNOSSOS(self):

        # Version 1.4
        # modified diffraction as formula 2.5.21 EU DIRECTIVE 2015/996
        # Semi_Perim = (self.d_diffTOsource + self.d_recTOsource + self.d_recTOdiff)/2
        # h = round((2./self.d_recTOsource) * sqrt(Semi_Perim*(Semi_Perim - self.d_diffTOsource)*(Semi_Perim - self.d_recTOsource)*(Semi_Perim - self.d_recTOdiff)),2)
        Ch = {}
        Att_dic = {}
        C2nd = 1

        for band in self.level_input:
            wave_length = self.sound_speed/float(band)

            if (40./wave_length)*self.delta < -2:
                Att = 0
                Att_dic[band] = Att
            else:
                # removed according to the 2.5.21
                # Ch[band] = min(band*h/250.,1)
                Ch[band] = 1

                if (40/wave_length)*C2nd*self.delta >= -2:
                    Att = 10*Ch[band]*log10(3+(40/wave_length)*self.delta)
                else:
                    Att = 0
                #     limitation to Att
                if Att <0:
                    Att=0
                if Att > 25:
                    Att=25


                Att_dic[band] = round(Att, 2)

        return Att_dic

class Diffraction3D(object):
    '''
    CLASS TO CALCULATE DIFFRACTION in £D
    Input data:
    - delta: distance in 3d from source to
    - level_input: has to be a dict with keys [63, 125, 250, 500, 1000 , 2000, 4000, 8000] and value the levels in bands
    - epsilon: distance in 3D of all obstacles

    Reference Equation is 2.5.23 Allegato_2 22-12-2021
    The output is dict:
    -
    '''
    def __init__(self, level_input, distSUP3D, eDist, dInclinata, temperature):

        self.temp = float(temperature)
        self.level_input = level_input
        self.distSUP3D = distSUP3D
        self.dInclinata = dInclinata
        self.epsilon = eDist
        self.sound_speed = 331.6 + 0.6 * self.temp
        self.d = distSUP3D - dInclinata

    def attenuation(self):
        Att_dic = {}
        Ch = 1

        for band in self.level_input:
            wave_length = self.sound_speed / float(band)
            c2nd = (1. + (5 * wave_length / self.epsilon) ** 2) / (1 / 3. + (5 * wave_length / self.epsilon) ** 2)
            if 40./wave_length * c2nd * self.d >= -2:
                Att = 10*Ch*log10(3 + (40 / wave_length * c2nd * self.d))
                if Att < 0:
                    Att = 0
                if Att > 25:
                    Att = 25
                Att_dic[band] = round(Att, 2)
            else:
                Att = 0
                Att_dic[band] = round(Att, 2)
         
        return Att_dic


    def level3D(self):
        level_diff = {}

        attenuation = self.attenuation()

        for band in self.level_input:
            level_diff[band] = round(self.level_input[band] - GeometricalAttenuation('spherical',self.distSUP3D) - attenuation[band],1)

        return level_diff







class CNOSSOS(object):

    def __init__(self, input_dict):
        self.input_dict = input_dict

    def bands(self):
        return on_Acoustics_CNOSSOS.CNOSSOS(self.input_dict).bands()

    def overall(self):
        return on_Acoustics_CNOSSOS.CNOSSOS(self.input_dict).bands().overall()


class NMPB(object):

    def __init__(self, input_dict):
        self.input_dict = input_dict

    def bands(self):
        return on_Acoustics_NMPB.NMPB(self.input_dict).bands()

    def overall(self):
        return on_Acoustics_NMPB.NMPB(self.input_dict).overall()






#
#level_emi_bands = GlobalToOctaveBands('ISO_traffic_road',70)
#print level_emi_bands
#d_diffTOsource = 35.8
#d_recTOsource = 31.96
#d_recTOdiff = 13.84
#print 'deltaaaa' , d_recTOdiff + d_diffTOsource - d_recTOsource
#band = Diffraction('KURZEANDERSON',level_emi_bands,d_diffTOsource,d_recTOsource,d_recTOdiff).level()
#print band
#print OctaveBandsToGlobal(band)


################################################################################################



#ii = {4000: 67.5, 8000: 59.4, 1000: 77.9, 2000: 74.9, 500: 73.5, 250: 71.9, 125: 72.6, 63: 77.9}
#a = AtmosphericAbsorption((6.37+31.62),20,70,ii).level()
#c = Diffraction('CNOSSOS',ii ,31.62,33.69,6.37).attenuation()
#d = DiffBands(a,c)
#b = GeometricalAttenuation('spherical',33.69)
#
#
#print OctaveBandsToGlobal(d)




#gg =AtmosphericAbsorption((6.37+31.62),20,70,ii).attenuation()
#
#print gg

################################################################################################




#print NMPB(10,10,10,10,'continuos','smooth','flat').bands()

#print CNOSSOS(10,10,0,
#        0,0,
#        0,0,
#        0,0,
#        0,0,
#        0,0,
#        0,'k=1',100,20,0).overall()
##
#
#

#print level
#print OctaveBandsToGlobal(level)
#print Diffraction('CNOSSOS',level,10,8,11).level()
#print Diffraction('MAEKAWA2',level,10,8,11).level()
#print OctaveBandsToGlobal(Diffraction('KURZEANDERSON',level,10,8,11).level())

#level_ini = GlobalToOctaveBands('CNOSSOS',100)
#print level_ini
#
#l =  Diffraction('KURZEANDERSON',level_ini,42.35,43.92,6.37).level()
#a = Diffraction('KURZEANDERSON',level_ini,42.35,43.92,6.37).attenuation()
#print 'level',l
#print 'att', a
#
#print 'level global',OctaveBandsToGlobal(l)
#print 'att global', OctaveBandsToGlobal(a)
#print 20 * log10(43.92) + 11
