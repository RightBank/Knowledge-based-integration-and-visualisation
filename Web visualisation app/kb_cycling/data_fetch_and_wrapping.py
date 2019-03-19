import matplotlib

from .queries import *
from .utils import *
from osgeo import ogr
from geojson import Feature, FeatureCollection, loads
import geojson


# for fetch the data (including inferred data) for map visualisation
def data_fetch():
    results = query_resulted_in_csv(server, query_geom_symbol)

    feature_symboliser = {}
    symbolisers_geoms = {}

    """parse the queries results"""
    for row in results:
        symboliser_info = ()
        feature_symboliser[str(row.symboliser)] = ()
        query = query_symboliser.substitute(symboliser=str(row.symboliser))
        # print(query)
        results_symbolisers = query_resulted_in_csv(server, query)
        # print(list(results_symbolisers)[0][0])
        for row1 in results_symbolisers:
            # print(str(row1.h), str(row1.s), str(row1.v), str(row1.stroke_width), str(row1.size))
            symboliser_info = (float(str(row1.h)), float(str(row1.s)), float(str(row1.v)),
                               str(row1.stroke_width), str(row1.size))
        if symboliser_info not in symbolisers_geoms.keys():
            symbolisers_geoms[symboliser_info] = {}
        symbolisers_geoms[symboliser_info][str(row.feature)] = str(row.featureWKT)

    # print(symbolisers_geoms)

    symbolisers_dict = {}
    featurecollection_list = []

    for key in symbolisers_geoms.keys():
        symboliser_type = ''
        """This part maps symboliser info to JS Leaflft style"""

        rgb_decimal = matplotlib.colors.hsv_to_rgb([key[0] / 360, key[1], key[2]])
        color_hex = matplotlib.colors.to_hex(rgb_decimal)

        # print(color_hex)
        if key[3] != 'None':
            symboliser_type = 'https://www.gis.lu.se/ont/data_portrayal/symboliser#LineSymboliser'
            new_key = default_line_style
            new_key['color'] = color_hex
            new_key['weight'] = key[3]

        if key[4] != 'None':
            symboliser_type = 'https://www.gis.lu.se/ont/data_portrayal/symboliser#PointSymboliser'
            new_key = default_point_style
            new_key['fillColor'] = color_hex
            new_key['radius'] = int(key[4])

        symbolisers_dict[key] = new_key

        """This part is GeoJSON conversion"""

        feature_list = []
        for feature_key in symbolisers_geoms[key].keys():
            geom = ogr.CreateGeometryFromWkt(symbolisers_geoms[key][feature_key])
            geom_geojson = loads(geom.ExportToJson())
            feature_geojson = Feature(geometry=geom_geojson, properties={"URI": feature_key})
            feature_list.append(feature_geojson)

        feature_collection = FeatureCollection(feature_list)

        feature_collection['style'] = symbolisers_dict[key]

        feature_collection['symboliser_type'] = symboliser_type
        # print(feature_collection)
        # feature_collection = geojson.loads(dump)

        featurecollection_list.append(geojson.dumps(feature_collection))
    return featurecollection_list


# get legend information for map
def legend_info_fetch():

    legend_info = query_resulted_in_csv(server, query_legend)
    legend_info_list = []
    for row in legend_info:
        # print(row)
        h = float(row.h)
        s = float(row.s)
        v = float(row.v)
        rgb_decimal = matplotlib.colors.hsv_to_rgb([h / 360, s, v])
        color_hex = matplotlib.colors.to_hex(rgb_decimal)

        legend_info_list.append((str(row.label), str(color_hex)))

    return legend_info_list







