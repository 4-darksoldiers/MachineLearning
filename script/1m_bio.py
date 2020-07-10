from __future__ import division
import math
import random
import pandas as pd
import requests



flowerLables = {0: 'EI',
                1: 'IE',
                2: 'N'}

random.seed(0)


# 生成区间[a, b)内的随机数
def rand(a, b):
    return (b - a) * random.random() + a


# 生成大小 I*J 的矩阵，默认零矩阵
def makeMatrix(I, J, fill=0.0):
    m = []
    for i in range(I):
        m.append([fill] * J)
    return m


# 函数 sigmoid
def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))


# 函数 sigmoid 的导数
def dsigmoid(x):
    return x * (1 - x)

def getKmers(sequence, size):
    return [0.00001*float(int(sequence[x:x+size].replace('A','0').replace('C','1').replace('G','2').replace('T','3').replace('N','4').replace('D','5').replace('R','6').replace('S','7'), base = 8)) for x in range(len(sequence) - size + 1)]
    
class NN:
    """ 三层反向传播神经网络 """

    def __init__(self, ni, nh, no):
        # 输入层、隐藏层、输出层的节点（数）
        self.ni = ni + 1  # 增加一个偏差节点
        self.nh = nh + 1
        self.no = no

        # 激活神经网络的所有节点（向量）
        self.ai = [1.0] * self.ni
        self.ah = [1.0] * self.nh
        self.ao = [1.0] * self.no

        # 建立权重（矩阵）
        self.wi = makeMatrix(self.ni, self.nh)
        self.wo = makeMatrix(self.nh, self.no)
        # 设为随机值
        for i in range(self.ni):
            for j in range(self.nh):
                self.wi[i][j] = rand(-0.2, 0.2)
        for j in range(self.nh):
            for k in range(self.no):
                self.wo[j][k] = rand(-2, 2)

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

    def backPropagate(self, targets, lr):
        """ 反向传播 """

        # 计算输出层的误差
        output_deltas = [0.0] * self.no
        for k in range(self.no):
            error = targets[k] - self.ao[k]
            output_deltas[k] = dsigmoid(self.ao[k]) * error

        # 计算隐藏层的误差
        hidden_deltas = [0.0] * self.nh
        for j in range(self.nh):
            error = 0.0
            for k in range(self.no):
                error = error + output_deltas[k] * self.wo[j][k]
            hidden_deltas[j] = dsigmoid(self.ah[j]) * error

        # 更新输出层权重
        for j in range(self.nh):
            for k in range(self.no):
                change = output_deltas[k] * self.ah[j]
                self.wo[j][k] = self.wo[j][k] + lr * change         #学习速率lr的影响

        # 更新输入层权重
        for i in range(self.ni):
            for j in range(self.nh):
                change = hidden_deltas[j] * self.ai[i]
                self.wi[i][j] = self.wi[i][j] + lr * change

        # 计算误差
        error = 0.0
        error += 0.5 * (targets[k] - self.ao[k]) ** 2
        return error  #梯度下降检验没看到

    def test(self, patterns):
        count = 0
        for p in patterns:
            target = flowerLables[(p[1].index(1))]   #花的类型
            result = self.update(p[0])
            index = result.index(max(result))        
            print(p[0], ':', target, '->', flowerLables[index])
            count += (target == flowerLables[index])
        accuracy = float(count / len(patterns))
        print('accuracy: %-.9f' % accuracy)

    def weights(self):
        print('输入层权重:')
        for i in range(self.ni):
            print(self.wi[i])
        print()
        print('输出层权重:')
        for j in range(self.nh):
            print(self.wo[j])

    def outputs(self):
        f=open('weight.txt','w')
        for i in range(self.ni):
            f.write(str(self.wi[i]))
            f.write("\n")
        f.write("out\n")
        for i in range(self.nh):
            r.write(str(self.wo[i]))
            f.write("\n")
        f.write("\n")
        f.close()

    def train(self, patterns, iterations=1000, lr=0.1):
        # lr: 学习速率(learning rate)
        for i in range(iterations):
            error = 0.0
            for p in patterns:
                inputs = p[0]
                targets = p[1]
                self.update(inputs)
                error = error + self.backPropagate(targets, lr)
            if i % 100 == 0:                    #迭代达到100次倍数
                print('error: %-.9f' % error)



def iris():
    data = []
    # 读取数据
    raw = pd.read_csv('splice.data')
    raw_data = raw.values
    raw_feature = raw_data[0:,2:3]
    for i in range(len(raw_feature)):
        ele = []
        ele.append(getKmers(raw_feature[i][0].strip(),6))
        if raw_data[i][0] == 'EI':
            ele.append([1, 0, 0])
        elif raw_data[i][0] == 'IE':
            ele.append([0, 1, 0])
        else:
            ele.append([0, 0, 1])
        data.append(ele)
    # 随机排列数据
    random.shuffle(data)
    training = data[0:2000]
    test = data[2001:3190]
    nn = NN(55, 100, 3)          #输入层 隐藏层（层数对准确率似乎无影响） 输出层
    nn.train(training, iterations=10000)
    nn.test(test)


if __name__ == '__main__':
    iris()
