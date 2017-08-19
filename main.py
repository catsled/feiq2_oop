import threading
import multiprocessing
from udp_socket import *
from recv_message import *
from send_message import *
from build_message import *
from Display import *
import maindata as md
from tcp_server import *
from tcp_client import *

def main():
    """整体控制"""
    md.user_online = True
    # 创建信息通道queue
    md.queue = multiprocessing.Queue()
    # 创建主线程发送信息的套接字
    main_udp_socket = Udp('',2425).get_udp_socket()
    # 创建信息接收的子线程(处理)
    t1 = threading.Thread(target=RecvMessage(main_udp_socket).recv_message)
    t1.start()
    # 创建处理文件传输的子进程(上传,下载)
    p1 = multiprocessing.Process(target=TcpServer('',2425,md.queue).get_request_info) 
    p1.start()
    # 根据不同情况进行数据的发送
    while True:
        display_window()
        choose = input('Choose:')
        if choose == '1':  # 上线
            message = BuildMessage(md.ONLINE_MSG,'me').build_message()
            SendMessage(message,main_udp_socket,md.broadcast_ip).send_message()
        elif choose == '2':  # 下线
            message = BuildMessage(md.OFFLINE_MSG,'me').build_message()
            SendMessage(message,main_udp_socket,md.broadcast_ip).send_message()
        elif choose == '3':  # 打印在线用户列表
            display_user_list()            
        elif choose == '4':  # 发送聊天信息
            ip = md.user_info_list[int(input('Num:'))]['user_ip']
            chat_message = input('Message:')
            if not (ip and chat_message):
                pass
            message = BuildMessage(md.SEND_MSG,chat_message).build_message()
            SendMessage(message,main_udp_socket,ip).send_message()
        elif choose == '5':  # 发送文件
            num = int(input('Num:'))
            ip = md.user_info_list[num]['user_ip']
            print(ip)
            display_current_list()
            try:
                file_name = md.current_file_list[int(input('File_n:'))]
            except Exception as ret:
                print("%s" % ret)
            else:
                message = BuildMessage().build_upload_message(file_name)
                SendMessage(message,main_udp_socket,ip).send_message()
                print('等待上传:....')
        elif choose == '6':  # 下载文件
            display_current_download()
            file_name = md.download_list[int(input('File_n:'))]['file_name']
            TcpClient('',2425,md.queue).download_file(file_name)


if __name__ == '__main__':
    main()
