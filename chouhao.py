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
        # # #设置菜单栏
        # menubar = Menu(self)
        # setmenu = Menu(menubar)
        # setmenu.add_command(label = "设置人数",command = self.setting)
        # menubar.add_cascade(label = "设置",menu=setmenu)
        # self.config(menu = menubar)
        #主体
        self.create_f1()
        self.create_f2(zongshu)
        self.create_f3()


    def create_f1(self):

        self.f1 = Frame(self)
        with open('name.db',encoding = 'utf-8') as f:
            self.name = f.read()
        Label(self.f1,text= self.name,font=("隶书", 30),pady=10).pack()
        self.f1.pack(side=TOP)

    def create_f2(self,zongshu):

        self.f2 = Frame(self)

        f21 = Frame(self.f2)
        Label(f21,text="本次抽号，将从右边方框中的数字随机抽取一个",anchor = W,justify=LEFT,wraplength = 300,font=("华文楷体", 20),borderwidth=20).pack()
        Button(f21,text="设置随机人数",command = self.setting).pack()
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
        f31 = Frame(f3)
        Label(f31,text='抽中号码为:',font=("微软雅黑", 30)).pack()
        self.nuLabel = Label(f31,text = '0',font=("微软雅黑", 40),fg = '#ed1941')
        self.nuLabel.pack()
        f31.grid(row=0,sticky = W)
        f32 = Frame(f3)
        self.btn1 = Button(f32,text='开始',command = self.start,width = 20,height = 3,bg = "#ffce7b")
        self.btn1.pack(side=LEFT,padx = 30)
        self.btn2 = Button(f32,text='结束',command = self.stop,width = 20,height = 3,bg = '#f15a22')
        self.btn2.pack(side=RIGHT,padx = 30)
        f32.grid(row=0,column = 1,sticky = E)
        f3.pack(side=BOTTOM)

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
                with open('chouhao.db','w') as f:
                    f.write(self.entry.get())
                root.destroy()
            except ValueError:
                with open('chouhao.db','w') as f:
                    f.write(self.i)
                messagebox.showerror(title='温馨提示', message = "请输入正整数")
                self.entry.focus_set()

        Button(root, text="确定", command = on_click).pack(side=LEFT,padx = 75)
        Button(root, text="取消", command = root.destroy).pack(side=LEFT)

        root.mainloop()



    def start(self):

        if self.btn1['state'] == 'normal':
            self.stopped = False
        #pdb.set_trace()
        def change():
            if self.stopped:
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
            self.after(50,change)

        change()


    def stop(self):

        self.stopped = True
        self.btn1.config(state = 'normal')

def main(zongshu):

    gui = GUI(zongshu)
    gui.title("随机抽号程序")
    gui.geometry('700x480+50+80')
    gui.mainloop()

if __name__ == "__main__":

    with open('chouhao.db','r') as f:
        zongshu = f.read()
    main(zongshu)