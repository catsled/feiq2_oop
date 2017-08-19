import os
import maindata as md

def display_window():
    """显示用户界面"""
    print('+++++++++fei+++++++++')
    print('        1.上线       ')
    print('        2.下线       ')
    print('        3.显示用户   ')
    print('        4.发送信息   ')
    print('        5.发送文件   ')
    print('        6.下载文件   ')
    print('+++++++++++++++++++++')

def display_user_list():
    """显示在线用户"""
    for i, user in enumerate(md.online_user_list):
        md.user_info_list.append(user)
        print(i, user)

def display_current_list():
    """显示当前目录下的所有文件(不包括文件夹)"""
    file_list = os.listdir()
    temp_list = list()
    for e in file_list:
        if not os.path.isdir(e):
            temp_list.append(e)
    for i, e in enumerate(temp_list):
        md.current_file_list.append(e)
        print("{}: {}".format(i,e))

def display_current_upload():
    """显示当前正在上传的文件"""
    for e in md.upload_list:
        print(e)

def display_current_download():
    """显示可下载的文件"""
    for i, e in enumerate(md.download_list):
        print('{}: {}'.format(i,e))
