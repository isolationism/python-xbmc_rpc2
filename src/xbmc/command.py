#!/usr/bin/python

# Standard library
import socket
from uuid import uuid4 as generate_random_uuid
from StringIO import StringIO

# Third-party libraries
from simplejson import dumps as encode, loads as decode


class XBMC(object):
    """
    Controls an XMBC Instance via sockets.
    """

    socket_timeout = 1
    rpc_version = "2.0"
    buffer_size = 1024

    def __init__(self, server='localhost', port='9090'):
        """
        Constructor
        """
        self._c = self._connect(server, port)

    def _connect(self, server, port):
        """
        Returns an open socket connection
        """
        conn = socket.create_connection((server, port))
        conn.settimeout(self.socket_timeout)
        return conn

    def _disconnect(self):
        """
        Closes a socket connection
        """
        if getattr(self, '_c', False):
            self._c.close()
        return True

    def request(self, method, params=None):
        """
        Creates a new request using the passed method and parameters.
        """
        req_id = generate_random_uuid().hex
        req = {
            'jsonrpc': self.rpc_version,
            'method': method,
            'id': req_id,
        }
        if params:
            req['params'] = params
        enc_req = encode(req)
        self._c.send(enc_req)
        enc_res = self._c.recv(self.buffer_size)
        res = decode(enc_res)
        if res.get('id') != req_id:
            raise RuntimeError("Received unexpected response: %s" \
                               % (res, ))
        return res.get('result')

    def JSONRPC_Version(self):
        """
        Returns the JSON RPC version in use
        """
        return self.request('JSONRPC.Version')

