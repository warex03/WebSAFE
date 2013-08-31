import tornado.web
import json, httplib, urllib2

from safe.api import read_layer, calculate_impact
from safe.impact_functions.inundation.flood_OSM_building_impact \
    import FloodBuildingImpactFunction
from subprocess import call

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render( "index.html")
 
class CalculateHandler(tornado.web.RequestHandler):
        
    def post(self):
        #exposure = self.get_argument("exposure", "No Exposure sent!")
        hazard = read_layer("/vagrant/webapp/data/flood.shp")
        exposure = read_layer("/vagrant/webapp/data/buildings.shp")
        #hazard = self.get_argument("hazard", "No Hazard sent!")
        impact_function = FloodBuildingImpactFunction

        # assign the required keywords for inasafe calculations
        exposure.keywords['category'] = 'exposure'
        exposure.keywords['subcategory'] = 'structure'
        hazard.keywords['category'] = 'hazard'
        hazard.keywords['subcategory'] = 'flood'
    
        # run analisys
        impact = calculate_impact(
            layers=[exposure, hazard],
            impact_fcn=impact_function
        )
        #filename = glob.glob('*.shp')[0]
        #layer_file = str(os.path.join(layer_path, filename))
        #hazard = read_layer(hazard_filename)
        result = impact.keywords["impact_summary"]
        self.render("result.html", result=result)
        
    def get(self):
		self.render( "calculate.html")

class KMLHandler(tornado.web.RequestHandler):
    def get(self):
        conn = httplib.HTTPConnection("mahar.pscigrid.gov.ph")
        conn.request("GET", "/static/kmz/rain-forecast.KML")
        res = conn.getresponse()
        data = res.read()
        conn.close()
        self.content_type = 'soap/xml'
        self.write(data)