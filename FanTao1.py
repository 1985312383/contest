import csv
import re
import numpy as np
from matplotlib import pyplot as plt

thre = 1.7  # 要调整的参数,这个是阈值
iteration_num = 2  # 要调整的参数，这个是迭代次数

'''
清洗数据
'''
def cleanData(kind):
    for k in range(1, 325):
        with open(f"./data/附件1：UWB数据集/{kind}数据/{k}.{kind}.txt", "r") as f:  # 打开文件
            f.readline()  # 去掉第一行
            data = f.readlines()  # 读取文件

        f.close()

        data_num = len(data) / 4
        if int(data_num) - data_num < -0.1:
            raise ValueError("数据数量不对!")

        initial_time = re.search(":.*:([0-9]*)", data[0], flags=0)  # 获取初始数据序列
        initial_time = int(initial_time.group(1))

        Measures = []
        for i in range(int(data_num)):
            measure = []
            for j in range(4):
                device = []
                anchor = re.search(":[0-9]*?:RR:0:([0-9]):[0-9]*?:([0-9]*?):[0-9]*?:([0-9]*)", data[4 * i + j], flags=0)
                device.extend([int(anchor.group(3)) - initial_time, anchor.group(1), anchor.group(2)])  # 获取数据序号、设备号、测量值
                device = list(map(int, device))
                measure.append(device)  # 一个measure就是四个设备拿到的四份数据
            Measures.append(measure)
        Measures = np.array(Measures)  # Measures是三维数组是获取的所有测量数据

        # 注意newline
        with open(f"cleaned_data/{kind}数据/{k}.{kind}.csv", "w+", newline="") as datacsv:
            # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
            csvwriter = csv.writer(datacsv, dialect=("excel"))
            # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
            csvwriter.writerow(["数据序列", "设备号", "测量值"])
            for i in range(len(Measures)):
                csvwriter.writerows(Measures[i])

        datacsv.close()

        normalized_device_data = []
        normalized_device_data_x = []
        device_data = []
        device_data_x = []
        for i in range(4):
            device_data.append(Measures[:, i, 2])
            device_data_x.append(np.arange(len(Measures[:, i, 2])))
            normalized_device_data.append(device_data[i] / np.max(Measures[:, i, 2]))  # 最大值归一化
        normalized_device_data_x = device_data_x

        '''
        画图，在每一组数据中，循环清洗数据时请勿取消注释
        '''
        # try:
        #     plt.figure()
        #     plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
        #     plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        #     plt.title(u"4个UWB锚点在正常环境下的数据图(未滤波)")
        #     plt.xlabel(u"数据序号")
        #     plt.ylabel(u"归一化后的测量值")
        #
        #     normalized_device_data = np.array(normalized_device_data)
        #     normalized_device_data_x = np.array(normalized_device_data_x)
        #     device_data = np.array(device_data)
        #     device_data_x = np.array(device_data_x)
        #
        #     for i in range(4):
        #         # plt.plot(np.array(normalized_device_data_x[i,:]), np.array(normalized_device_data[i,:]),label=u"UWB锚点"+str(i))\
        #         plt.plot(np.array(device_data_x[i, :]), np.array(device_data[i, :]), label=u"UWB锚点" + str(i))
        #         plt.legend(loc="lower right")
        #
        #     plt.figure(2)
        #     plt.title(u"4个UWB锚点在正常环境下的数据图(已滤波)")
        #     plt.xlabel(u"数据序号")
        #     plt.ylabel(u"归一化后的测量值")
        #     device_mean = np.mean(device_data, axis=1)
        #     device_std = np.std(device_data, axis=1)
        #
        #     low_thre = device_mean - device_std * thre
        #     high_thre = device_mean + device_std * thre
        #
        #     for _ in range(iteration_num):
        #         for i in range(4):
        #             for j in range(len(device_data[i, :])):
        #                 if device_data[i, j] < low_thre[i] or device_data[i, j] > high_thre[i]:
        #                     device_data[i, j] = device_mean[i]
        #
        #     for i in range(4):
        #         # plt.plot(np.array(device_data_x[i,:]), np.array(device_data[i,:]/np.max(device_data[i,:])),label=u"UWB锚点"+str(i))
        #         plt.plot(np.array(device_data_x[i, :]), np.array(device_data[i, :]),
        #                  label=u"UWB锚点" + str(i))
        #         plt.legend(loc="lower right")
        #     plt.show()
        #     plt.pause()
        # except:
        #     pass


if __name__ == '__main__':
    cleanData("正常")
    cleanData("异常")