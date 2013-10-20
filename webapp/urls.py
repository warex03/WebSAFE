from handlers.handlers import IndexHandler, CalculateHandler, \
    ImpactJSONHandler, ImpactPDFHandler, ImpactKMLHandler, \
    ImpactStyleHandler, ImpactMapPDFHandler, FileTreeHandler, \
    AngularHandler, TestHandler, ListHandler, DetailHandler
from handlers.layerapi_handlers import LayerHandler
    
from modules import NavbarModule

import os.path
import tornado.web

# This is where we encode the urls with their respective handlers
handlers = [
    (r"/", IndexHandler),
    (r"/calculate", CalculateHandler),
    (r"/layers", LayerHandler),
    (r"/angular", AngularHandler),
    (r"/test", TestHandler),
    (r"/list", ListHandler),
    (r"/detail", DetailHandler),
]

handlers += [
    (r"/impactstyle", ImpactStyleHandler),
    (r"/json", ImpactJSONHandler),
    (r"/mappdf", ImpactMapPDFHandler),
    (r"/pdf", ImpactPDFHandler),
    (r"/kml", ImpactKMLHandler),
    (r"/filetree", FileTreeHandler),
]

class Application(tornado.web.Application):
	def __init__(self):
		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			debug=True,
            ui_modules = {'Navbar': NavbarModule}
		)
		tornado.web.Application.__init__(self, handlers, **settings)