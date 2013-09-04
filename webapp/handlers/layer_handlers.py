import tornado.web
import json, httplib, urllib2, glob, os, sys
from Settings import ROOT, DATA_PATH
from subprocess import call

from safe.api import read_layer

class LayerHandler(tornado.web.RequestHandler): 
    def post(self):
        layer_type = self.get_argument("layer_type", "None")
        filename = self.get_argument("filename", "None")
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