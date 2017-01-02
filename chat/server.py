#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import socket
from datetime import datetime
import json
import os
import os.path

class server:

    def __init__(self):
        debug = False
        self.HOST = ''
        self.PORT = 21567
        self.BUFSIZE = 1024 * 10
        self.ADDR = (self.HOST, self.PORT)
        self.clients = {}

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.ADDR)
        self.socket.listen(10)
        print('服务端启动了')
        flag = False
        while True:
            conn, addr = self.socket.accept()
            if not debug:
                for c in self.clients.keys():
                    if c.getpeername()[0] == addr[0]:
                        self.__senderror("客户端已开启一个，不可再重复开启", conn)
                        flag = True
                        break
                if flag:
                    continue
            threading.Thread(target=self.__in, args=(conn,)).start()

    def __in(self, conn):
        while True:
            try:
                tmp = json.loads(conn.recv(self.BUFSIZE).decode())
            except (ConnectionRefusedError,ConnectionResetError):
                name = self.clients[conn]
                del self.clients[conn]
                self.__printAndSendMsg('【系统提示】' + name + "下线了" + '\n', 'system')
                self.__printAndSendOnline()
                return
            if not tmp:
                print("服务端没有接收到数据")
            name = tmp.get('name')
            data = tmp.get('message')
            history = tmp.get('history')
            if name:
                self.clients[conn] = name
                self.__printAndSendMsg('【系统提示】' + name + "上线了" + '\n', 'system')
                self.__printAndSendOnline()
            elif data:
                self.__printAndSendMsg('【' + self.clients[conn] + '】：    ' + datetime.now().strftime(
                    '%Y/%m/%d %X') + '\n','name_time')
                self.__printAndSendMsg(data + '\n', 'message')
            elif history:
                if history == '?':
                    files = os.listdir(os.path.join(os.getcwd(),'history'))[::-1]
                    l = json.dumps({"historylist": files})
                    conn.send(l.encode())
                else:
                    with open(os.path.join(os.getcwd(), 'history', history), encoding='utf-8') as f:
                        self.__sendhistory(f.read(), conn)


    def __printAndSendMsg(self, data, type):
        print(data)
        with open(os.path.join('history', datetime.now().strftime('%Y-%m-%d %H')+".db"), 'a',
                  encoding='utf-8') \
                as f:
            f.write(data)
        message = json.dumps({type: data})
        for c in self.clients.keys():
            try:
                c.send(message.encode())
            except (ConnectionResetError, ConnectionAbortedError):
                print(c,'发送失败')
                del self.clients[c]
                self.__printAndSendOnline()

    def __printAndSendOnline(self):
        online = ""
        for name in self.clients.values():
            online += name + '\n'
        message = json.dumps({"online": online})
        for c in self.clients.keys():
            try:
                c.send(message.encode())
            except (ConnectionResetError, ConnectionAbortedError):
                print(c, '发送失败')
                del self.clients[c]
                self.__printAndSendOnline()

    def __sendhistory(self, data, conn):
        print('发送给【' + self.clients[conn] + '】历史记录')
        message = json.dumps({"history": data})
        try:
            conn.send(message.encode())
        except:
            print(conn, '发送失败')
            del self.clients[conn]
            self.__printAndSendOnline()

    def __senderror(self, data, conn):
        print(data)
        message = json.dumps({"error": data})
        try:
            conn.send(message.encode())
        except:
            print(conn, '发送失败')
            del self.clients[conn]
            self.__printAndSendOnline()


if __name__ == '__main__':
    server()