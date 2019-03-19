import urllib
from rdflib.plugins.sparql.results import csvresults
import io


# given endpoint and query, get and wrap the result in CSV
def query_resulted_in_csv(endpoint, query):
    values = urllib.parse.urlencode({'query': query}).encode("utf-8")
    headers = {
        'Accept': 'text/csv'
    }

    request = urllib.request.Request(endpoint, data=values, headers=headers)
    response_body = urllib.request.urlopen(request).read()

    # print(response_body)

    f = io.BytesIO(response_body)

    csv_parser = csvresults.CSVResultParser()
    results = csv_parser.parse(f)
    return results


# given endpoint and query, update the knowledge base
def query_update(endpoint, query):
    values = urllib.parse.urlencode({'update': query}).encode("utf-8")
    headers = {
        'Content_Type': 'application/x-www-form-urlencoded'
    }
    request = urllib.request.Request(endpoint, data=values, headers=headers)
    urllib.request.urlopen(request).read()


default_point_style = {
				'radius': 2,
				'fillColor': "#ff7800",
				'color': "#000",
				'weight': 1,
				'opacity': 1,
				'fillOpacity': 0.8
			}


default_line_style = {
        'color': "#008000",
        'weight': 5,
        'opacity': 1}

# the endpoint URL
server = 'http://localhost:8081/rdf4j-server/repositories/cycling'
