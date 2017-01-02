#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import socket
from datetime import datetime
import json

class server:

    def __init__(self):
        self.HOST = ''
        self.PORT = 21567
        self.BUFSIZE = 1024 * 10
        self.ADDR = (self.HOST, self.PORT)
        self.clients = {}

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.ADDR)
        self.socket.listen(10)
        print('服务端启动了')
        while True:
            conn, addr = self.socket.accept()
            threading.Thread(target=self.__in, args=(conn,)).start()

    def __in(self,conn):
        while True:
            try:
                tmp = json.loads(conn.recv(self.BUFSIZE).decode())
            except (ConnectionRefusedError,ConnectionResetError):
                name = self.clients[conn]
                del self.clients[conn]
                self.__printAndSendMsg('【系统提示】' + name + "下线了")
                return
            if not tmp:
                print("服务端没有接收到数据")
            name = tmp.get('name')
            data = tmp.get('message')
            if name:
                self.clients[conn] = name
                self.__printAndSendMsg('【系统提示】' + name + "上线了")
                continue
            elif data:
                data = '【' + self.clients[conn] + '】：    ' + datetime.now().strftime('%Y/%m/%d %X') + \
                      '\n' + data
                self.__printAndSendMsg(data)


    def __printAndSendMsg(self, data):

        print(data)
        online = ""
        for name in self.clients.values():
            online += name + '\n'
        message = json.dumps({'message': data, "online": online})
        for c in self.clients.keys():
            try:
                c.send(message.encode())
            except (ConnectionResetError, ConnectionAbortedError):
                print(c,'发送失败')

if __name__ == '__main__':
    server()