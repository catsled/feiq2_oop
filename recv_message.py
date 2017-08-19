from deal_recv_message import DealMessage
import maindata as md

class RecvMessage(object):
    """接收信息"""
    def __init__(self,udp_socket):
        self._udp_socket = udp_socket

    def recv_message(self):
        """接收信息"""
        while True:
            udp_message = self._udp_socket.recvfrom(1024)  # 通过udp接收到的消息
            DealMessage(udp_message,self._udp_socket).start()
            if not md.user_online:
                break
        try:
            self._udp_socket.close()
        except:
            raise TypeError('没有创建udp_socket')
        else:
            print('停止接收消息')

