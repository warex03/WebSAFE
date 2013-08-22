import tornado.web
from globals import Globals

class NavbarModule(tornado.web.UIModule):
    def render(self):
        return self.render_string('modules/_navbar.html', 
                                    page_title=Globals.page_title,
                                    links=Globals.links, 
                                    tools=Globals.tools)