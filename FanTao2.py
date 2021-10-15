
# -*- coding: utf-8 -*-

import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split  # 数据集的分割函数
from sklearn.preprocessing import StandardScaler  # 数据预处理
from sklearn import metrics
import pandas as pd
from sklearn.utils import shuffle
import matplotlib.pyplot as plt

# 四个锚点坐标
A0 = [0, 0, 1300]
A1 = [5000, 0, 1700]
A2 = [0, 5000, 1700]
A3 = [5000, 5000, 1300]

class RELM_HiddenLayer:
    """
        正则化的极限学习机
        :param x: 初始化学习机时的训练集属性X
        :param num: 学习机隐层节点数
        :param C: 正则化系数的倒数
    """
    def __init__(self, x, num, C=10):
        row = x.shape[0]
        columns = x.shape[1]
        rnd = np.random.RandomState()

        # 权重w
        self.w = rnd.uniform(-1, 1, (columns, num))

        # 偏置b
        self.b = np.zeros([row, num], dtype=float)

        for i in range(num):
            rand_b = rnd.uniform(-0.4, 0.4)
            for j in range(row):
                self.b[j, i] = rand_b

        self.H0 = np.matrix(self.sigmoid(np.dot(x, self.w) + self.b))
        self.C = C
        self.P = (self.H0.H * self.H0 + len(x) / self.C).I
        # .T:共轭矩阵,.H:共轭转置,.I:逆矩阵

    @staticmethod
    def sigmoid(x):
        """
            激活函数sigmoid
            :param x: 训练集中的X
            :return: 激活值
        """
        return 1.0 / (1 + np.exp(-x))

    @staticmethod
    def softplus(x):
        """
            激活函数 softplus
            :param x: 训练集中的X
            :return: 激活值
        """
        return np.log(1 + np.exp(x))

    @staticmethod
    def tanh(x):
        """
            激活函数tanh
            :param x: 训练集中的X
            :return: 激活值
        """
        return (np.exp(x) - np.exp(-x)) / (np.exp(x) + np.exp(-x))

    # 回归问题 训练
    def regressor_train(self, T):
        """
            初始化了学习机后需要传入对应标签T
            :param T: 对应属性X的标签T
            :return: 隐层输出权值beta
        """
        #       all_m = np.dot(self.P, self.H0.H)
        #       self.beta = np.dot(all_m, T)
        #       return self.beta
        all_m = np.dot(self.P, self.H0.H)
        self.beta = np.dot(all_m, T)
        return self.beta
    # 回归问题 测试
    def regressor_test(self, test_x):
        """
            传入待预测的属性X并进行预测获得预测值
            :param test_x:被预测标签的属性X
            :return: 被预测标签的预测值T
        """
        b_row = test_x.shape[0]
        h = self.sigmoid(np.dot(test_x, self.w) + self.b[:b_row, :])
        #     h = self.sigmoid(np.dot(test_x, self.w) + self.b[:b_row, :])
        result = np.dot(h, self.beta)
        #       result =np.argmax(result,axis=1)
        return result


# In[]

# 数据读取及划分
url = 'cleaned_data/正常数据/1.正常.csv'
data = pd.read_csv(url, sep=',', header='infer')
data = np.array(data)
print(data)
data = shuffle(data)
X_data = data[:, :23]
Y = data[:, 23:26]
print(Y)

# Y=np.array(Y).reshape(-1, 1)
# print(Y)
# labels=np.asarray(pd.get_dummies(Y),dtype=np.int32)
# asarray是将输入数据（get_dummies）转换为矩阵形式
# what=pd.get_dummies(Y)
# get_dummies是将数据分成类，然后每一个数据，对应分类结果上写1，其他都是0
# print(what)

# 下面3行代码就是将数据集随即按照num_train分成训练集和测试集，数据量大，就分了两部分

num_train = 0.1
X_train, X_, Y_train, Y_ = train_test_split(X_data, Y, test_size=num_train, random_state=20)
X_test, X_vld, Y_test, Y_vld = train_test_split(X_, Y_, test_size=0.1, random_state=20)

# In[]

# 数据标准化处理
stdsc = StandardScaler()
X_train = stdsc.fit_transform(X_train)
X_test = stdsc.fit_transform(X_test)
X_vld = stdsc.fit_transform(X_vld)
Y_true = Y_test
# Y_true=np.argmax(Y_test,axis=1)


# In[]

# 不同隐藏层结果对比

result = []

for j in range(1, 30, 5):
    a = RELM_HiddenLayer(X_train, j)
    a.regressor_train(Y_train)
    num_data = len(X_test)
    predict = a.regressor_test(X_test)
    print(predict)

    #    acc=metrics.precision_score(predict,Y_true, average='macro')
    #    plt.scatter(2,4,s=200)

    for i in range(1, num_data, 1):
        print('hidden- %d,predict1：%f,predict2：%f,predict3：%f' % (j, predict[i, 0], predict[i, 1], predict[i, 2]))

    # print(predict[i])
    # plt.scatter(i,predict[i].tolist())
#    plt.plot(i, predict[i],linewidth=5)
# plt.show()
#    result.append(pre)
#    print('hidden- %d,acc：%f'%(j,acc))
