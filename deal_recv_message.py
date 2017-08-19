"""
处理通过udp接收到的信息
"""
from build_message import *
from send_message import *
import maindata as md

class DealMessage(object):
    """信息处理"""
    def __init__(self,message,udp_socket=None):
        self._message = message
        self._data_dict = None 
        self._addr = message[1]
        self._udp_socket = udp_socket

    def _deal_recv_message(self):
        """处理接收到的信息"""
        data, addr = self._message
        self._data_dict = dict()
        data = data.decode('gbk',errors='ignore')
        data = data.split(":",5)
        self._data_dict['package_id'] = data[1]  # 包编号
        self._data_dict['command'] = data[-2]  # 命令
        self._data_dict['option'] = data[-1]  # 选项
        self._data_dict['user_name'] = data[3]
        return self._data_dict, addr

    def _split_command(self):
        """拆分命令"""
        command = int(self._data_dict['command']) & 0x000000ff
        opt = int(self._data_dict['command']) & 0xffffff00
        return command, opt

    def _classify_message(self):
        """信息分类"""
        self._deal_recv_message()
        command, opt = self._split_command()
        if command == md.ONLINE_MSG:  # 用户上线
            print('%s(%s) connected' % (self._data_dict['option'][:-2],self._addr[0]))
            self.add_user(self._data_dict['option'][:-2],self._addr[0])
        elif command == md.OFFLINE_MSG:  # 用户下线
            print('%s(%s) disconnected' % (self._data_dict['option'][:-2],self._addr))
            if not md.online_user_list:
                user_dict = dict()
                user_dict['user_name'] = self._data_dict['option'][:-2]
                user_dict['user_ip'] = self._addr[0]
                md.online_user_list.remove(user_dict)  # 将下线用户从列表中删除
        elif command == md.RESPONSE_ONLINE:  # 回复在线信息
            self.add_user(self._data_dict['option'][:-2],self._addr[0])
        elif command == md.SEND_MSG:  # 收到聊天信息
            print('%s(%s)>>>>%s' % (self._data_dict['user_name'],self._addr[0],
                  self._data_dict['option'][:-2]))
            if opt & 0x00f00000 == md.FILE_MSG:  # 收到文件信息
                info = self.deal_download_message()
                md.download_list.append(info)
        message = BuildMessage(md.RESPONSE_RECV).build_message()
        SendMessage(message,self._udp_socket,self._addr[0]).send_message()

    def add_user(self,user_name,addr):
        """添加在线用户"""
        user_dict = dict()
        user_dict['user_name'] = self._data_dict['option'][:-2]
        user_dict['user_ip'] = self._addr[0]
        if user_dict not in md.online_user_list:
            md.online_user_list.append(user_dict)  # 将用户添加到在线列表中

    def _split_download_option(self):
        """拆分下载文件信息"""
        # option:(file_id,file_name,file_size,file_time,file_property)
        self._deal_recv_message()
        option = self._data_dict['option']
        upload_file = dict()
        data = option.split(":",5)
        upload_file['file_id'] = data[0]  #  下载需要的文件编号
        upload_file['file_name'] = data[1]  #  保存在下载列表中
        upload_file['package_id'] = self._data_dict['package_id']  # 下载需要的包编号
        upload_file['addr'] = self._addr
        upload_file['file_size'] = data[2]
        return upload_file

    def deal_download_message(self):
        """处理文件下载信息"""
        # \x000:yy:00:598fd0d7:1:\x07\x00
        upload_info = self._split_download_option()
        upload_dict = dict()
        upload_dict['type'] = 'upload'
        upload_dict['data'] = upload_info
        md.queue.put(upload_dict)
        return upload_info

    def deal_upload_message(self):
        """处理文件上传信息"""
        #1_lbt80_0#128#323A64723B11#0#0#0#4000#9:1502281066:pls:DESKTOP-VSL9V3N:96:598afadf:0:0:
        self._deal_recv_message()
        file_dict = dict()
        data = self._data_dict['option'].split(":",3)
        file_dict['package_id'] = int(data[0], 16)
        file_dict['file_id'] = data[1]
        return file_dict

    def start(self):
        """执行方法"""
        self._classify_message()
