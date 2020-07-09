"""
本文件是DNA外显子/内含子预测程序的主程序源代码
版本：1.5   （个位数代表一次大改动，小数代表一次小改动，其他文件相同）
作者：叶佳晨
最后一次修改时间：2020/07/07
更具体的功能、算法介绍请见报告
"""
from DNA_predict import ExonIntron_predict


def main():
    myApp = ExonIntron_predict()  # 类的实例化，调用类的初始化方法__init__函数


main()
