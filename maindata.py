


#feiq命令

ONLINE_MSG = 0x00000001  # 上线信息
OFFLINE_MSG = 0x00000002  # 下线信息
RESPONSE_ONLINE = 0x00000003  # 在线回复
SEND_MSG = 0x00000020  # 发送信息
RESPONSE_RECV = 0x00000021  # 收到信系
FILE_MSG = 0x00200000  #发送文件
NORMAL_FILE = 0x00000001  # 普通文件


# 全局变量

user_online = False
online_user_list = list()
user_info_list = list()
current_file_list = list()
download_list = list()
upload_list = list()


broadcast_ip = '255.255.255.255'

# 文件信息队列
queue = None
