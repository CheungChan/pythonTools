#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: cheungchan
from tkinter import *
import random,time,math
from tkinter import messagebox

class GUI(Tk):
    def __init__(self,zongshu):

        Tk.__init__(self)
        self.l = list()
        self.checked = 0
        self.stopped = False
        self.restart = False
        self.create_f1()
        self.create_f2(zongshu)
        self.create_f3()
        self.create_f4()


    def create_f1(self):

        self.f1 = Frame(self)
        with open('name.db',encoding = 'utf-8') as f:
            self.name = f.read()
        Label(self.f1,text= self.name,font=("隶书", 30),pady=10).pack()
        self.f1.pack(side=TOP)

    def create_f2(self,zongshu):

        self.f2 = Frame(self)

        f21 = Frame(self.f2)
        Label(f21,text="本次抽号，将从右边方框中的数字随机抽取一个",anchor = W,justify=LEFT,wraplength = 300,font=("华文楷体", 20),borderwidth=10).pack(side=TOP)
        Button(f21,text="设置随机号数量",command = self.setting).pack(side=LEFT,padx=10)
        f21.grid(row=0,sticky=W)
        f22 = Frame(self.f2,bg='#cde6c7')
        zongshu = int(zongshu)
        pingfanggen = int(math.sqrt(zongshu))

        index = 0
        for i in range(zongshu//pingfanggen):
            for j in range(pingfanggen + 1):
                index += 1
                if index > zongshu:
                    break
                b = Label(f22,text=str(index),height = 1,width=5,relief='groove',bg='#00a6ac')
                b.grid(row = i, column = j,padx = 5,pady = 5)
                self.l.append(b)
        f22.grid(row=0,column=1,sticky = E)

        self.f2.pack(pady = 30)

    def create_f3(self):
        f3 = Frame(self)
        Label(f3,text='抽中号码为',font=("微软雅黑", 30)).pack()
        self.nuLabel = Label(f3,text = '0',font=("微软雅黑", 40),fg = '#ed1941')
        self.nuLabel.pack()
        f3.pack()

    def create_f4(self):

        f4 = Frame(self)
        self.btn1 = Button(f4,text='开始',command = self.start,width = 20,height = 3,bg = "#ffce7b")
        self.btn1.pack()
        f4.pack()

    def setting(self):

        root = Toplevel()
        root.title("设置随机个数")
        root.geometry('300x100+300+300')


        l1 = Label(root, text="随机个数(设置完请重启）：")
        l1.pack()
        with open('chouhao.db','r') as f:
            self.i = f.read()
        v = StringVar()
        self.entry = Entry(root,textvariable = v)
        v.set(self.i)
        self.entry.icursor('end')
        self.entry.pack()
        self.entry.focus_set()

        def on_click():
            try:
                if int(self.entry.get()) <= 0:
                    raise ValueError("请输入正整数")
                if int(self.entry.get()) > 150:
                    raise ValueError("数字太大")
                with open('chouhao.db','w') as f:
                    f.write(self.entry.get())
                root.destroy()
            except ValueError as e:
                with open('chouhao.db','w') as f:
                    f.write(self.i)
                messagebox.showerror(title='温馨提示', message = str(e))
                self.entry.focus_set()

        Button(root, text="确定", command = on_click).pack(side=LEFT,padx = 75)
        Button(root, text="取消", command = root.destroy).pack(side=LEFT)

        root.mainloop()

    def start(self):

        global n
        n = 0
        def change():
            global n
            if n >= 50:
                self.btn1.config(state = 'normal')
                return
            l = self.l
            i = random.randint(0,len(l) - 1)
            #randint(a, b) method of random.Random instance
            #Return random integer in range [a, b], including both end points.
            l[self.checked].config(bg = '#00a6ac')
            l[i].config(bg = '#d71345')
            self.checked = i
            self.nuLabel.config(text=str(i + 1))
            self.btn1.config(state = 'disabled')
            n += 1
            self.after(50,change)

        change()

def main(zongshu):

    gui = GUI(zongshu)
    gui.title("随机抽号程序")
    gui.geometry('700x480+50+80')
    gui.mainloop()

if __name__ == "__main__":

    with open('chouhao.db','r') as f:
        zongshu = f.read()
    main(zongshu)