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
    
        try:
            # run analisys
            impact = calculate_impact(
                layers=[exposure, hazard],
                impact_fcn=impact_function
            )
            output_style = '/vagrant/webapp/data/impact' + '_style.json'
            with open(output_style, 'w') as style_json:
                json.dump(impact.style_info, style_json)
            output = '/vagrant/webapp/data/impact.json'
            #call(['ogr2ogr', '-f', 'KML', output, impact.filename])
            #call(['ogr2ogr', '-f', 'KML', output, '/vagrant/webapp/data/impact.shp'])
            call(['ogr2ogr', '-f', 'GeoJSON', output, '/vagrant/webapp/data/impact.shp'])
        
            result = impact.keywords["impact_summary"]
        except:
            raise
        else:
            self.render("result.html", result=result)
        
    def get(self):
		self.render( "calculate.html")
        
class ImpactKMLHandler(tornado.web.RequestHandler):
    def get(self):
        data = open('/vagrant/webapp/data/impact.KML')
        f = data.read()
        self.content_type = 'soap/xml'
        self.write(f)
        data.close()
        
class ImpactJSONHandler(tornado.web.RequestHandler):
    def get(self):
        data = open('/vagrant/webapp/data/impact.json')
        f = data.read()
        self.content_type = 'application/json'
        self.write(f)
        data.close()
        
class ImpactStyleHandler(tornado.web.RequestHandler):
    def get(self):
        data = open('/vagrant/webapp/data/impact_style.json')
        f = data.read()
        self.content_type = 'application/json'
        self.write(f)
        data.close()
        
class ImpactPDFHandler(tornado.web.RequestHandler):
    def get(self):
        data = open('/vagrant/webapp/data/impact.pdf')
        f = data.read()
        self.content_type = 'application/pdf'
        self.write(f)
        data.close()
        