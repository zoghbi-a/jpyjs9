# SPDX-FileCopyrightText: 2022-present Abdu Zoghbi <a.zoghbi@nasa.gov>
#
# SPDX-License-Identifier: MIT

__version__ = '0.1'

from jupyter_server.extension.application import ExtensionApp, ExtensionAppJinjaMixin
from jupyter_server.utils import url_path_join
from jupyter_server.base.handlers import JupyterHandler, AuthenticatedFileHandler
from tornado import web
from jupyter_server.extension.handler import (
    ExtensionHandlerJinjaMixin,
    ExtensionHandlerMixin,
)


## ----------------------------------------- ##
## Add a JS9 icon to the jupyterlab launcher ##
"""
This is the main js9 web server.
js9_main_server is called by jupyter_serverproxy_servers
as an entry point
"""
def js9_web_server():
    return {
        'command': [],
        'launcher_entry': {
            'enabled': True,
            'title': 'JS9',
            'new_browser_tab': False,
        }
    }
## ----------------------------------------- ##



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
    js9web = '/tmp/js9-web/'
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