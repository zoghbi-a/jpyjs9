
"""
JS9 wrapper to be used in Jupyter/IPython notebooks
Adapted from jjs9 by Matias Carrasco Kind
"""

import pyjs9
import ipywidgets as ipw
from sidecar import Sidecar
from six import BytesIO
import base64
from socketIO_client import SocketIO
import json
from io import StringIO
import http
import requests
import socketio
import uuid
from collections import OrderedDict
from collections import defaultdict
import weakref


class KeepRefs(object):
    __refs__ = defaultdict(list)
    def __init__(self):
        self.__refs__[self.__class__].append(weakref.ref(self))

    @classmethod
    def get_instances(cls):
        for inst_ref in cls.__refs__[cls]:
            inst = inst_ref()
            if inst is not None:
                yield inst


class jJS9(pyjs9.JS9, KeepRefs):
    def __init__(self, root='http://localhost', path='/js9', port_html=8888, port_io=2718, transport='socketio', wid=None):
        KeepRefs.__init__(self)
        pyjs9.js9Globals['transport'] = transport
        if wid is None:
            self.wid = str(uuid.uuid4().hex)
        else:
            self.wid = wid
        self.node_url = f'{root}:{port_io}'
        self.frame_url = f'{root}:{port_html}{parth}'
        self.displays = OrderedDict()
        self.connected = False
        self.msg = ''
        self.id = None
        #super(jJS9, self).__init__(host=self.node_url, id=wid+'JS9')
        
    
    def connect(self, wid = None, external=False):
            temp = self.wid
            if wid is not None:
                self.wid = wid
            if external:
                super(jJS9, self).__init__(host=self.node_url, id='JS9-'+self.wid)
                self.connected = True
                return
            if self.wid in self.displays:
                super(jJS9, self).__init__(host=self.node_url, id='JS9-'+self.wid)
                self.connected = True
            else:
                print(f'{self.wid} display does not exist')
                self.wid = temp
    
    def handler_displayed(self, widget):
        #self._connect()
        self.msg = 'connected'
    
    def new_display(self, attached=True, wid=None, height_px=600, width_px=580):
        if wid is not None:
            self.wid = str(wid)
        all_d = set()
        for r in self.get_instances():
            for j in r.displays.keys():
                all_d.add(j)
        if self.wid in all_d:
            print(f'{self.wid} exists. Enter a different id or remove current display')
            return
        html_code = "<iframe src='{}/{}' width={} height={}></iframe>".format(self.frame_url, self.wid, width_px, height_px)
        self.displays[self.wid] = {'attached': attached, 'obj':ipw.widgets.HTML(value = html_code)}
        if attached:
            display(self.displays[self.wid]['obj'])
        else:
            self.sc = Sidecar(title='{}'.format(self.wid), layout=ipw.Layout(width='580px', height='600px'))
            self.displays[self.wid]['obj'].on_displayed(self.handler_displayed)
            with self.sc:
                display(self.displays[self.wid]['obj'])
        return
    def close_display(self, wid=None):
        if wid is not None:
            closeid = wid
        else:
            closeid = self.wid
        temp = self.displays[closeid]
        if temp['attached']:
            temp['obj'].close()
        else:
            self.sc.close()
            temp['obj'].close()
        #self.displays.pop(closeid)
        del(self.displays[closeid])
        self.connected = False
        return
    
    def close_all_displays(self, force=False):
        tkeys = list(self.displays.keys())
        for kid in tkeys:
            self.close_display(wid = kid)
        try:
            self.sc.close_all()
        except AttributeError:
            pass
        if force:
            for r in self.get_instances():
                for jid in r.displays.keys():
                    temp = r.displays[jid]
                    if temp['attached']:
                        temp['obj'].close()
                    else:
                        r.sc.close()
                        temp['obj'].close()
                    del(r.displays[jid])
                    r.connected = False
        return