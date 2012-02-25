#!/usr/bin/python

import socket
from simplejson import dumps as encode, loads as decode

class XBMC(object):
    """
    Controls an XMBC Instance via sockets.
    """
