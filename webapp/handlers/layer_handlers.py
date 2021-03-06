import tornado.web
import json, httplib, urllib2, glob, os, sys
from Settings import ROOT, DATA_PATH
from subprocess import call

from safe.api import read_layer

'''This is the handler for the API call that returns the json metadata of exposure layers 
'''
class ExposureLayerHandler(tornado.web.RequestHandler):
    def get(self):
        filename = self.get_argument("filename")
        output = filename[:-4]
        output = output + '.json'
        try:
            call(['ogr2ogr', '-f', 'GeoJSON', output, filename])
            data = open(output)
            f = data.read()
            self.set_header("Content-Type", "application/json")
            self.write(f)
            data.close()
        except:
            raise HTTPError(500)
            
'''This is the handler for the API call that returns the json metadata of hazard layers 
'''
class HazardLayerHandler(tornado.web.RequestHandler):
    def get(self):
        filename = self.get_argument("filename")
        output = filename[:-4]
        output = output + '.json'
        try:
            call(['ogr2ogr', '-f', 'GeoJSON', output, filename])
            data = open(output)
            f = data.read()
            self.set_header("Content-Type", "application/json")
            self.write(f)
            data.close()
        except:
            raise HTTPError(500)