#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

import marshal
from tkinter import *
from tkinter import messagebox
from ser import Ser

class Box(object):
    def __init__(self):
        self.top = Tk()
        self.top.title('旗丰控制系统')

        self.set_menu()
        #self.set_main()
        self.login()
        #self.config()

    def set_menu(self):
        menu = Menu(self.top)
        self.top.config(menu=menu)

        menu.add_command(label='参数设置', command=lambda:self.config())
        menu.add_command(label='帮助', command=self.show_help)
        menu.add_command(label='退出', command=lambda:self.top.quit())

    def show_help(self):
        f = open('data.txt', 'rb')
        data = marshal.load(f)
        f.close()
        messagebox.showinfo(message='售后电话: \n%s' % data[3])

    def config(self):
        top = Toplevel()
        frame = Frame(top, padx=20, pady=20)
        frame.grid(row=0)

        title = Label(frame, text='参数设置')

        v1 = StringVar()
        v2 = StringVar()
        v3 = StringVar()
        v4 = StringVar()
        label1 = Label(frame, text='冷凝器', wraplength=100)
        entry1 = Entry(frame, width=40, textvariable=v1)
        label2 = Label(frame, text='蒸发箱')
        entry2 = Entry(frame, width=40, textvariable=v2)
        label3 = Label(frame, text='空调管道')
        entry3 = Entry(frame, width=40, textvariable=v3)
        label4 = Label(frame, text='维修电话')
        entry4 = Entry(frame, width=40, textvariable=v4)

        f = open('data.txt', 'rb')
        data = marshal.load(f)
        v1.set(data[0])
        v2.set(data[1])
        v3.set(data[2])
        v4.set(data[3])
        f.close()

        ok = Button(frame, text='保存',
                command=lambda:self.set_config(
                    top,
                    entry1.get(),
                    entry2.get(),
                    entry3.get(),
                    entry4.get()
                ))
    
        cancle = Button(frame, text='返回',command=lambda:top.destroy())

        title.grid(row=0, column=1, columnspan=2)
        label1.grid(row=1, column=0, padx=20, pady=20)
        entry1.grid(row=1, column=1, columnspan=3, padx=20, pady=20)
        label2.grid(row=2, column=0, padx=20, pady=20)
        entry2.grid(row=2, column=1, columnspan=3, padx=20, pady=20)
        label3.grid(row=3, column=0, padx=20, pady=20)
        entry3.grid(row=3, column=1, columnspan=3, padx=20, pady=20)
        label4.grid(row=4, column=0, padx=20, pady=20)
        entry4.grid(row=4, column=1, columnspan=3, padx=20, pady=20)
        ok.grid(row=5, column=1, padx=20, pady=20)
        cancle.grid(row=5, column=2, padx=20, pady=20)

    def set_config(self, top, v1,v2,v3,v4):
        f = open('data.txt', 'wb')
        #data = {
        #    {'lengnq', v1},
        #    {'zhengfx', v2},
        #    {'konggd', v3},
        #    {'phone', v4}
        #}
        data = [v1,v2,v3,v4]
        marshal.dump(data, f)
        f.close()
        top.destroy()


    def cload(self, current, new):
        current.destroy()
        if new == 'main':
            self.set_main()
        elif new == 'config':
            self.config()

    def login(self):
        frame = Frame(self.top, padx=160, pady=120)
        frame.grid(row=0)

        label = Label(frame, text='设备地址', width=10)
        label.grid(row=0, column=0)

        entry = Entry(frame, width=20)
        entry.grid(row=0, column=1)

        button = Button(frame, text='连接',\
                command=lambda:self.connect(entry.get(), frame))
        button.grid(row=1, column=0, columnspan=2, pady=10)

    def connect(self, value, frame):
        try:
            self.ser = Ser(value)
            frame.destroy()
            self.set_main()
        except:
            messagebox.showerror(message='设备连接失败')

        #frame.destroy()
        #self.set_main()


    def set_main(self):
        main = Frame(self.top, pady=60)
        main.grid(sticky='nsew')

        label = Label(main, text='可视化空调清洗设备', font='Times 22', fg='#316be6')
        label.grid(column=0, row=0, columnspan=3, padx=240, pady=60)

        button1 = Button(main, text='冷凝器', command=lambda:self.start(1,[0,1]))
        button2 = Button(main, text='蒸发箱', command=lambda:self.start(2,[0,2]))
        button3 = Button(main, text='空调管道', command=lambda:self.start(3,[0,3]))

        button1.grid(column=0, row=2, pady=60)
        button2.grid(column=1, row=2, pady=60)
        button3.grid(column=2, row=2, pady=60)

    def start(self, config, num_list):
        for item in num_list:
            self.ser.turn_on(item)

        f = open('data.txt', 'rb')
        data = marshal.load(f)
        f.close()
        if data[config-1]:
            timer = int(data[config-1]) * 1000

        top = Toplevel()
        frame = Frame(top, padx=80, pady=40)
        frame.pack()
        message = Message(frame, text='正在清洗中...', width=200, pady=20)
        message.pack()
        message.after(timer, lambda:self.end(top, num_list))
        Button(frame, text='取消', command=lambda:self.end(top, num_list)).pack()

    def end(self, top, num_list):
        for item in num_list:
            self.ser.turn_off(item)
        top.destroy()
