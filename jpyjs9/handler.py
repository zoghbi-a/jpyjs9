
from jupyter_server.extension.application import ExtensionApp, ExtensionAppJinjaMixin
from jupyter_server.base.handlers import JupyterHandler, AuthenticatedFileHandler
from tornado import web
from jupyter_server.extension.handler import (
    ExtensionHandlerJinjaMixin,
    ExtensionHandlerMixin,
)


## ---------------------------------------- ##
## A handler to capture a js9 parameter and ##
## pass it to the template html page
class Js9Handler(ExtensionHandlerJinjaMixin, ExtensionHandlerMixin, JupyterHandler):
    @web.authenticated
    def get(self, jid='JS9'):
        self.write(self.render_template("index.html", jid=jid))
## ---------------------------------------- ##


## -------------------------------------------- ##
## Jupyter server app to handle /js9 and /js9/* ##
class Js9App(ExtensionAppJinjaMixin, ExtensionApp):
    """An extension to /js9 handler to jupyter lab"""
    name = "js9"
    extension_url = "/js9"
    load_other_extensions = True
    js9web = '/opt/js9-web/'
    static_paths = [js9web]
    template_paths = [js9web]

    def initialize_handlers(self):
        self.handlers.extend([
            # serve JS9 and static files under /js9/
            (rf"/{self.name}/?([0-9a-zA-Z]+)?$", Js9Handler),
            (rf"/{self.name}/(.*)", AuthenticatedFileHandler, {"path": self.static_paths[0]}),
        ])
## -------------------------------------------- ##


## ---------------------------- ##
## Enable the js9App by default ##
def _jupyter_server_extension_paths():
    return [{
        'module': 'jpyjs9',
        'app': Js9App
    }]
## ---------------------------- ##