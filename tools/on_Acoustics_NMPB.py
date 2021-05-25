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
from __future__ import print_function


from builtins import str
from builtins import object
from math import log10
import traceback

class NMPB(object):
    """ Arguments:
        - light_number: number of light vehicles per hour (number)
        - heavy_number: number of heavy vehicles per hour (number)
        - light_speed: speed of light vehicles (number)
        - heavy_speed: speed of heavy vehicles (number)
        - traffic: type of the traffic flow (string: 'continuous','pulsed accelerated', 'pulsed decelerated', 'non-differentiated pulsed')
        - surface: type of road surface (string: 'smooth','porous','stones','cement','corrugated')
        - slope: slope of the road (string: 'flat', 'down', 'up')
    """
    def __init__(self, input_dict):

        if 'l_n' in input_dict:
            self.light_number = input_dict['l_n']
        else:
            self.light_number = 0

        if 'h_n' in input_dict:
            self.heavy_number = input_dict['h_n']
        else:
            self.heavy_number = 0

        if 'l_s' in input_dict:
            self.light_speed = input_dict['l_s']
        else:
            self.light_speed = 0

        if 'h_s' in input_dict:
            self.heavy_speed = input_dict['h_s']
        else:
            self.heavy_speed = 0

        if 'type' in input_dict:
            self.traffic = input_dict['type'].lower()
        else:
            self.traffic = 'continuous'

        if 'surface' in input_dict:
            self.surface = input_dict['surface'].lower()
        else:
            self.surface = 'smooth'

        if 'slope' in input_dict:
            self.slope = input_dict['slope'].lower()
        else:
            self.slope = 'flat'

    def __str__(self):
        return '(' + \
                'light_number=' + str(self.light_number) + '; ' +\
                'heavy_number=' + str(self.heavy_number) + '; ' +\
                'light_speed=' + str(self.light_speed) + '; ' +\
                'heavy_speed=' + str(self.heavy_speed) + '; ' + \
                'slope=' + str(self.slope) + '; ' +\
                'traffic=' + str(self.traffic) + '; ' +\
                'surface=' + str(self.surface) + '; ' +\
                'power=' + str(self.run()) + ')'

    def overall(self):

        try:
            return round(self.run(),1)
        except:
            # fix_print_with_import
            print(traceback.format_exc())
            return 0

    def bands(self):

        power_bands = {}

        bands = [125, 250, 500, 1000 , 2000, 4000]

        try:
            iso_traffic_spectrum = {125 : -10.2, 250 : -10.2, 500 : -7.2, 1000 : -3.9, 2000 : -6.4, 4000 : -11.4}

            overall = self. overall()

            for band in bands:
                power_bands[band] = round(overall + iso_traffic_spectrum[band],1)

            return power_bands

        except:
            for band in bands:
                power_bands[band] = 0

            return power_bands

            # fix_print_with_import
            print(traceback.format_exc())
            return 0

    def run(self):
        # light vehicles
        if self.light_speed < 20:
            self.light_speed = 20
        if self.traffic == 'continuous':
            if self.slope == 'flat' or self.slope == 'down':
                if self.light_speed < 44:
                    E_o_l = 29.4
                    a_l = 0
                else:
                    E_o_l = 22.0
                    a_l = 21.6

            if self.slope == 'up':
                if self.light_speed < 43:
                    E_o_l = 37.0
                    a_l = -10.0
                elif self.light_speed >= 43 and self.light_speed < 80:
                    E_o_l = 32.1
                    a_l = 4.8
                else:
                    E_o_l = 22.0
                    a_l = 21.6

        if self.traffic == 'pulsed accelerated':
            if self.slope == 'flat':
                if self.light_speed < 50:
                    E_o_l = 37.2
                    a_l = -10.0
                elif self.light_speed >= 50 and self.light_speed < 64:
                    E_o_l = 33.0
                    a_l = 0
                else:
                    E_o_l = 22.0
                    a_l = 21.6

            if self.slope == 'up':
                if self.light_speed < 32:
                    E_o_l = 37.0
                    a_l = -10.0
                else:
                    E_o_l = 34.0
                    a_l = 5.2

            if self.slope == 'down':
                if self.light_speed < 40:
                    E_o_l = 34.0
                    a_l = -9.3
                elif self.light_speed >= 40 and self.light_speed < 53:
                    E_o_l = 31.2
                    a_l = 0
                else:
                    E_o_l = 22.0
                    a_l = 21.6

        if self.traffic == 'non-differentiated pulsed':
            if self.slope == 'flat' or self.slope == 'down':
                if self.light_speed < 40:
                    E_o_l = 34.0
                    a_l = -9.3
                elif self.light_speed >= 40 and self.light_speed < 53:
                    E_o_l = 31.2
                    a_l = 0
                else:
                    E_o_l = 22.0
                    a_l = 21.6

            if self.slope == 'up':
                if self.light_speed < 43:
                    E_o_l = 37.0
                    a_l = -10.0
                elif self.light_speed >= 43 and self.light_speed < 80:
                    E_o_l = 32.1
                    a_l = 4.8
                else:
                    E_o_l = 22.0
                    a_l = 21.6

        if self.traffic == 'pulsed decelerated':
            if self.slope == 'flat':
                if self.light_speed < 60:
                    E_o_l = 29.4
                    a_l = 0
                elif self.light_speed >= 60 and self.light_speed < 100:
                    E_o_l = 13.0
                    a_l = 34.3
                else:
                    E_o_l = 22.0
                    a_l = 21.6
            if self.slope == 'up':
                if self.light_speed < 40:
                    E_o_l = 34.0
                    a_l = -9.3
                elif self.light_speed >= 40 and self.light_speed < 53:
                    E_o_l = 31.2
                    a_l = 0
                else:
                    E_o_l = 22.0
                    a_l = 21.6
            if self.slope == 'down':
                if self.light_speed < 60:
                    E_o_l = 27.1
                    a_l = 0
                else:
                    E_o_l = 11.3
                    a_l = 33.8

        # heavy vehicles
        if self.heavy_speed < 20:
            self.heavy_speed = 20

        if self.traffic == 'continuous' or self.traffic == 'pulsed accelerated' or self.traffic == 'non-differentiated pulsed':
            if self.slope == 'flat' or self.slope == 'down':
                if self.heavy_speed < 51:
                    E_o_h = 47.0
                    a_h = -10.3
                elif self.heavy_speed >= 51 and self.heavy_speed < 70:
                    E_o_h = 42.8
                    a_h = 0
                else:
                    E_o_h = 32.3
                    a_h = 19.4
            if self.slope == 'up':
                if self.heavy_speed < 63:
                    E_o_h = 48
                    a_h = -10.4
                elif self.heavy_speed >= 63 and self.heavy_speed < 70:
                    E_o_h = 42.8
                    a_h = 0
                else:
                    E_o_h = 32.3
                    a_h = 19.4
        else:
            if self.slope == 'flat':
                if self.heavy_speed < 65:
                    E_o_h = 36
                    a_h = 3.9
                else:
                    E_o_h = 16.7
                    a_h = 41.7
            if self.slope == 'up':
                if self.heavy_speed < 65:
                    E_o_h = 41
                    a_h = 0
                else:
                    E_o_h = 27.9
                    a_h = 25.7
            if self.slope == 'down':
                if self.heavy_speed < 51:
                    E_o_h = 47.0
                    a_h = -10.3
                elif self.heavy_speed >= 51 and self.heavy_speed < 70:
                    E_o_h = 42.8
                    a_h = 0
                else:
                    E_o_h = 32.3
                    a_h = 19.4

        # surface correction
        if self.surface == 'smooth':
            surface_correction_l = 0
            surface_correction_h = 0
        elif self.surface == 'stones':
            surface_correction_l = 3
            surface_correction_h = 3
        elif self.surface == 'cement' or self.surface == 'corrugated':
            surface_correction_l = 2
            surface_correction_h = 2
        elif self.surface == 'porous':
            if self.light_speed <= 60:
                surface_correction_l = -1
            elif self.light_speed > 60 or self.light_speed <= 80:
                surface_correction_l = -2
            else:
                surface_correction_l = -3
            if self.heavy_speed <= 60:
                surface_correction_h = -1
            elif self.heavy_speed > 60 or self.heavy_speed <= 80:
                surface_correction_h = -2
            else:
                surface_correction_h = -3

        v_o = 20.0
        if self.light_number > 0 and self.light_number != None and self.light_speed > 0 and self.light_speed != None:
            power_l = E_o_l + a_l*log10(self.light_speed/v_o) + 10*log10(self.light_number) + surface_correction_l
            power_l_lin = 10**(power_l/10)
        else:
            power_l = 0
            power_l_lin = 0
        if self.heavy_number > 0 and self.heavy_number != None and self.heavy_speed > 0 and self.heavy_speed != None:
            power_h = E_o_h + a_h*log10(self.heavy_speed/v_o) + 10*log10(self.heavy_number) + surface_correction_h
            power_h_lin = 10**(power_h/10)
        else:
            power_h = 0
            power_h_lin = 0

        if (power_l_lin + power_h_lin) > 0:
            power = 10*log10(power_l_lin + power_h_lin)
        else:
            power = 0

        return power

#
#
#prova = {}
#
#prova['l_n'] = 1233
#prova['l_s'] = 39
#prova['h_n'] = 40
#prova['h_s'] = 34
#
#
#prova['type'] = 'continuous'
#prova['slope'] = 'flat'
#prova['surface'] = 'smooth'
#
#print NMPB(prova).bands()
#print NMPB(prova).overall()
