from urls import Application

import tornado.httpserver
import tornado.ioloop
import tornado.options
import os

def main():
	tornado.options.parse_command_line()
	http_server = tornado.httpserver.HTTPServer(Application())
	http_server.listen(os.environ.get("PORT", 8000))
        print os.environ.get("PORT", 8000)
	# start it up
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()