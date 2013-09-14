import tornado.web
import json, httplib, urllib2, glob, os, sys
from Settings import ROOT, DATA_PATH
from subprocess import call

from safe.api import read_layer, calculate_impact
from safe.impact_functions.core import requirements_collect, get_doc_string, \
    requirement_check
from safe.impact_functions.inundation.flood_OSM_building_impact \
    import FloodBuildingImpactFunction
    
from weasyprint import HTML, CSS

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render("index.html")
 
class CalculateHandler(tornado.web.RequestHandler):

    def post(self):
        result = None
        purpose = self.get_argument("purpose")
        if "pdf" in purpose:
            html = self.get_argument("html")
            output = os.path.join(DATA_PATH, 'pdf', 'report.pdf')
            data = open(os.path.join(ROOT, 'static', 'css', 'pdf.css'))
            css = data.read()
            data.close()
            HTML(string=html).write_pdf(output, stylesheets=[CSS(string=css)])
            return
        elif "calculate" in purpose:
            encoding = sys.getfilesystemencoding()
            exposure = self.get_argument("exposure")
            exposure_category = self.get_argument("exposure_category")
            exposure_subcategory = self.get_argument("exposure_subcategory")
            
            hazard = self.get_argument("hazard")
            hazard_category = self.get_argument("hazard_category")
            hazard_subcategory = self.get_argument("hazard_subcategory")
            #params = {}
            
            try:
                hazard_layer = read_layer(hazard.encode(encoding))
                exposure_layer = read_layer(exposure.encode(encoding))

                # assign the required keywords for inasafe calculations
                exposure_layer.keywords['category'] = exposure_category
                exposure_layer.keywords['subcategory'] = exposure_subcategory
                hazard_layer.keywords['category'] = hazard_category
                hazard_layer.keywords['subcategory'] = hazard_subcategory
                
                #define a method that determines the correct impact function based on keywords given
                impact_function = FloodBuildingImpactFunction
                #requirements = requirements_collect(impact_function)
                #print requirements
                #requirement_check(params=params, require_str=requirements, verbose=True)
                
                output = os.path.join(DATA_PATH, 'impact', 'impact.json')
                output_style = os.path.join(DATA_PATH, 'impact', 'impact_style.json')
                output_summary = os.path.join(DATA_PATH, 'impact', 'impact_summary.html')
                
                if os.path.exists(output) and os.path.exists(output_style) \
                    and os.path.exists(output_summary):
                        with open(output_summary) as summary:
                            result = summary.read()
                            summary.close()
                else:           
                    impact = calculate_impact(
                        layers=[exposure_layer, hazard_layer],
                        impact_fcn=impact_function
                    )
                
                    #create the style for the impact layer
                    with open(output_style, 'w') as style_json:
                        json.dump(impact.style_info, style_json)
                        style_json.close()
                
                    call(['ogr2ogr', '-f', 'GeoJSON', output, impact.filename])
        
                    #create the impact summary file
                    result = impact.keywords["impact_summary"]
                    with open(output_summary, 'w') as summary:
                        summary.write(result)
                        summary.close()
            except:
                print 'IO Error or something else has occurred!'
                raise
            else:
                self.render("result.html", result=result)
        
    def get(self):
        self.render( "calculate.html", data_path=DATA_PATH)
        
class ImpactJSONHandler(tornado.web.RequestHandler):
    def get(self):
        data = open(os.path.join(DATA_PATH, 'impact', 'impact.json'))
        f = data.read()
        self.set_header("Content-Type", "application/json")
        self.write(f)
        data.close()
        
class ImpactStyleHandler(tornado.web.RequestHandler):
    def get(self):
        data = open(os.path.join(DATA_PATH, 'impact', 'impact_style.json'))
        f = data.read()
        self.set_header("Content-Type", "application/json")
        self.write(f)
        data.close()
        
class ImpactKMLHandler(tornado.web.RequestHandler):
    def get(self):
        data = open(os.path.join(DATA_PATH, 'impact', 'impact.KML'))
        f = data.read()
        self.set_header("Content-Type", "application/xml")
        self.write(f)
        data.close()
        
class ImpactPDFHandler(tornado.web.RequestHandler):
    def get(self):
        data = open(os.path.join(DATA_PATH, 'pdf', 'report.pdf'))
        f = data.read()
        self.set_header("Content-Type", "application/pdf")
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
        