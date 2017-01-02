#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import socket
import sys
import os
import json

class client:

    def __init__(self):
        self.SERVER_IP = '192.168.3.13'
        self.PORT = 21567
        self.ADDR = (self.SERVER_IP, self.PORT)
        self.BUFSIZE = 1024 * 10

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect(self.ADDR)
        except (ConnectionRefusedError,ConnectionResetError):
            print("服务端没有启动")
            sys.exit(-1)
        data = json.dumps({"name": os.getlogin()})
        self.socket.send(data.encode())
        threading.Thread(target=self.__in).start()
        threading.Thread(target=self.__out).start()

    def __in(self):
        while True:
            data = input()
            if not data:
                continue
            data = json.dumps({"message":data})
            self.socket.send(data.encode())

    def __out(self):
        while True:
            try:
                data = self.socket.recv(self.BUFSIZE).decode()
            except (ConnectionRefusedError,ConnectionResetError):
                print("服务端没有启动")
                sys.exit(-1)
            if not data:
                print('没有从服务端接收到数据')
            data = json.loads(data)
            message = data.get('message')
            online = data.get('online')
            if message:
                print(message)
            if online:
                print("上线" + online)

if __name__ == '__main__':
    client()