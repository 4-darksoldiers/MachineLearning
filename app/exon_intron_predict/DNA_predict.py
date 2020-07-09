"""
本文件是预测外显子/内含子程序的GUI界面设计源代码
版本：3.2
作者：叶佳晨
最后一次修改时间：2020/07/09
"""
from tkinter import *
import tkinter.messagebox as mb
import tkinter.filedialog as fd
from simulate import *


class ExonIntron_predict:
    def __init__(self):  # 初始化方法
        self.root = Tk()
        self.root.withdraw()
        self.root.title("DNA预测程序")
        self.initFace = Frame(self.root)
        self.initFace.grid()  # initFace是登录界面
        Label(self.initFace, text="欢迎使用本外显子/内含子预测程序\n请先登录！", font=(
            "幼圆", 17)).grid(column=3, columnspan=5, rowspan=2, padx=50)
        self.photo = PhotoImage(file="dna.gif")
        Label(self.initFace, image=self.photo).grid(
            row=2, column=0, columnspan=4, rowspan=6)
        Label(self.initFace, text="用户名：", font=("幼圆", 14)).grid(
            row=3, column=7, sticky=E, padx=20)
        Label(self.initFace, text="密  码：", font=("幼圆", 14)).grid(
            row=4, column=7, sticky=E, padx=20)
        self.user = StringVar()  # 用于存储用户输入的用户名
        self.code = StringVar()  # 用于存储用户输入的密码
        Entry(self.initFace, textvariable=self.user).grid(
            row=3, column=8, columnspan=3, sticky=E+W, ipadx=25, ipady=4)
        Entry(self.initFace, textvariable=self.code, show='*').grid(row=4,
                                                                    column=8, columnspan=3, sticky=E+W, ipadx=25, ipady=4)  # 让用户输入时密码显示为‘*’
        Button(self.initFace, text="登录", command=self.login,
               font=("幼圆", 12)).grid(row=6, column=8, padx=10)
        Button(self.initFace, text="注册", command=self.signUp,
               font=("幼圆", 12)).grid(row=6, column=9, padx=20)
        Button(self.initFace, text="退出", command=self.quit, font=(
            "幼圆", 12)).grid(row=7, column=10, padx=10, pady=10)
        self.root.update_idletasks()
        self.root.geometry('1000x520+%d+%d' % ((self.root.winfo_screenwidth()-self.root.winfo_width()
                                                )/2, (self.root.winfo_screenheight()-50-self.root.winfo_height())/2))  # 主要作用是让窗口处于屏幕正中间；下同
        self.root.deiconify()
        try:
            file = open(".passwd.txt", "r")
        except FileNotFoundError:
            file = open(".passwd.txt", "w")
            file.write("admin;admin")
        file.close()  # 这一步比较关键，由于本程序中包含一个登录窗口，因此需要用文件存储
        # 使用try...except的方法，可以保留之前用户创建的账户，同时若保存密码的文件被误删，这样也可以创建而保证程序没有错误
        self.root.mainloop()

    def login(self):  # 登录功能函数
        file = open(".passwd.txt", "r")
        flag = 0
        for passwd in file.readlines():
            passwd = passwd.strip()
            passwd = passwd.split(';')
            if self.user.get() == passwd[0]:
                flag = 1  # flag用于检索该用户名是否已经被占用，若未被占用则为0，下面signUp函数中同理
                if self.code.get() == passwd[1]:
                    mb.showinfo(title="登录成功！", message="欢迎您，"+self.user.get())
                    self.operate()
                    break
                else:
                    mb.showerror("错误", "密码错误！")
        file.close()
        if flag == 0:
            is_sign_up = mb.askyesno("提示：", "您还未注册，是否注册用户？")
            if is_sign_up:
                self.signUp()

    def signUp(self):  # 注册功能函数
        def signUpConfirm():  # 注册的确认函数，主要功能是用于检索用户密码输入是否正确和该用户是否已被注册
            if confirm.get() != code.get():
                mb.showerror("错误", "确认密码输入错误！")
            else:
                file = open(".passwd.txt", "r+")
                flag = 0
                for passwd in file.readlines():
                    passwd = passwd.strip()
                    passwd = passwd.split(';')
                    if user.get() == passwd[0]:
                        flag = 1
                if flag == 1:
                    mb.showerror("错误", "该用户已被注册！")
                else:
                    flag = mb.askokcancel("提示", "确认注册用户%s吗？" % user.get())
                    if flag:
                        file.write("\n%s;%s" % (user.get(), code.get()))
                        mb.showinfo(title="注册", message="用户%s 注册成功！" %
                                    (user.get()))
                        win.destroy()
                        self.user.set(user.get())
                        self.code.set(code.get())
                file.close()

        win = Toplevel(self.root)
        win.title("注册")
        user = StringVar()
        user.set(self.user.get())
        code = StringVar()
        code.set(self.code.get())
        confirm = StringVar()
        Label(win, text="用  户 名：", font=("幼圆", 13)).grid(
            row=1, column=0, sticky=E, pady=10)
        Label(win, text="密      码：", font=("幼圆", 13)).grid(
            row=2, column=0, sticky=E, pady=10)
        Label(win, text="确认密码：", font=("幼圆", 13)).grid(
            row=3, column=0, sticky=E, pady=10)
        Entry(win, textvariable=user).grid(row=1, column=1)
        Entry(win, textvariable=code, show='*').grid(row=2, column=1)
        Entry(win, textvariable=confirm, show='*').grid(row=3, column=1)
        Button(win, text="确认", command=signUpConfirm,
               font=("幼圆", 12)).grid(row=4, column=0)
        Button(win, text="取消", command=win.destroy,
               font=("幼圆", 12)).grid(row=4, column=1)
        win.update_idletasks()
        win.geometry('%dx%d+%d+%d' % (win.winfo_width(), win.winfo_height(), (win.winfo_screenwidth() -
                                                                              win.winfo_width())/2, (win.winfo_screenheight()-50-win.winfo_height())/2))

    def operate(self):  # 核心操作：以字符串或fasta文件输入待测DNA序列
        def choose_file():
            self.filePath.set(fd.askopenfilename(
                title="选择fasata文件", filetypes=[("fasta文件", ".fasta .fa")]))

        self.initFace.destroy()
        self.main = Frame(self.root)
        self.main.grid()
        self.filePath = StringVar()
        self.choose = IntVar()
        self.choose.set(1)
        Radiobutton(self.main, text="在下方输入待预测的DNA序列", font=(
            "幼圆", 14), value=0, variable=self.choose).grid(row=0, column=2, ipadx=100, pady=15)
        self.seq = Text(self.main, height=9)
        self.seq.grid(row=1, column=2, columnspan=8,
                      sticky=E+W, padx=90, ipadx=120, ipady=20)
        Radiobutton(self.main, text="导入fasta格式的DNA序列文件", font=(
            "幼圆", 14), value=1, variable=self.choose).grid(row=2, column=2, ipadx=100, pady=35)
        f = Frame(self.main)
        f.grid(row=3, column=2, columnspan=8)
        Label(f, text="文件路径：", font=("幼圆", 11)).grid()
        Entry(f, textvariable=self.filePath).grid(
            row=0, column=1, ipadx=70, sticky=W+S+N+E)
        Button(f, text="选择文件", command=choose_file,
               font=("幼圆", 11)).grid(row=0, column=2)
        Button(self.main, text="预  测", command=self.run, font=(
            "幼圆", 16)).grid(row=4, column=2, pady=40, sticky=E)
        Button(self.main, text="退出", command=self.quit,
               font=("幼圆", 14)).grid(row=5, column=8)

    def run(self):  # 调用机器学习的结果，并将结果可视化
        model = simulate("test.result")
        flag1 = 0
        if self.choose.get() == 0:
            seq = self.seq.get(0.0, END)
            if len(seq) <= 61:
                mb.showerror("错误", "请输入至少61bp的DNA序列！")
            else:
                model.getStr(seq)
                flag1 = 1
        else:
            path = self.filePath.get()
            if path == "":
                mb.showerror("错误", "请选择文件！")
            else:
                model.getFile(path)
                flag1 = 1

        if flag1:
            li = model.getResult()
            result = Toplevel(self.root)
            result.title("预测结果")
            c = Canvas(result, width=600, height=800)
            c.pack()
            y = 800/(2+len(li)/500)
            x = 50
            for i in range(len(li)):
                if li[i] == 0:
                    c.create_line(x, y, x+1, y, width=5, fill='gray')
                if li[i] == 1:
                    c.create_line(x, y, x+1, y, width=5, fill='red')
                if li[i] == 2:
                    c.create_line(x, y, x+1, y, width=5, fill='blue')
                if i % 500 == 0:
                    c.create_text(x, y, text="%d" %
                                  (i+1), anchor=NE, font=("幼圆", 10))
                if i % 500 == 499 or i+1 == len(li):
                    c.create_text(x, y, text="%d" %
                                  (i+1), anchor=NW, font=("幼圆", 10))
                    x = 50
                    y += 800/(2+len(li)/500)
                else:
                    x = x+1

            result.update_idletasks()
            result.geometry('600x800+%d+%d' % ((result.winfo_screenwidth() -
                                                result.winfo_width())/2, (result.winfo_screenheight()-50-result.winfo_height())/2))

    def quit(self):  # 关闭窗口功能函数
        self.root.quit()
        self.root.destroy()
