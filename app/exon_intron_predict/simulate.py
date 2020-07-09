"""
作者：谢乐凡
修改者：叶佳晨
"""
from __future__ import division

import math
import tkinter.messagebox as mb

flag = {0: 1,
        1: 2,
        2: 0}

# 生成大小 I*J 的矩阵，默认零矩阵


def makeMatrix(I, J, fill=0.0):
    m = []
    for i in range(I):
        m.append([fill] * J)
    return m

# 函数 sigmoid


def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


class simulate:
    """ 三层反向传播神经网络 """

    def __init__(self, filename):
        # 输入层、隐藏层、输出层的节点（数）
        self.ni = 60 + 1  # 增加一个偏差节点
        self.nh = 100 + 1
        self.no = 3

        # 激活神经网络的所有节点（向量）
        self.ai = [1.0] * self.ni
        self.ah = [1.0] * self.nh
        self.ao = [1.0] * self.no

        # 建立权重（矩阵）
        self.wi = makeMatrix(self.ni, self.nh)
        self.wo = makeMatrix(self.nh, self.no)

        f = open(filename, 'r', encoding='UTF-8')
        while True:
            get = f.readline()
            if get[0] == "输":
                break
        for i in range(self.ni):
            line = f.readline()
            get = line[1:len(line)-2]
            num = get.split(",")
            for j in range(len(num)):
                self.wi[i][j] = float(num[j])
        while True:
            get = f.readline()
            if get[0] == "输":
                break
        for i in range(self.nh):
            line = f.readline()
            get = line[1:len(line)-2]
            num = get.split(",")
            for j in range(len(num)):
                self.wo[i][j] = float(num[j])

    def update(self, inputs):
        if len(inputs) != self.ni - 1:
            raise ValueError('与输入层节点数不符！')
        # 激活输入层
        for i in range(self.ni - 1):
            self.ai[i] = inputs[i]
        # 激活隐藏层
        for j in range(self.nh):
            sum = 0.0
            for i in range(self.ni):
                sum = sum + self.ai[i] * self.wi[i][j]
            self.ah[j] = sigmoid(sum)
        # 激活输出层
        for k in range(self.no):
            sum = 0.0
            for j in range(self.nh):
                sum = sum + self.ah[j] * self.wo[j][k]
            self.ao[k] = sigmoid(sum)

        return self.ao[:]

    def getFile(self, filename):
        f = open(filename, "r", encoding='UTF-8')
        get = f.readline()
        get = f.read()
        self.seq = get.replace("\n", "")

    def getStr(self, s):
        self.seq = s.replace("\n", "")
        self.seq = self.seq.replace("\t", "")
        self.seq = self.seq.replace(" ", "")
        self.seq = self.seq.upper()
        num = self.seq.count("A")+self.seq.count("C") + \
            self.seq.count("G")+self.seq.count("T")
        if num != len(self.seq):
            mb.showwarning("警告", "序列中包含了AaGgCcTt以外的字符")

    def getResult(self):
        feature = []
        num = 0
        for i in self.seq:
            if i == 'A':
                num = 0
            if i == 'G':
                num = 1
            if i == 'C':
                num = 2
            if i == 'T':
                num = 3
            feature.append(num)

        li = []
        for i in range(len(self.seq)-60):
            test = feature[i: i+60]
            result = self.update(test)
            index = result.index(max(result))
            li.append(flag[index])

        return li
