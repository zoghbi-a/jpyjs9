"""
JS9 wrapper to be used in Jupyter/IPython notebooks.
Some of the ideas were adopted from jjs9 (https://github.com/mgckind/jjs9)
"""
import logging

from pyjs9 import JS9 as JS9_ 
import weakref
import uuid
import ipywidgets as ipw
from sidecar import Sidecar
from jupyter_server import serverapp


class JS9Manager:
    """Manage multiple instances of JS9"""

    def __init__(self):
        self.instances = weakref.WeakValueDictionary()

    def get_JS9(self, side=False, app_url=None, id=None, width=600, height=700,
                host=None, multi=False, pageid=None, maxtries=5, delay=2, debug=False):
        """Return JS9 instance if cached, or a new one"""
        if id is not None and id in self.instances:
            return self.instances[id]
        else:
            new_js9 = JS9(side, app_url, id, width, height, host, multi, 
                          pageid, maxtries, delay, debug)
            self.instances[new_js9.jid] = new_js9
            return new_js9
        

class JS9(JS9_):
    
    def __init__(self, side=False, app_url=None, id=None, socketio_path='socket.io',
                 width=600, height=700, host=None, multi=False, pageid=None,
                 maxtries=5, delay=2, debug=False):
        """Start or connect to an instance of JS9

        Parameters:
        -----------
        side: Default is False, Set True to start in a side windown in jupyter
        app_url: '/js9', the url to the js9 app inside jupyterlab
        id: 'JS9',
        socketio_path: socketio path for commuinating with the Helper
        width: 600, width of the window
        height: 600
        host: Helper host; default='http://localhost:2718',
        multi: False,
        pageid: None,
        maxtries: 5,
        delay: 1,
        debug: False,
        """
        # append the main docstring from parent
        JS9.__init__.__doc__ += JS9_.__init__.__doc__

        if id is None:
            id = 'JS9-' + f'{uuid.uuid4()}'[:4]
        self.jid = id
        
        if host is None:
            host = 'http://localhost:2718'

        if debug:
            logger = logging.getLogger()
            logger.setLevel(logging.DEBUG)

        if app_url is None:
            base_url = '/'
            for server in serverapp.list_running_servers():
                base_url = server['base_url']
                break
            app_url = base_url + 'js9'
        self.app_url = app_url
        logging.debug(f'Using app_url: {app_url}')
        
            
        # attach the JS9 window
        html = f"<iframe src='{app_url}/{id}' width={width} height={height}></iframe>"
        self.ipw_obj = ipw.widgets.HTML(value = html)
        self.display(side, width, height)

        # initialize the parent JS9 class, first remove our added keys
        logging.debug(f'Initializing pyjs9.JS9 for id: {id}')
        super(JS9, self).__init__(host=host, id=id, socketio_path=socketio_path,
                                  multi=multi, pageid=pageid, 
                                  maxtries=maxtries, delay=delay, debug=debug)

    
    def display(self, side=False, width=600, height=700):
        """Display widget"""
        self.sc = None
        if side:
            # open a side window 
            layout = ipw.Layout(width=f'{width}px', height=f'{height}px')
            self.sc = Sidecar(title=f'{self.jid}', layout=layout)
            with self.sc:
                display(self.ipw_obj)
        else:
            display(self.ipw_obj)
            
            
    def close(self):
        # close the display as well as the js9 connection
        self.ipw_obj.close()
        if self.sc is not None:
            self.sc.close()
        super(JS9, self).close()
