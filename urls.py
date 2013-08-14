from handlers.handlers import IndexHandler

import os.path
import tornado.web

handlers = [
    (r"/", IndexHandler),
]

class Application(tornado.web.Application):
	def __init__(self):
		settings = dict(
			template_path=os.path.join(os.path.dirname(__file__), "templates"),
			static_path=os.path.join(os.path.dirname(__file__), "static"),
			debug=True,
		)
		tornado.web.Application.__init__(self, handlers, **settings)