# SPDX-FileCopyrightText: 2022-present Abdu Zoghbi <a.zoghbi@nasa.gov>
#
# SPDX-License-Identifier: MIT

__version__ = '0.1'


from .handler import _jupyter_server_extension_paths
from .js9 import JS9


## ----------------------------------------- ##
## Add a JS9 icon to the jupyterlab launcher ##
"""
This is the main js9 web server.
js9_web_server is called by jupyter_serverproxy_servers
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


## ------------------------------------------ ##
## Add a proxy entry that for js9 server-side ##
"""
Server side helpers to support external communication with JS9 
(via the shell and Python) and handle the display of large files.
See: https://js9.si.edu/js9/help/helper.html
js9_helper_server is called by jupyter_serverproxy_servers
as an entry point
"""
def js9_helper_server():
    return {
        'command': ['bash', '-c', 'node /opt/js9-web/js9Helper.js'],
        'port': 2718,
        'launcher_entry': {
           'enabled': False,
        }
    }
## ------------------------------------------ ##
