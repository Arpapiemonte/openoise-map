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

from builtins import str
from builtins import range
from builtins import object
from math import log10
import numpy
import os
import xml.etree.ElementTree as ET


class CNOSSOS(object):
    """ Arguments:

    """
    def __init__(self, input_dict):

        self.input_dict = input_dict
        self.Ts = self.input_dict['Ts']
        self.k = self.input_dict['k']
        self.dist_intersection = self.input_dict['dist_intersection']
        self.temperature = self.input_dict['temperature']
        try:
            self.slope = (self.input_dict['slope']) / 100.
        except:
            self.slope = 0
        try:
            self.surface = self.input_dict['surface'].upper()
        except:
            self.surface = '0'

        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        tree = ET.parse(os.path.join(dir_path,"on_Acoustics_CNOSSOS_Road_Params.xml"))
        tree_1 = ET.parse(os.path.join(dir_path,"on_Acoustics_CNOSSOS_Road_Surfaces.xml"))
        self.root = tree.getroot()
        self.root1 = tree_1.getroot()
        self.speed_reference = float(self.root[1].text)
        self.temp_reference = float(self.root[3].text)
        self.vehicles_classes = {}
        self.surfaces_classes = {'0':0,'NL01':1,'NL02':2,'NL03':3,'NL04':4, 'NL05':5,'NL06':6, 'NL07':7, 'NL08':8, 'NL09':9, 'NL10':10, 'NL11':11, 'NL12':12, 'NL13':13, 'NL14':14}
        self.CNOSSOS_Road_Params = {}
        self.CNOSSOS_Surface_Params = {}

    def road_param(self,m):     # Read the xml cnossos file and creates the Dictionary CNOSSOS_Road_Params with the tables III.A.1,2,3,4,5

        Ar_temp = self.root[6][self.vehicles_classes.get(m)-1].attrib.get('Ar').split()            # Gets the coefficient Ar from the xlm File for each catergory of vehicles
        Br_temp = self.root[6][self.vehicles_classes.get(m)-1].attrib.get('Br').split()            # Gets the coefficient Br from the xlm File for each catergory of vehicles
        Ap_temp = self.root[6][self.vehicles_classes.get(m)-1].attrib.get('Ap').split()            # Gets the coefficient Ap from the xlm File for each catergory of vehicles
        Bp_temp = self.root[6][self.vehicles_classes.get(m)-1].attrib.get('Bp').split()            # Gets the coefficient Bp from the xlm File for each catergory of vehicles
        a_temp  = self.root[4][self.vehicles_classes.get(m)-1].attrib.get('Astudded').split()      # Gets the coefficient Astudded from the xlm File for each catergory of vehicles
        b_temp  = self.root[4][self.vehicles_classes.get(m)-1].attrib.get('Bstudded').split()      # Gets the coefficient Bstudded from the xlm File for each catergory of vehicles


        Cr = {}
        Cp = {}

        for aaa in self.root[7][self.vehicles_classes.get(m)-1].iter('Type'):
            k = 'k=' + str(aaa.get('k'))
            Cr[k] = aaa.get('Cr')       # Gets the coefficient Cr from the xlm File for each catergory of vehicles
            Cp[k] = aaa.get('Cp')       # Gets the coefficient Cp from the xlm File for each catergory of vehicles


        # Creates a Dictionary with the corresponding coefficients for each frequency

        Ar = {63: float(Ar_temp[0]), 125: float(Ar_temp[1]),250: float(Ar_temp[2]), 500: float(Ar_temp[3]), 1000: float(Ar_temp[4]), 2000: float(Ar_temp[5]), 4000: float(Ar_temp[6]),8000: float(Ar_temp[7])}
        Br = {63: float(Br_temp[0]), 125: float(Br_temp[1]),250: float(Br_temp[2]), 500: float(Br_temp[3]), 1000: float(Br_temp[4]), 2000: float(Br_temp[5]), 4000: float(Br_temp[6]),8000: float(Br_temp[7])}
        Ap = {63: float(Ap_temp[0]), 125: float(Ap_temp[1]),250: float(Ap_temp[2]), 500: float(Ap_temp[3]), 1000: float(Ap_temp[4]), 2000: float(Ap_temp[5]), 4000: float(Ap_temp[6]),8000: float(Ap_temp[7])}
        Bp = {63: float(Bp_temp[0]), 125: float(Bp_temp[1]),250: float(Bp_temp[2]), 500: float(Bp_temp[3]), 1000: float(Bp_temp[4]), 2000: float(Bp_temp[5]), 4000: float(Bp_temp[6]),8000: float(Bp_temp[7])}
        a  = {63: float(a_temp[0]) , 125: float(a_temp[1]), 250: float(a_temp[2]) , 500: float(a_temp[3]) , 1000: float(a_temp[4]) , 2000: float(a_temp[5]) , 4000: float(a_temp[6]) ,8000: float(a_temp[7])}
        b  = {63: float(b_temp[0]) , 125: float(b_temp[1]), 250: float(b_temp[2]) , 500: float(b_temp[3]) , 1000: float(b_temp[4]) , 2000: float(b_temp[5]) , 4000: float(b_temp[6]) ,8000: float(b_temp[7])}


        params = {}
        params['Ar'] = Ar
        params['Br'] = Br
        params['Ap'] = Ap
        params['Bp'] = Bp
        params['a']  = a
        params['b']  = b
        params['Cr'] = Cr
        params['Cp'] = Cp

        if m == '1':
            params['K'] = 0.08
        elif m == '2' or m == '3':
            params['K'] = 0.04
        else:
            params['K'] = 0.00

        self.CNOSSOS_Road_Params[m] = params

        return self.CNOSSOS_Road_Params[m]

    def surface_param(self,m):                       # Read the xml cnossos file and creates the Dictionary CNOSSOS_Surface_Params with the tables in CNOSSOS-EU_Road_Catalogue_Final_20-April2014

        ID = self.surfaces_classes.get(self.surface)

        alfa = self.root1[1][ID][self.vehicles_classes[m]-1].attrib.get('A').split()
        beta = self.root1[1][ID][self.vehicles_classes[m]-1].attrib.get('B').split()
        vmin = self.root1[1][ID].attrib.get('Vmin')
        vmax =self.root1[1][ID].attrib.get('Vmax')

        alfa_bands = {63: float(alfa[0]), 125: float(alfa[1]),250: float(alfa[2]), 500: float(alfa[3]), 1000: float(alfa[4]), 2000: float(alfa[5]), 4000: float(alfa[6]),8000: float(alfa[7])}

        surf_params = {}
        surf_params['Alfa'] = alfa_bands
        surf_params['Beta'] = beta
        surf_params['Vmin'] = float(vmin)
        surf_params['Vmax'] = float(vmax)

        self.CNOSSOS_Surface_Params[m] = surf_params

        return self.CNOSSOS_Surface_Params[m]


    def bands(self):

        for i in range(6):
            if str(i)+'_n' in self.input_dict and str(i)+'_s' in self.input_dict and self.input_dict[str(i)+'_n'] > 0 and self.input_dict[str(i)+'_s'] > 0 :
                self.vehicles_classes[str(i)]= i
            if i == 4:
                if str(i)+'a_n' in self.input_dict and str(i)+'a_s' in self.input_dict and self.input_dict[str(i)+'a_n'] > 0 and self.input_dict[str(i)+'a_s'] > 0 :
                    self.vehicles_classes['4a']= 4
                if str(i)+'b_n' in self.input_dict and str(i)+'b_s' in self.input_dict and self.input_dict[str(i)+'b_n'] > 0 and self.input_dict[str(i)+'b_s'] > 0 :
                    self.vehicles_classes['4b']= 5

        # con tutte le bande
        #bands = [63, 125, 250, 500, 1000 , 2000, 4000, 8000]
        # escludendo bande 63 e 8000
        bands = [125, 250, 500, 1000 , 2000, 4000]

        p = {}
        p_all_vehicles = {}

        for band in bands:
            p[band] = 0
            p_all_vehicles[band] = 0


        for m in list(self.vehicles_classes.keys()):

            speed = 0
            flow = 0

            if m == '1':
                speed = float(self.input_dict['1_s'])
                flow = float(self.input_dict['1_n'])
            elif m == '2':
                speed = float(self.input_dict['2_s'])
                flow = float(self.input_dict['2_n'])
            elif m == '3':
                speed = float(self.input_dict['3_s'])
                flow = float(self.input_dict['3_n'])
            elif m == '4a':
                speed = float(self.input_dict['4a_s'])
                flow = float(self.input_dict['4a_n'])
            elif m == '4b':
                speed = float(self.input_dict['4b_s'])
                flow = float(self.input_dict['4b_n'])
            elif m == '5':
                speed = float(self.input_dict['5_s'])
                flow = float(self.input_dict['5_n'])

            if speed > 0 and flow > 0:
                for f in list(p.keys()):
                    p[f] = round(10*log10(numpy.power(10,self.L_rolling(m,f,speed)/10)+ numpy.power(10,self.L_propagation(m,f,speed)/10)) + 10*log10(flow/(1000*speed)),1)

                    p_all_vehicles[f] = round(10*log10(numpy.power(10,p_all_vehicles[f]/10.) + numpy.power(10,p[f]/10.)),1)

        return p_all_vehicles


    def overall(self):

        p =self.bands()

        p_overall = 0

        for f in list(p.keys()):
            if p[f] > 0:
                p_overall = round(10*log10(numpy.power(10,p_overall/10.) + numpy.power(10,p[f]/10.)),1)

        return p_overall


    def L_rolling(self,m,f,speed):                  # L_rolling as pag. 34, cap. III.2.3, formula III-5

        self.CNOSSOS_Road_Params[m] = self.road_param(m)

        # delta_Lroad
        if m == '1' or m == '2' or m == '3':
            self.CNOSSOS_Surface_Params[m] = self.surface_param(m)

            if speed < self.CNOSSOS_Surface_Params[m]['Vmin']:
                speed = self.CNOSSOS_Surface_Params[m]['Vmin']

            if speed > self.CNOSSOS_Surface_Params[m]['Vmax']:
                speed = self.CNOSSOS_Surface_Params[m]['Vmax']

            delta_Lroad = float(self.CNOSSOS_Surface_Params[m]['Alfa'][f]) + float(self.CNOSSOS_Surface_Params[m]['Beta'][0]) * log10(speed/self.speed_reference)

        else:
            delta_Lroad = 0

        # delta_Lstudd
        if m == '1':
            if speed  < 50:
                c = 50./70.
            elif speed  > 90:
                c = 90./70.
            else:
                c = (speed/70.)

            delta_studd = float(self.CNOSSOS_Road_Params[m]['a'][f])+float(self.CNOSSOS_Road_Params[m]['b'][f])*(log10(c))

            if self.input_dict['1_n'] != 0:
                ps = (self.input_dict['1_qstudd']/self.input_dict['1_n'])*(self.Ts/12.)
            else:
                ps = 0

            delta_Lstudd = 10*log10((1-ps)+ ps * numpy.power(10,(delta_studd/10.)))

        else:
            delta_Lstudd = 0

        # delta_Lacc
        if self.dist_intersection == 0:
            delta_Lacc = 0
        else:
            delta_Lacc = float(self.CNOSSOS_Road_Params[m]['Cr'][self.k]) * max([1.-(float(self.dist_intersection)/100.),0.])

        # delta_Ltemp
        delta_Ltemp = self.CNOSSOS_Road_Params[m]['K']* (self.temp_reference - self.temperature)

        delta_sum = delta_Lroad + delta_Lstudd + delta_Lacc + delta_Ltemp

        return self.CNOSSOS_Road_Params[m]['Ar'][f] + self.CNOSSOS_Road_Params[m]['Br'][f] * log10(speed/self.speed_reference) + delta_sum


    def L_propagation(self,m,f,speed):             # L_propagation as pag. 37, cap. III.2.4, formula III-11

        # delta_Lroad
        if self.surface == 'NL01':

            self.CNOSSOS_Surface_Params[m] = self.surface_param(m)

            delta_Lroad = min(self.CNOSSOS_Surface_Params[m]['Alfa'][f],0)
        else:
            delta_Lroad = 0

        # delta_Lacc
        if self.dist_intersection == 0:
            delta_Lacc = 0
        else:
            delta_Lacc = float(self.CNOSSOS_Road_Params[m]['Cp'][self.k]) * max([1.-(float(self.dist_intersection)/100.),0.])

        # delta_grad
        if m == '1':
            if self.slope > 0.02:
                delta_Lgrad = ((min([self.slope,0.12])-0.02)/(0.015))*(speed/100.)
            elif self.slope < -0.06:
                delta_Lgrad = (min([-self.slope,0.12])-0.06)/0.01
            else:
                delta_Lgrad = 0
        elif m == '2':
            if self.slope > 0.00:
                delta_Lgrad = min([self.slope,0.12])/0.01*(speed/100.)
            elif self.slope < -0.04:
                delta_Lgrad = ((min([-self.slope,0.12])-0.04)/0.007)*(speed-20)/100
            else:
                delta_Lgrad = 0
        elif m == '3':
            if self.slope > 0.00:
                delta_Lgrad = min([self.slope,0.12])/0.008*(speed/100.)
            elif self.slope < -0.04:
                delta_Lgrad = ((min([-self.slope,0.12])-0.04)/0.005)*(speed-10)/100
            else:
                delta_Lgrad = 0
        else:
            delta_Lgrad = 0

        delta_sum = delta_Lroad + delta_Lacc + delta_Lgrad

        return self.CNOSSOS_Road_Params[m]['Ap'][f] + self.CNOSSOS_Road_Params[m]['Bp'][f] *(speed - self.speed_reference)/self.speed_reference + delta_sum

#prova = {}
#
#prova['1_n'] = 233
#prova['1_s'] = 70
#prova['2_n'] = 8
#prova['2_s'] = 70
#prova['3_n'] = 1
#prova['3_s'] = 65
#prova['4a_n'] = 5
#prova['4a_s'] = 70
#prova['4b_n'] = 10
#prova['4b_s'] = 70
#prova['5_n'] = None
#prova['5_s'] = None
#
#prova['Ts'] = 0
#prova['1_qstudd'] = 0
#prova['k'] = 'k=1'
#prova['dist_intersection'] = 100
#prova['temperature'] = 20
#prova['slope'] = 0
#prova['surface'] = 'NL05'
##
#print CNOSSOS(prova).overall()
