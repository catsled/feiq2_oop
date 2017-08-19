"""
套接字基类
"""

class SocketBase(object):
    """创建套接字基类(udp,tcp)"""
    def __init__(self,ip,port):
        self._ip = ip
        self._port = port
