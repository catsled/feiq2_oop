import socket
from socket_base import SocketBase


class Udp(SocketBase):
    """创建udp套接字及其相应的操作"""

    def __init__(self,ip,port):
        super().__init__(ip,port)
        self._udp_socket = None

    def _create_udp_socket(self):
        """创建udp套接字"""
        self._udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def _set_udp_socket(self):
        """设置udp套接字"""
        self._udp_socket.bind((self._ip, self._port))
        self._udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # 设置允许广播

    def get_udp_socket(self):
        """获得udp套接字"""
        self._create_udp_socket()
        self._set_udp_socket()
        return self._udp_socket

