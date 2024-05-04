# SPDX-FileCopyrightText: 2022-present Abdu Zoghbi <a.zoghbi@nasa.gov>
#
# SPDX-License-Identifier: MIT

__version__ = '0.1'

from .app import _jupyter_server_extension_paths, JS9_PATH
from .js9 import JS9, JS9Manager as _manager
js9 = _manager()

__all__ = ['JS9', 'js9']

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
        #'command': ['bash', '-c', f'DEBUG=* node {JS9_PATH}/js9Helper.js'],
        'command': ['bash', '-c', f'node {JS9_PATH}/js9Helper.js'],
        'port': 2718,
        'launcher_entry': {
           'enabled': False,
        }
    }
## ------------------------------------------ ##

## ----------------------------------------- ##
## Add a JS9 icon to the jupyterlab launcher ##
"""
We do it this way so we don't have to write
Jupyterlab extension. There could be a simpler
way to do it
"""
def js9_launcher():
    return {
        'command': [],
        'new_browser_tab': False,
        'launcher_entry': {
            'enabled': True,
            'title': 'JS9',
        }
    }
## ----------------------------------------- ##
