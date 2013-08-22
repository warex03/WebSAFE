import tornado.web
import json, httplib
from safe.api import read_layer

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render(
			"index.html",
		)
        
class CalculateHandler(tornado.web.RequestHandler):
	def get(self):
		self.render(
			"calculate.html",
		)
        
class KMLHandler(tornado.web.RequestHandler):
    def get(self):
        conn = httplib.HTTPConnection("mahar.pscigrid.gov.ph")
        conn.request("GET", "/static/kmz/rain-forecast.KML")
        res = conn.getresponse()
        data = res.read()
        conn.close()
        self.content_type = 'soap/xml'
        self.write(data)