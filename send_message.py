

class SendMessage(object):
    """发送信息"""
    def __init__(self,message,socket,ip='',port=2425):
        self._message = message
        self._ip = ip
        self._port = port
        self._udp_socket = socket

    def send_message(self):
        """发送信息"""
        self._udp_socket.sendto(self._message.encode('gbk'),(self._ip,self._port))
