import socket
from socket_base import SocketBase

class TcpBase(SocketBase):
    """tcp基础类"""
    def __init__(self,ip,port,queue):
        super().__init__(ip,port)
        self._tcp_socket = None
        self._queue = queue
        self._list = list()

    def _create_tcp_socket(self):
        """创建tcp套接字"""
        self._tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _set_tcp_socket(self):
        """设置tcp套接字"""
        # 抽象方法
        pass
 
    def get_file_info(self,species):
        """获取文件信息"""
        while True:
            e = self._queue.get()
            if e['type'] == species:
                self._list.append(e['data'])
            else:
                self._queue.put(e)


