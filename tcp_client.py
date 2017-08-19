
from tcp_base import TcpBase
import threading
from deal_recv_message import *
import time
import maindata as md

class TcpClient(TcpBase):
    """tcp服务器(发送文件)"""
    def __init__(self,ip,port,queue):
        super().__init__(ip,port,queue)

    def _set_tcp_socket(self):
        """设置tcp客户端"""
        pass

    def get_tcp_socket(self):
        """获得一个tcp服务器的套接字"""
        self._create_tcp_socket()
        return self._tcp_socket

    def download_file(self,file_name):
        """下载文件"""
        self.get_tcp_socket()
        for e in md.download_list:
            if file_name == e['file_name']:  # 判断请求的文件是否在下载列表中
                package_id = e['package_id']
                file_id = 0
                message = BuildMessage().build_download_message(package_id,file_id)
                self._tcp_socket.connect(e['addr'])
                self._tcp_socket.send(message.encode('gbk'))
                f = open(file_name,'wb')
                length = 0
                while True:
                    data = self._tcp_socket.recv(1024)
                    if data:
                        f.write(data)
                        length += len(data)
                    if length >= int(e['file_size']):
                        print('下载完成.....')
                        break
                f.close()
                self._tcp_socket.close()
            break
