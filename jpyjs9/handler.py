
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
        self.write(self.render_template("js9.html", jid=jid))
## ---------------------------------------- ##
