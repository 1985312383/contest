# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import root
import pandas as pd
import csv

global d0, d1, d2, d3  # 即 A0,A1,A2,A3的测量值

# 设置坐标
len_x = 5000
len_y = 5000
len_z = 3000
x_mid = len_x/2
y_mid = len_y/2
z_mid = len_z/2
A0_z = 1300
A1_z = 1700
A2_z = 1700
A3_z = 1300

def A0_A1_A2_Positioning(Tag):
    x, y, z = Tag[0], Tag[1], Tag[2]
    return [
        (x - 0) ** 2 + (y - 0) ** 2 + (z - A0_z) ** 2 - d0 ** 2,  # A0距离约束
        (x - len_x) ** 2 + (y - 0) ** 2 + (z - A1_z) ** 2 - d1 ** 2,  # A1距离约束
        (x - 0) ** 2 + (y - len_y) ** 2 + (z - A2_z) ** 2 - d2 ** 2,  # A2距离约束
    ]


def A0_A1_A3_Positioning(Tag):
    x, y, z = Tag[0], Tag[1], Tag[2]
    return [
        (x - 0) ** 2 + (y - 0) ** 2 + (z - A0_z) ** 2 - d0 ** 2,  # A0距离约束
        (x - len_x) ** 2 + (y - 0) ** 2 + (z - A1_z) ** 2 - d1 ** 2,  # A1距离约束
        (x - len_x) ** 2 + (y - len_y) ** 2 + (z - A3_z) ** 2 - d3 ** 2,  # A3距离约束
    ]


def A0_A2_A3_Positioning(Tag):
    x, y, z = Tag[0], Tag[1], Tag[2]
    return [
        (x - 0) ** 2 + (y - 0) ** 2 + (z - A0_z) ** 2 - d0 ** 2,  # A0距离约束
        (x - 0) ** 2 + (y - len_y) ** 2 + (z - A2_z) ** 2 - d2 ** 2,  # A2距离约束
        (x - len_x) ** 2 + (y - len_y) ** 2 + (z - A3_z) ** 2 - d3 ** 2,  # A3距离约束
    ]


def A1_A2_A3_Positioning(Tag):
    x, y, z = Tag[0], Tag[1], Tag[2]
    return [
        (x - 5000) ** 2 + (y - 0) ** 2 + (z - A1_z) ** 2 - d1 ** 2,  # A1距离约束
        (x - 0) ** 2 + (y - len_y) ** 2 + (z - A2_z) ** 2 - d2 ** 2,  # A2距离约束
        (x - len_x) ** 2 + (y - len_y) ** 2 + (z - A3_z) ** 2 - d3 ** 2,  # A3距离约束
    ]


def read_predict_data(file_path):
    data = pd.read_csv(file_path, encoding="gbk")
    data = data.drop(columns=data.columns[0])
    lable = data.diff()
    lable = lable.drop(index=lable.index[0])
    lable = lable.drop(index=lable.index[0])
    lable = np.array(lable)
    lable = np.absolute(lable)
    lable = np.amax(lable, axis=0)

    last_distance = data.iloc[-1]
    last_distance = np.array(last_distance)
    global d0, d1, d2, d3
    d0, d1, d2, d3 = last_distance  # 获取最后一行的A0-A3

    tag = []
    if np.sum(lable > 10) == 1:
        if lable[0] > 10:
            tag.append(root(A1_A2_A3_Positioning, [x_mid, y_mid, len_z]).x)
        elif lable[1] > 10:
            tag.append(root(A0_A2_A3_Positioning, [x_mid, y_mid, len_z]).x)
        elif lable[2] > 10:
            tag.append(root(A0_A1_A3_Positioning, [x_mid, y_mid, len_z]).x)
        elif lable[3] > 10:
            tag.append(root(A0_A1_A2_Positioning, [x_mid, y_mid, len_z]).x)
    elif np.sum(lable > 10) > 1:
        if lable[0] > 10:
            tag.append(root(A1_A2_A3_Positioning, [x_mid, y_mid, len_z]).x)
        if lable[1] > 10:
            tag.append(root(A0_A2_A3_Positioning, [x_mid, y_mid, len_z]).x)
        if lable[2] > 10:
            tag.append(root(A0_A1_A3_Positioning, [x_mid, y_mid, len_z]).x)
        if lable[3] > 10:
            tag.append(root(A0_A1_A2_Positioning, [x_mid, y_mid, len_z]).x)

    tag = np.array(tag)
    if len(tag) > 1:
        for i in range(len(tag) - 1):
            if (tag[i][0] > len_x) or (tag[i][0] < 0):
                tag = np.delete(tag, obj=i, axis=0)
    if len(tag) > 1:
        for i in range(len(tag) - 1):
            if tag[i][1] > len_y or tag[i][1] < 0:
                tag = np.delete(tag, obj=i, axis=0)
    if len(tag) > 1:
        for i in range(len(tag) - 1):
            if tag[i][2] > len_z or tag[i][2] < 0:
                tag = np.delete(tag, obj=i, axis=0)
    # print(tag)
    return np.array(tag)


def clustering_4_tag_position(cluster_tag):
    pass


def read_label(file_path):
    pass


def tag_check(cluster_tag, predicted_tag, actual_tag):
    pass


thre = 1.5  # 要调整的参数,这个是阈值
iteration_num = 2  # 要调整的参数，这个是迭代次数

'''
for _ in range(iteration_num):
    for i in range(4):
        for j in range(len(device_data[i, :])):
            if device_data[i, j] < low_thre[i] or device_data[i, j] > high_thre[i]:
                processed_device_data[i, j] = device_mean[i]
'''


def getData(kind):
    with open("submit/task2/abnormal_data.csv", "w+", newline="") as datacsv:
        # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
        csvwriter.writerow(["Number", "x1", "y1", "z1", "x", "y", "z", "xyz_error", "xy_error", "xz_error", "yz_error", "x_error", "y_error", "z_error"])

        correct_tag_position = pd.read_table("data/附件1：UWB数据集/Tag坐标信息.txt", delim_whitespace=True)  # 打开文件
        correct_tag_position = np.array(correct_tag_position.drop(columns=correct_tag_position.columns[0]))

        for index in range(1, 325):
            # data = pd.read_csv(f"cleaned_data/{kind}数据/{i}.{kind}.csv")
            # last_line = np.array(data.tail(1))
            cluster_tag = np.array(read_predict_data(f"cleaned_data/{kind}数据/{index}.{kind}.csv"))  # 产生2-4个可行点，用于聚类
            # cluster_tag_mean = cluster_tag.mean(axis=0)
            # cluster_tag_std = cluster_tag.std(axis=0)
            # low_thre = cluster_tag_mean - cluster_tag_std * thre  # 去除离群点
            # high_thre = cluster_tag_mean + cluster_tag_std * thre  # 去除离群点
            # for _ in range(iteration_num):
            #     for i in range(4):
            #         for j in range(3):
            #             if cluster_tag[i, j] < low_thre[j] or cluster_tag[i, j] > high_thre[j]:
            #                 cluster_tag[i, j] = cluster_tag_mean[j]

            predicted_tag = np.around(cluster_tag.mean(axis=0) / 10.0, 2)

            result = np.append(index, np.append(predicted_tag.T, np.array(correct_tag_position[index - 1])))
            result = np.append(result,calculate_3D_error(result[1],result[2],result[3],result[4],result[5],result[6]))
            result = np.append(result,calculate_2D_error(result[1],result[2],result[4],result[5]))
            result = np.append(result, calculate_2D_error(result[1],result[3],result[4],result[6]))
            result = np.append(result, calculate_2D_error(result[2], result[3], result[5], result[6]))
            result = np.append(result, calculate_1D_error(result[1],result[4]))
            result = np.append(result, calculate_1D_error(result[2], result[5]))
            result = np.append(result, calculate_1D_error(result[3], result[6]))
            result = np.around(result, 2)
            csvwriter.writerow(result)


def test(D0, D1, D2, D3):
    global d0, d1, d2, d3
    d0, d1, d2, d3 = D0, D1, D2, D3  # 获取最后一行的A0-A3

    tag = []
    tag.append(root(A0_A1_A2_Positioning, [x_mid, y_mid, len_z]).x)  # 初始点选了4个anchor的中点
    tag.append(root(A0_A1_A3_Positioning, [x_mid, y_mid, len_z]).x)  # 初始点选了4个anchor的中点
    tag.append(root(A0_A2_A3_Positioning, [x_mid, y_mid, len_z]).x)  # 初始点选了4个anchor的中点
    tag.append(root(A1_A2_A3_Positioning, [x_mid, y_mid, len_z]).x)  # 初始点选了4个anchor的中点

    tag = np.array(tag)
    if len(tag) > 1:
        for i in range(len(tag) - 1):
            if (tag[i][0] > len_x) or (tag[i][0] < 0):
                tag = np.delete(tag, obj=i, axis=0)
    if len(tag) > 1:
        for i in range(len(tag) - 1):
            if tag[i][1] > len_y or tag[i][1] < 0:
                tag = np.delete(tag, obj=i, axis=0)
    if len(tag) > 1:
        for i in range(len(tag) - 1):
            if tag[i][2] > len_z or tag[i][2] < 0:
                tag = np.delete(tag, obj=i, axis=0)

    tag = np.around(tag.mean(axis=0) / 10.0, 2)
    # print(tag)
    return np.array(tag)


def calculate_3D_error(x1, y1, z1, x, y, z):
    return (x1 - x) ** 2 + (y1 - y) ** 2 + (z1 - z) ** 2

def calculate_2D_error(x1, y1,  x, y):
    return (x1 - x) ** 2 + (y1 - y) ** 2

def calculate_1D_error(x1,  x):
    return abs(x1-x)

if __name__ == '__main__':
    getData("异常")

    # 计算测试数据只需注释getdata，赋值最开始的d0,d1,d2,d3即可，然后运行test
    # print(test(1620,3950,2580,4440))

    #计算各维度的平均误差，单位cm，计算数据时请注释
    # error = pd.read_csv("submit/task2/abnormal_data.csv")
    # error = np.array(error)
    # average_error = error.mean(axis=0)
    # average_error = np.around(average_error, 2)
    # for i in range(7, 14):
    #     print(average_error[i])

    breakpoint()
