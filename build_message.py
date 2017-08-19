"""
构建要发送的信息
"""
import maindata as md
import time
from deal_recv_message import *
import os

class BuildMessage(object):
    """构建信息"""
    def __init__(self,command=-1,option=''):
        self._command = command
        self._option = option
        self._package_id = int(time.time())

    def build_message(self):
        """构建信息"""
        # %d:%d:%s:%s:%d:%s(version,packageid,user,hostname,command,option)
        message_form = "%d:%d:%s:%s:%d:%s"
        message = message_form % (1, self._package_id, 'me', 'localhost', self._command, self._option)
        return message

    def build_upload_message(self,file_name):
        """构建上传文件信息"""
        # option:(file_id,file_name,file_size,file_time,file_property)
        try:
            file_size = os.path.getsize(file_name)
            file_time = int(os.path.getctime(file_name))
        except Exception as ret:
            print('文件不存在',ret)
        else:
            option = "%d:%s:%x:%x:%x" % (0, file_name, file_size, file_time, md.NORMAL_FILE)
            self._command = md.SEND_MSG | md.FILE_MSG
            self._option = '\0' + option
            #将文件信息加入队列用来获得上传文件的信息
            upload_info = dict()
            upload_info['package_id'] = self._package_id
            upload_info['file_name'] = file_name
            upload_info['file_id'] = 0
            temp_info = dict()
            temp_info['type'] = 'upload' 
            temp_info['data'] = upload_info  # 保存上传文件的关键信息
            md.queue.put(temp_info)
            md.upload_list.append(upload_info)
            return self.build_message()

    def build_download_message(self,packageid,fileid):
        """构建文件下载信息"""
        self._option = "%x:%x:%x:" % (int(packageid),int(fileid),0)
        self._command = 96
        return self.build_message()
