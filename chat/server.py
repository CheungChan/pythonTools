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
        debug = True
        self.HOST = ''
        if debug:
            self.PORT = 21568
            print('debug模式启动')
        else:
            self.PORT = 21567
        self.BUFSIZE = 1024 * 10
        self.ADDR = (self.HOST, self.PORT)
        self.clients = {}

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(self.ADDR)
        self.socket.listen(10)
        print('服务端启动了' + self.get_format_now())
        flag = False
        while True:
            conn, addr = self.socket.accept()
            if not debug:
                for c in self.clients.keys():
                    if c.getpeername()[0] == addr[0]:
                        self.__senderror('【' + self.clients.get(c) + "】客户端已开启一个，不可再重复开启", conn)
                        flag = True
                        break
                if flag:
                    continue
            threading.Thread(target=self.__in, args=(conn,)).start()

    def __in(self, conn):
        while True:
            try:
                tmp = json.loads(conn.recv(self.BUFSIZE).decode())
            except (ConnectionRefusedError,ConnectionResetError,ConnectionAbortedError,json.decoder.JSONDecodeError):
                name = self.clients[conn]
                del self.clients[conn]
                self.__printAndSendMsg('【系统提示】【' + name + '】' + self.get_format_now() + "下线了" + '\n',
                                       'system')
                self.__printAndSendOnline()
                return
            if not tmp:
                print("服务端没有接收到数据")
            name = tmp.get('name')
            data = tmp.get('message')
            history = tmp.get('history')
            if name:
                self.clients[conn] = name
                self.__printAndSendMsg( '【系统提示】【' + name + '】' + self.get_format_now() + "上线了" + '\n', \
                                                                'system')
                self.__printAndSendOnline()
            elif data:
                self.__printAndSendMsg('【' + self.clients[conn] + '】：    ' + self.get_format_now() + '\n','name_time')
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
        with open(os.path.join('history', self.get_format_db()+".db"), 'a',
                  encoding='utf-8') \
                as f:
            f.write(data)
        message = json.dumps({type: data})
        for c in self.clients.keys():
            try:
                c.send(message.encode())
            except (ConnectionResetError, ConnectionAbortedError):
                self.__handle_error(c)

    def __printAndSendOnline(self):
        online = ""
        for name in self.clients.values():
            online += name + '\n'
        message = json.dumps({"online": online})
        for c in self.clients.keys():
            try:
                c.send(message.encode())
            except (ConnectionResetError, ConnectionAbortedError):
                self.__handle_error(c)

    def __sendhistory(self, data, conn):
        print(self.get_format_now() + '发送给【' + self.clients[conn] + '】历史记录')
        message = json.dumps({"history": data})
        try:
            conn.send(message.encode())
        except:
            self.__handle_error(conn)

    def __handle_error(self, conn):
        name = self.clients[conn]
        print(name, '发送失败')
        self.clients.pop(conn)
        self.__printAndSendOnline()

    def __senderror(self, data, conn):
        print(data)
        message = json.dumps({"error": data})
        try:
            conn.send(message.encode())
        except:
            self.__handle_error(conn)

    def get_format_now(self):
        return datetime.now().strftime('  %Y-%m-%d %H:%M:%S  ')

    def get_format_db(self):
        return datetime.now().strftime('%Y-%m-%d %H')

if __name__ == '__main__':
    server()