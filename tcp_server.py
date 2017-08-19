from tcp_base import TcpBase
import threading
from deal_recv_message import *

class TcpServer(TcpBase):
    """tcp服务器(发送文件)"""
    def __init__(self,ip,port,queue):
        super().__init__(ip,port,queue)

    def _set_tcp_socket(self):
        """设置tcp服务器"""
        self._tcp_socket.bind((self._ip, self._port))
        self._tcp_socket.listen(128)

    def get_tcp_socket(self):
        """获得一个tcp服务器的套接字"""
        self._create_tcp_socket()
        self._set_tcp_socket()
        return self._tcp_socket

    def get_request_info(self):
        """获取请求"""
        self.get_tcp_socket()
        t1 = threading.Thread(target=self.get_file_info, args=('upload', ))
        t1.start()
        while True:
            conn, addr = self._tcp_socket.accept()
            self.upload_file((conn,addr))

    def upload_file(self,info):
        """上传文件"""
        conn, addr = info
        while True:
            data = conn.recv(1024)
            if data:
                file_info = DealMessage((data,addr)).deal_upload_message()                
                print(self._list)
                for e in self._list:
                    if int(e['package_id']) == int(file_info['package_id'])\
                    and int(e['file_id']) == int(file_info['file_id']):
                        with open(e['file_name'],'rb') as fout:
                            conn.send(fout.read())
                        print('发送成功')
                        self._list.remove(e)
                        conn.close()
                        return True
                else:
                    break
        conn.close()
