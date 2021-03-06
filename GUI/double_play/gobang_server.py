# -*- coding: utf-8 -*-
# 服务器端 首先运行这个程序 建立服务器 后期有需要可以使用云服务器
import os
import socket
import json
import threading
import time
import sys
from queue import Queue


def server_handle_1(c1, c2):
    # 接受到client1的消息 发送到client2上去
    while True:
        data = c1.recv(1024)
        print(data)
        time.sleep(1)
        c2.send(('%s' % data.decode('utf-8')).encode('utf-8'))

def server_handle_2(c1, c2):
    # 接受到client1的消息 发送到client2上去
    while True:
        data = c2.recv(1024)
        print(data)
        time.sleep(1)
        c1.send(('%s' % data.decode('utf-8')).encode('utf-8'))



def server_init():
    # 创建 socket 对象
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 获取本地主机名
    host = socket.gethostname()
    port = 9999
    # 绑定端口号
    s.bind((host, port))
    address = (host, port)
    # 设置最大连接数，超过后排队
    s.listen(2)
    print("等待客户端1连接")
    c1, addr1 = s.accept()
    print('客户端1连接成功\n')  # 打印接受到的信息
    print("等待客户端2连接")
    c2, addr2 = s.accept()
    print('客户端2连接成功\n')  # 打印接受到的信息
    t1 = threading.Thread(target=server_handle_1, args=(c1, c2))
    t2 = threading.Thread(target=server_handle_2, args=(c1, c2))
    t1.start()
    t2.start()

if __name__ == '__main__':
    server_init()

