from handlers.handlers import IndexHandler, CalculateHandler, \
    ImpactKMLHandler, ImpactJSONHandler, ImpactPDFHandler
from modules import NavbarModule

import os.path
import tornado.web

# This is where we encode the urls with their respective handlers
handlers = [
    (r"/", IndexHandler),
    (r"/calculate", CalculateHandler),
    (r"/impact", ImpactKMLHandler),
    (r"/json", ImpactJSONHandler),
    (r"/pdf", ImpactPDFHandler),
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