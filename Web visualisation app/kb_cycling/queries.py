from string import Template


query_geom_symbol = '''
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
PREFIX net: <http://inspire.ec.europa.eu/ont/net#>
SELECT ?feature ?featureWKT ?symboliser
WHERE { ?feature a geo:Feature.
        net:network_detailed net:Network.elements ?feature.
        ?feature geo:hasDefaultGeometry [
                geo:asWKT ?featureWKT]. 
                ?feature <https://gis.lu.se/ont/data_portrayal/symboliser#isSymbolisedBy> ?symboliser.
    }
'''

query_symboliser = Template('''
PREFIX geo: <http://www.opengis.net/ont/geosparql#>
PREFIX net: <http://inspire.ec.europa.eu/ont/net#>
PREFIX graphic: <https://gis.lu.se/ont/data_portrayal/graphic#>
PREFIX symboliser: <https://gis.lu.se/ont/data_portrayal/symboliser#>
PREFIX carto: <https://gis.lu.se/ont/carto#>
SELECT *         
WHERE { OPTIONAL {<$symboliser> a symboliser:LineSymboliser;
      						graphic:strokeWidth ?stroke_width;
      						graphic:strokeColour [
      						carto:hueInHSV ?h;
        					carto:saturationInHSV ?s;
        					carto:valueInHSV ?v].}
        	OPTIONAL {<$symboliser> a symboliser:PointSymboliser;
      						graphic:size ?size;
      						graphic:hasFillColor [
      						carto:hueInHSV ?h;
        					carto:saturationInHSV ?s;
        					carto:valueInHSV ?v].}
  }''')

query_update_context = Template('''
DELETE {
?context <https://gis.lu.se/ont/visualisation_context#representsPhenomenon> ?phenomenon.
}
INSERT {
?context <https://gis.lu.se/ont/visualisation_context#representsPhenomenon> <$phenomenon>.
}
WHERE {
?context a <https://gis.lu.se/ont/visualisation_context#VisualisationContext>;
    <https://gis.lu.se/ont/visualisation_context#representsPhenomenon> ?phenomenon;
    <https://gis.lu.se/ont/visualisation_context#hasScaleValueDenominator> ?scale.    
}
''')


query_context = '''
SELECT ?phenomenon
WHERE {
?context a <https://gis.lu.se/ont/visualisation_context#VisualisationContext>;
    <https://gis.lu.se/ont/visualisation_context#representsPhenomenon> ?phenomenon;
    <https://gis.lu.se/ont/visualisation_context#hasScaleValueDenominator> ?scale.    
}
'''

query_legend = '''
PREFIX carto: <https://gis.lu.se/ont/carto#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?thematic_value ?label ?h ?s ?v
WHERE {
	?colour a carto:Colour;
    		carto:colourCorrespondsToThematicValue ?thematic_value;
    		carto:hueInHSV ?h;
        	carto:saturationInHSV ?s;
        	carto:valueInHSV ?v.
  	?context a <https://gis.lu.se/ont/visualisation_context#VisualisationContext>;
    	<https://gis.lu.se/ont/visualisation_context#representsPhenomenon> ?phenomenon.
  	?thematic_value a ?phenomenon;
    		rdfs:label ?label;
    		carto:thematicValueOrder ?order.
}
order by ?order
'''