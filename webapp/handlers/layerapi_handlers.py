import tornado.web
import json, httplib, urllib2, glob, os, sys
from Settings import ROOT, DATA_PATH
from subprocess import call

from safe.api import read_layer

'''This is the handler for the API call that returns the json metadata of a layer 
'''
class LayerHandler(tornado.web.RequestHandler): 
    '''this returns the metadata(keywords) of the layer with the specified filename
    '''
    def post(self):
        layer_type = self.get_argument("layer_type")
        #change this to ID
        filename = self.get_argument("filename")
        encoding = sys.getfilesystemencoding()
        if "hazard" in layer_type:
            layer = read_layer(filename.encode(encoding))
            json_data = layer.keywords
            json_data.update({ "name": layer.name })
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(json_data))
            
        elif "exposure" in layer_type:
            layer = read_layer(filename.encode(encoding))
            json_data = layer.keywords
            json_data.update({ "name": layer.name })
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(json_data))
    
    '''this returns the GeoJson of the layer with the specified filename
    '''
    def get(self):
        filename = self.get_argument("filename")
        output = filename[:-4]
        output = output + '.json'
        self.set_header("Content-Type", "application/json")
        try:
            with open(output) as data:
                f = data.read()
                self.write(f)
                data.close()
        except:
            try:
                call(['ogr2ogr', '-f', 'GeoJSON', output, filename])
                data = open(output)
                f = data.read()
                self.write(f)
                data.close()
            except:
                raise# HTTPError(500)