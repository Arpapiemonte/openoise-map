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

#from PyQt4.QtGui import *
from qgis.PyQt.QtGui import QColor
from qgis.core import  (QgsGraduatedSymbolRenderer,
                        QgsSymbol,
                        QgsRendererRange)
from qgis.utils import iface



def render(layer,field):

    myTargetField = field
    myRangeList = []
    myOpacity = 1

    # symbol
    mySymbol = QgsSymbol.defaultSymbol(layer.geometryType())
    mySymbol.setColor(QColor('#D8D8D8'))
    mySymbol.setAlpha(myOpacity)
    myRange = QgsRendererRange(-150.0,0.0,mySymbol,"No level")
    myRangeList.append(myRange)
    # symbol
    mySymbol = QgsSymbol.defaultSymbol(layer.geometryType())
    mySymbol.setColor(QColor('#FFFFFF'))
    mySymbol.setAlpha(myOpacity)
    myRange = QgsRendererRange(0.1,34.4,mySymbol,"< 35 dB(A)")
    myRangeList.append(myRange)    
    # symbol
    mySymbol = QgsSymbol.defaultSymbol(layer.geometryType())
    mySymbol.setColor(QColor('#238443'))
    mySymbol.setAlpha(myOpacity)
    myRange = QgsRendererRange(34.5,39.4,mySymbol,"35 - 39 dB(A)")
    myRangeList.append(myRange)
    # symbol
    mySymbol = QgsSymbol.defaultSymbol(layer.geometryType())
    mySymbol.setColor(QColor('#78C679'))
    mySymbol.setAlpha(myOpacity)
    myRange = QgsRendererRange(39.5,44.4,mySymbol,"40 - 44 dB(A)")
    myRangeList.append(myRange)
    # symbol
    mySymbol = QgsSymbol.defaultSymbol(layer.geometryType())
    mySymbol.setColor(QColor('#C2E699'))
    mySymbol.setAlpha(myOpacity)
    myRange = QgsRendererRange(44.5,49.4,mySymbol,"45 - 49 dB(A)")
    myRangeList.append(myRange)
    # symbol
    mySymbol = QgsSymbol.defaultSymbol(layer.geometryType())
    mySymbol.setColor(QColor('#FFFFB2'))
    mySymbol.setAlpha(myOpacity)
    myRange = QgsRendererRange(49.5,54.4,mySymbol,"50 - 54 dB(A)")
    myRangeList.append(myRange)
    # symbol
    mySymbol = QgsSymbol.defaultSymbol(layer.geometryType())
    mySymbol.setColor(QColor('#FECC5C'))
    mySymbol.setAlpha(myOpacity)
    myRange = QgsRendererRange(54.5,59.4,mySymbol,"55 - 59 dB(A)")
    myRangeList.append(myRange)
    # symbol
    mySymbol = QgsSymbol.defaultSymbol(layer.geometryType())
    mySymbol.setColor(QColor('#FD8D3C'))
    mySymbol.setAlpha(myOpacity)
    myRange = QgsRendererRange(59.5,64.4,mySymbol,"60 - 64 dB(A)")
    myRangeList.append(myRange)
    # symbol
    mySymbol = QgsSymbol.defaultSymbol(layer.geometryType())
    mySymbol.setColor(QColor('#FF0909'))
    mySymbol.setAlpha(myOpacity)
    myRange = QgsRendererRange(64.5,69.4,mySymbol,"65 - 69 dB(A)")
    myRangeList.append(myRange)
    # symbol
    mySymbol = QgsSymbol.defaultSymbol(layer.geometryType())
    mySymbol.setColor(QColor('#B30622'))
    mySymbol.setAlpha(myOpacity)
    myRange = QgsRendererRange(69.5,74.4,mySymbol,"70 - 74 dB(A)")
    myRangeList.append(myRange)
    # symbol
    mySymbol = QgsSymbol.defaultSymbol(layer.geometryType())
    mySymbol.setColor(QColor('#67033B'))
    mySymbol.setAlpha(myOpacity)
    myRange = QgsRendererRange(74.5,79.4,mySymbol,"75 - 79 dB(A)")
    myRangeList.append(myRange)
    # symbol
    mySymbol = QgsSymbol.defaultSymbol(layer.geometryType())
    mySymbol.setColor(QColor('#1C0054'))
    mySymbol.setAlpha(myOpacity)
    myRange = QgsRendererRange(79.5,150.0,mySymbol,">= 80 dB(A)")
    myRangeList.append(myRange)
    
    myRenderer = QgsGraduatedSymbolRenderer('', myRangeList)
    myRenderer.setMode(QgsGraduatedSymbolRenderer.EqualInterval)
    myRenderer.setClassAttribute(myTargetField)
    
    layer.setRenderer(myRenderer)
    iface.legendInterface().refreshLayerSymbology(layer)
    #layer.reload()
    #iface.mapCanvas().refresh()
    layer.triggerRepaint()

                        
def render_old(layer,field):

    myTargetField = field
    myRangeList = []
    myOpacity = 1
    # symbol
    mySymbol = QgsSymbol.defaultSymbol(layer.geometryType())
    mySymbol.setColor(QColor('#FFFFFF'))
    mySymbol.setAlpha(myOpacity)
    myRange = QgsRendererRange(-150.0,0.0,mySymbol,"No level")
    myRangeList.append(myRange)
    # symbol
    mySymbol = QgsSymbol.defaultSymbol(layer.geometryType())
    mySymbol.setColor(QColor('#C0FFC0'))
    mySymbol.setAlpha(myOpacity)
    myRange = QgsRendererRange(0.1,34.9,mySymbol,"< 35 dB(A)")
    myRangeList.append(myRange)
    # symbol
    mySymbol = QgsSymbol.defaultSymbol(layer.geometryType())
    mySymbol.setColor(QColor('#00CC00'))
    mySymbol.setAlpha(myOpacity)
    myRange = QgsRendererRange(35.0,39.9,mySymbol,"35 - 40 dB(A)")
    myRangeList.append(myRange)
    # symbol
    mySymbol = QgsSymbol.defaultSymbol(layer.geometryType())
    mySymbol.setColor(QColor('#005000'))
    mySymbol.setAlpha(myOpacity)
    myRange = QgsRendererRange(40.0,44.9,mySymbol,"40 - 45 dB(A)")
    myRangeList.append(myRange)
    # symbol
    mySymbol = QgsSymbol.defaultSymbol(layer.geometryType())
    mySymbol.setColor(QColor('#FFFF00'))
    mySymbol.setAlpha(myOpacity)
    myRange = QgsRendererRange(45.0,49.9,mySymbol,"45 - 50 dB(A)")
    myRangeList.append(myRange)
    # symbol
    mySymbol = QgsSymbol.defaultSymbol(layer.geometryType())
    mySymbol.setColor(QColor('#FFC74A'))
    mySymbol.setAlpha(myOpacity)
    myRange = QgsRendererRange(50.0,54.9,mySymbol,"50 - 55 dB(A)")
    myRangeList.append(myRange)
    # symbol
    mySymbol = QgsSymbol.defaultSymbol(layer.geometryType())
    mySymbol.setColor(QColor('#FF6600'))
    mySymbol.setAlpha(myOpacity)
    myRange = QgsRendererRange(55.0,59.9,mySymbol,"55 - 60 dB(A)")
    myRangeList.append(myRange)
    # symbol
    mySymbol = QgsSymbol.defaultSymbol(layer.geometryType())
    mySymbol.setColor(QColor('#FF3333'))
    mySymbol.setAlpha(myOpacity)
    myRange = QgsRendererRange(60.0,64.9,mySymbol,"60 - 65 dB(A)")
    myRangeList.append(myRange)
    # symbol
    mySymbol = QgsSymbol.defaultSymbol(layer.geometryType())
    mySymbol.setColor(QColor('#990033'))
    mySymbol.setAlpha(myOpacity)
    myRange = QgsRendererRange(65.0,69.9,mySymbol,"65 - 70 dB(A)")
    myRangeList.append(myRange)
    # symbol
    mySymbol = QgsSymbol.defaultSymbol(layer.geometryType())
    mySymbol.setColor(QColor('#AD9AD6'))
    mySymbol.setAlpha(myOpacity)
    myRange = QgsRendererRange(70.0,74.9,mySymbol,"70 - 75 dB(A)")
    myRangeList.append(myRange)
    # symbol
    mySymbol = QgsSymbol.defaultSymbol(layer.geometryType())
    mySymbol.setColor(QColor('#0000FF'))
    mySymbol.setAlpha(myOpacity)
    myRange = QgsRendererRange(75.0,79.9,mySymbol,"75 - 80 dB(A)")
    myRangeList.append(myRange)
    # symbol
    mySymbol = QgsSymbol.defaultSymbol(layer.geometryType())
    mySymbol.setColor(QColor('#000066'))
    mySymbol.setAlpha(myOpacity)
    myRange = QgsRendererRange(80.0,150.0,mySymbol,"> 80 dB(A)")
    myRangeList.append(myRange)
    
    myRenderer = QgsGraduatedSymbolRenderer('', myRangeList)
    myRenderer.setMode(QgsGraduatedSymbolRenderer.EqualInterval)
    myRenderer.setClassAttribute(myTargetField)
    
    layer.setRenderer(myRenderer)
    iface.legendInterface().refreshLayerSymbology(layer)
    #layer.reload()
    #iface.mapCanvas().refresh()
    layer.triggerRepaint()
