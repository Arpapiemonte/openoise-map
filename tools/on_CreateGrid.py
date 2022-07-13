import os
from PyQt5.QtCore import QVariant
from PyQt5.QtGui import QColor
from qgis.core import (
    Qgis,
    QgsProject,
    QgsVectorLayer,
    QgsFeature,
    QgsField,
    QgsFields,
    QgsRasterLayer,
    QgsWkbTypes,
QgsProcessingFeedback,
    QgsVectorFileWriter,
QgsRasterBandStats,
QgsColorRampShader,
QgsRasterShader,
QgsSingleBandPseudoColorRenderer,
QgsVectorDataProvider
)

from qgis.utils import iface
from qgis import processing


def createGrid(resolution, grid_path, extent,BarGridReceiver):

    # feedback configuration
    feedback = QgsProcessingFeedback()
    feedback.progressChanged.connect(BarGridReceiver.setValue)

    # rename shape output in case already exists
    grid_path = removeLayer(grid_path)

    if not grid_path == 'Error':

        grid_layer_name = os.path.splitext(
            os.path.basename(grid_path))[0]

        grid_layer = QgsVectorLayer(
            grid_path,
            grid_layer_name,
            "ogr")

        crs_layer = QgsProject.instance().crs()

        xmax = extent.xMaximum()
        ymax = extent.yMaximum()
        xmin = extent.xMinimum()
        ymin = extent.yMinimum()
        extent_coords = "%f,%f,%f,%f" % (xmin, xmax, ymin, ymax)

        # native:creategrid
        params_creategrid = {
            'CRS': crs_layer,
            'EXTENT': extent_coords,
            'HOVERLAY': 0,
            'HSPACING': resolution,
            'OUTPUT': 'memory:',
            'TYPE': 0,
            'VOVERLAY': 0,
            'VSPACING': resolution
        }

        result_grid = processing.run("native:creategrid", params_creategrid)
        feedback.setProgress(70)
        grid_output = result_grid['OUTPUT']

        # native:difference
        # params_difference = {
        #     'INPUT': grid_output,
        #     'OUTPUT': 'memory:',
        #     'OVERLAY': overlay_layer
        # }
        #
        # result_difference = processing.run("native:difference", params_difference)
        # difference_output = result_difference['OUTPUT']

        # native:extractbylocation
        # params_extract = {
        #     'INPUT': grid_output,
        #     'INTERSECT': BuildingMaskLayer,
        #     'OUTPUT': 'memory:',
        #     'OVERLAY': BuildingMaskLayer,
        #     'PREDICATE': [2]
        # }

        # result_difference = processing.run("native:extractbylocation", params_extract)
        # feedback.setProgress(85)
        # difference_output = result_difference['OUTPUT']
        difference_output = result_grid['OUTPUT']

        # native:multipart to single partS
        params_multiTosingle = {
            'INPUT': difference_output,
            'OUTPUT': 'memory:',
        }

        result_multiTOsingle = processing.run("native:multiparttosingleparts", params_multiTosingle)
        feedback.setProgress(100)
        output_singlepart = result_multiTOsingle['OUTPUT']

        # remove layer in already in TOC
        # removeLayer(grid_path)
        print(grid_path)
        writer = QgsVectorFileWriter.writeAsVectorFormat(
            output_singlepart,
            grid_path,
            'utf-8',
            driverName='ESRI Shapefile',
            filterExtent=output_singlepart.extent()
        )

        grid_layer = iface.addVectorLayer(
            grid_path,
            '',
            'ogr'
        )
        #
        fieldsTOdelete = grid_layer.attributeList()

        pr = grid_layer.dataProvider()

        pr.deleteAttributes(fieldsTOdelete[1:5])

        grid_layer.updateFields()


def createRasterAndContour(resolution, layerTOrasterize_path, field, interval, contour_path, poly_path, ProgressBarGrid):
    project = QgsProject.instance()

    #feedback configuration
    # feedback = QgsProcessingFeedback()
    # feedback.progressChanged.connect(ProgressBarGrid.setValue)

    layerTOrasterize_name = os.path.splitext(
        os.path.basename(layerTOrasterize_path))[0]

    layerTOrasterize = QgsVectorLayer(
        layerTOrasterize_path,
        layerTOrasterize_name,
        "ogr"
    )

    # routine to detect the resolution raster
    feats_count = layerTOrasterize.featureCount()
    spacings = [5, 10, 20, 30, 40, 50]

    extent = layerTOrasterize.extent()
    xmax = extent.xMaximum()
    ymax = extent.yMaximum()
    xmin = extent.xMinimum()
    ymin = extent.yMinimum()
    extent_coords = "%f,%f,%f,%f" % (xmin, xmax, ymin, ymax)

    area_extent = (xmax-xmin)*(ymax-ymin)
    print(area_extent)
    print(feats_count)
    density_points = area_extent/feats_count
    print(density_points)
    dict_den = dict()
    for space in spacings:
        dict_den[density_points-space**2]=space
    print(dict_den)


    params_rasterize = {
        'BURN': 0,
        'DATA_TYPE': 5,
        'EXTENT': extent_coords,
        'EXTRA': '',
        'FIELD': field,
        'HEIGHT': resolution,
        'INIT': None,
        'INPUT': layerTOrasterize,
        'INVERT': False,
        'NODATA': -99,
        'OPTIONS': '',
        'OUTPUT': 'TEMPORARY_OUTPUT',
        'UNITS': 1,
        'WIDTH': resolution
    }
    result_rasterize = processing.run("gdal:rasterize", params_rasterize,)# feedback=feedback)
    # feedback.setProgress(25)
    ProgressBarGrid.setValue(25)
    raster_output = result_rasterize['OUTPUT']



    '''procedure to fill nodata corresponding to -99 values'''
    params_fillnull = {
        'BAND': 1,
        'DISTANCE': 5000,
        'EXTRA': '',
        'INPUT': raster_output,
        'ITERATIONS': 0,
        'MASK_LAYER': None,
        'NO_MASK': False,
        'OPTIONS': '',
        'OUTPUT': 'TEMPORARY_OUTPUT'}

    result_fillnodata = processing.run("gdal:fillnodata", params_fillnull,)# feedback=feedback)
    # feedback.setProgress(50)
    ProgressBarGrid.setValue(50)
    raster_filled = result_fillnodata['OUTPUT']
    raster_layer_filled = QgsRasterLayer(
        raster_filled,
        'Raster noise distrubution'
    )
    # apply noise color ramp to raster output layer
    stats = raster_layer_filled.dataProvider().bandStatistics(1, QgsRasterBandStats.All)
    fnc = QgsColorRampShader()
    fnc.setColorRampType(QgsColorRampShader.Interpolated)
    lst = [QgsColorRampShader.ColorRampItem(0, QColor(216, 216, 216)),
           QgsColorRampShader.ColorRampItem(35, QColor(216, 216, 216)),
           QgsColorRampShader.ColorRampItem(39, QColor(35, 132, 67)),
           QgsColorRampShader.ColorRampItem(44, QColor(120, 198, 121)),
           QgsColorRampShader.ColorRampItem(49, QColor(194, 230, 153)),
           QgsColorRampShader.ColorRampItem(54, QColor(255, 255, 178)),
           QgsColorRampShader.ColorRampItem(59, QColor(254, 204, 92)),
           QgsColorRampShader.ColorRampItem(64, QColor(253, 141, 60)),
           QgsColorRampShader.ColorRampItem(69, QColor(255, 9, 9)),
           QgsColorRampShader.ColorRampItem(74, QColor(179, 6, 34)),
           QgsColorRampShader.ColorRampItem(79, QColor(103, 3, 59)),
           QgsColorRampShader.ColorRampItem(80, QColor(28, 0, 84)),
           QgsColorRampShader.ColorRampItem(1500, QColor(28, 0, 84))]
    fnc.setColorRampItemList(lst)

    shader = QgsRasterShader()
    shader.setRasterShaderFunction(fnc)

    renderer = QgsSingleBandPseudoColorRenderer(raster_layer_filled.dataProvider(), 1, shader)
    raster_layer_filled.setRenderer(renderer)

    project.addMapLayer(raster_layer_filled)

    '''procedura da sviluppare per rimuovere i valori minore di zero
    { 'CELLSIZE' : 5, 'CRS' : QgsCoordinateReferenceSystem('EPSG:3003'), 
    'EXPRESSION' : '(\"Raster@1\">0)*\"Raster@1\"', 
    'EXTENT' : '1394561.740000000,1394816.740000000,4989600.651000000,4989900.651000000 [EPSG:3003]', 
    'LAYERS' : None, 
    'OUTPUT' : 'TEMPORARY_OUTPUT' }
    '''

    params_contour = {
        'BAND': 1,
        'CREATE_3D': False,
        'EXTRA': '',
        'FIELD_NAME': field,
        'IGNORE_NODATA': False,
        'INPUT': raster_filled,
        'INTERVAL': interval,
        'NODATA': -99,
        'OFFSET': 0,
        'OUTPUT': contour_path
    }

    # remove contour if already in TOC
    contour_path = removeLayer(contour_path)
    if contour_path == 'Error':
        params_contour['OUTPUT'] = 'TEMPORARY_OUTPUT'
    else:
        params_contour['OUTPUT'] = removeLayer(contour_path)

    result_contour = processing.run("gdal:contour", params_contour,)# feedback=feedback)
    # feedback.setProgress(75)
    ProgressBarGrid.setValue(75)
    contour_output = result_contour['OUTPUT']

    contour_name = os.path.splitext(
        os.path.basename(contour_path))[0]

    contour_layer = QgsVectorLayer(
        contour_output,
        contour_name
    )

    project.addMapLayer(contour_layer)

    # gdal: polygonize Contour NEW method
    parameter_poly_contour = {
        'BAND': 1,
        'CREATE_3D': False,
        'EXTRA': '',
        'FIELD_NAME_MAX': field+'_MAX',
        'FIELD_NAME_MIN': field+'_MIN',
        'IGNORE_NODATA': False,
        'INPUT': raster_filled,
        'INTERVAL': interval,
        'NODATA': -99,
        'OFFSET': 0,
        'OUTPUT': poly_path
    }
    # remove polygon in already in TOC
    poly_path = removeLayer(poly_path)
    if poly_path == 'Error':
        parameter_poly_contour['OUTPUT'] = 'TEMPORARY_OUTPUT'
    else:
        parameter_poly_contour['OUTPUT']=removeLayer(poly_path)

    result_poly = processing.run("gdal:contour_polygon", parameter_poly_contour,)#feedback=feedback)
    # feedback.setProgress(100)
    ProgressBarGrid.setValue(100)
    poly_output = result_poly['OUTPUT']

    poly_name = os.path.splitext(
        os.path.basename(poly_path))[0]

    poly_layer = QgsVectorLayer(
        poly_output,
        poly_name
    )

    project.addMapLayer(poly_layer)

    # ADD Area_mq field in table
    # Here we get the capabilities of your layer (Add attribute layer, edit feature ect ..
    caps = poly_layer.dataProvider().capabilities()

    # We make a list of fields from their name
    fields_name = [f.name() for f in poly_layer.fields()]

    # We check if we can add an attribute to the layer.
    if caps & QgsVectorDataProvider.AddAttributes:
        # We check if the attribute field is not exist
        if "Area_mq" not in fields_name:
            # We add the field name Area and with the double type (it can be integer or text
            poly_layer.dataProvider().addAttributes([QgsField("Area_mq", QVariant.Double)])
            # We update layer's field otherwise we'll not have the field
            poly_layer.updateFields()
            # Recreate the list field by the name to have index of the field
            fields_name = [f.name() for f in poly_layer.fields()]
            # we get the index of the Area field
            fareaidx = fields_name.index('Area_mq')
        else:
            # We are here because there is a field name Area
            print("The Area_mq field is already added")
            # Recreate the list field by the name to have index of the field
            fields_name = [f.name() for f in poly_layer.fields()]
            # we get the index of the Area field
            fareaidx = fields_name.index('Area_mq')

    # Here we check if we can change attribute of the layer
    if caps & QgsVectorDataProvider.ChangeAttributeValues:
        # we loop^on every feature
        for feature in poly_layer.getFeatures():
            # For each feature :
            # We calculate the area and put the index of the field Area
            # We round the area value by 2 digit expressed in km2
            attrs = {fareaidx: round(feature.geometry().area(), 2)}
            # We change the the value of Area Field for this feature.
            poly_layer.dataProvider().changeAttributeValues({feature.id(): attrs})

    return raster_output


def removeLayer(path_layer):
    # remove layer from TOC if already loaded
    basefile = os.path.basename(path_layer)
    diff_layer = os.path.splitext(basefile)[0]
    directory = os.path.dirname(path_layer)
    extensions = ["shp", "shx", "dbf", "prj", "sbn", "sbx", "fbn", "fbx", "ain", "aih", "ixs", "mxs", "atx", "xml",
                  "cpg", "qix"]
    output_path=path_layer
    if os.path.exists(path_layer):
        if len(QgsProject.instance().mapLayersByName(diff_layer)) > 0:
            lyr = QgsProject.instance().mapLayersByName(diff_layer)[0]
            print('renaming layer1: ', lyr.id())
            QgsProject.instance().removeMapLayer(lyr.id())
            lyr = None
            del lyr

        if not QgsVectorFileWriter.deleteShapeFile(path_layer):
            iface.messageBar().pushMessage("Ooops", "You have to choose a new shapefile for "+diff_layer+" - Overwrite is not allowed!", level=Qgis.Critical, duration=3)
            return 'Error'


    #     output_path=os.path.join(directory,diff_layer+'1.shp',)
        # QgsProject.instance().removeMapLayer(lyr.id())
        # QgsVectorFileWriter.deleteShapeFile(path_layer)

        # for ext in extensions:
        #     f = os.path.join(directory,diff_layer+'.'+ext)
        #     if os.path.exists(f):
        #         print('removing file: ',f)
        #         os.remove(f)

    return output_path


# def polygonize(raster_path, minimum, maximum, interval, poly_path):
#     project = QgsProject.instance()
#
#     raster_name = os.path.splitext(
#         os.path.basename(raster_path))[0]
#
#     raster = QgsRasterLayer(
#         raster_path,
#         raster_name,
#         "gdal"
#     )
#
#     # native: reclassify by table
#     table = []
#     for i in range(minimum, maximum, interval):
#         i += interval
#         value = (minimum + i) / 2
#         fillTbl = [minimum, i, value]
#         table.extend(fillTbl)
#         minimum += interval
#
#     parameter_reclaBYtbl = {
#         'DATA_TYPE': 5,
#         'INPUT_RASTER': raster,
#         'NODATA_FOR_MISSING': False,
#         'NO_DATA': -9999,
#         'OUTPUT': 'TEMPORARY_OUTPUT',
#         'RANGE_BOUNDARIES': 3,
#         'RASTER_BAND': 1,
#         'TABLE': table
#     }
#
#     result_reclas = processing.run("native:reclassifybytable", parameter_reclaBYtbl)
#     reclas_output = result_reclas['OUTPUT']
#
#     # gdal: polygonize OLD method
#     parameter_poly = {
#         'BAND': 1,
#         'EIGHT_CONNECTEDNESS': False,
#         'EXTRA': '',
#         'FIELD': 'dBA',
#         'INPUT': reclas_output,
#         'OUTPUT': poly_path
#     }
#
#     result_poly = processing.run("gdal:polygonize", parameter_poly)
#     poly_output = result_poly['OUTPUT']
#
#     poly_name = os.path.splitext(
#         os.path.basename(poly_path))[0]
#
#     poly_layer = QgsVectorLayer(
#         poly_path,
#         poly_name
#     )
#
#     project.addMapLayer(poly_layer)