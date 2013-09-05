import tornado.web
import json, httplib, urllib2, glob, os
from Settings import ROOT, DATA_PATH
from subprocess import call

from safe.api import read_layer, calculate_impact
from safe.impact_functions.inundation.flood_OSM_building_impact \
    import FloodBuildingImpactFunction

#from utilities import setupPrinter

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render( "index.html")
 
class CalculateHandler(tornado.web.RequestHandler):
        
    def post(self):
        purpose = self.get_argument("purpose", "None")
        if "pdf" in purpose:
            print purpose
            #setupPrinter("/vagrant/webapp/data/impact.pdf")
        elif "calculate" in purpose:
            print purpose
            #exposure = self.get_argument("exposure", "No Exposure sent!")
            #hazard = self.get_argument("hazard", "No Hazard sent!")
            
        hazard_filename = os.path.join(DATA_PATH, 'hazard', 'flood.shp')
        exposure_filename = os.path.join(DATA_PATH, 'exposure', 'buildings.shp')
        hazard = read_layer(hazard_filename)
        exposure = read_layer(exposure_filename)
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
            output_style = os.path.join(DATA_PATH, 'impact', 'impact_style.json')
            print output_style
            with open(output_style, 'w') as style_json:
                json.dump(impact.style_info, style_json)
            output = os.path.join(DATA_PATH, 'impact', 'impact.json')
            #call(['ogr2ogr', '-f', 'KML', output, impact.filename])
            #call(['ogr2ogr', '-f', 'KML', output, '/vagrant/webapp/data/impact.shp'])
            
            #call(['ogr2ogr', '-f', 'GeoJSON', output, impact.filename])
            call(['ogr2ogr', '-f', 'GeoJSON', output, os.path.join(DATA_PATH, 'test', 'impact.shp')])
        
            result = impact.keywords["impact_summary"]
        except:
            raise
        else:
            self.render("result.html", result=result)
        
    def get(self):
        try:
            exposure_path = os.path.join(DATA_PATH, 'exposure')
            os.chdir(exposure_path)
            exposure_data = glob.glob('*.shp')
            
            hazard_path = os.path.join(DATA_PATH, 'hazard')
            os.chdir(hazard_path)
            hazard_data = glob.glob('*.shp')
        except:
            raise
        else:
            self.render( "calculate.html", data_path=DATA_PATH)
        
class ImpactKMLHandler(tornado.web.RequestHandler):
    def get(self):
        data = open('/vagrant/webapp/data/impact/impact.KML')
        f = data.read()
        self.content_type = 'soap/xml'
        self.write(f)
        data.close()
        
class ImpactJSONHandler(tornado.web.RequestHandler):
    def get(self):
        data = open('/vagrant/webapp/data/impact/impact.json')
        f = data.read()
        self.content_type = 'application/json'
        self.write(f)
        data.close()
        
class ImpactStyleHandler(tornado.web.RequestHandler):
    def get(self):
        data = open('/vagrant/webapp/data/impact/impact_style.json')
        f = data.read()
        self.content_type = 'application/json'
        self.write(f)
        data.close()
        
class ImpactPDFHandler(tornado.web.RequestHandler):
    def get(self):
        data = open('/vagrant/webapp/data/pdf/impact.pdf')
        f = data.read()
        self.content_type = 'application/pdf'
        self.write(f)
        data.close()
        
class FileTreeHandler(tornado.web.RequestHandler):
    def post(self):
        to_return = ['<ul class="jqueryFileTree" style="display: none;">']
        try:
            dir = self.get_argument("dir", DATA_PATH)
            for f in os.listdir(dir):
                ff=os.path.join(dir,f)
                if os.path.isdir(ff) and "exposure" in ff:
                    to_return.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (ff,f))
                    
                elif os.path.isdir(ff) and "hazard" in ff:
                    to_return.append('<li class="directory collapsed"><a href="#" rel="%s/">%s</a></li>' % (ff,f))
                    
                else:
                    if not os.path.isdir(ff):
                        ext=os.path.splitext(f)[1][1:] # get .ext and remove dot
                        if "shp" in ext:
                            to_return.append('<li class="file ext_%s"><a href="#" rel="%s">%s</a></li>' % (ext,ff,f))
        except Exception,e:
            raise e
            #to_return.append('Could not load directory: %s' % str(e))
            
        to_return.append('</ul>')
        self.write(''.join(to_return))
        