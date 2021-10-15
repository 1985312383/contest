# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import root
import pandas as pd
import csv

global d0, d1, d2, d3  # 即 A0,A1,A2,A3的测量值


def A0_A1_A2_Positioning(Tag):
    x, y, z = Tag[0], Tag[1], Tag[2]
    return [
        (x - 0) ** 2 + (y - 0) ** 2 + (z - 1300) ** 2 - d0 ** 2,  # A0距离约束
        (x - 5000) ** 2 + (y - 0) ** 2 + (z - 1700) ** 2 - d1 ** 2,  # A1距离约束
        (x - 0) ** 2 + (y - 5000) ** 2 + (z - 1700) ** 2 - d2 ** 2,  # A2距离约束
    ]


def A0_A1_A3_Positioning(Tag):
    x, y, z = Tag[0], Tag[1], Tag[2]
    return [
        (x - 0) ** 2 + (y - 0) ** 2 + (z - 1300) ** 2 - d0 ** 2,  # A0距离约束
        (x - 5000) ** 2 + (y - 0) ** 2 + (z - 1700) ** 2 - d1 ** 2,  # A1距离约束
        (x - 5000) ** 2 + (y - 5000) ** 2 + (z - 1300) ** 2 - d3 ** 2,  # A3距离约束
    ]


def A0_A2_A3_Positioning(Tag):
    x, y, z = Tag[0], Tag[1], Tag[2]
    return [
        (x - 0) ** 2 + (y - 0) ** 2 + (z - 1300) ** 2 - d0 ** 2,  # A0距离约束
        (x - 0) ** 2 + (y - 5000) ** 2 + (z - 1700) ** 2 - d2 ** 2,  # A2距离约束
        (x - 5000) ** 2 + (y - 5000) ** 2 + (z - 1300) ** 2 - d3 ** 2,  # A3距离约束
    ]


def A1_A2_A3_Positioning(Tag):
    x, y, z = Tag[0], Tag[1], Tag[2]
    return [
        (x - 5000) ** 2 + (y - 0) ** 2 + (z - 1700) ** 2 - d1 ** 2,  # A1距离约束
        (x - 0) ** 2 + (y - 5000) ** 2 + (z - 1700) ** 2 - d2 ** 2,  # A2距离约束
        (x - 5000) ** 2 + (y - 5000) ** 2 + (z - 1300) ** 2 - d3 ** 2,  # A3距离约束
    ]


def read_last_data(file_path):
    data = pd.read_csv(file_path, encoding="gbk")
    last_distance = data.iloc[-1]
    last_distance = np.array(last_distance)
    global d0, d1, d2, d3
    d0, d1, d2, d3 = last_distance[1:5]  # 获取最后一行的A0-A3


def calculate_4_tag_position():
    tag = []
    tag.append(root(A0_A1_A2_Positioning, [2500, 2500, 1500]).x)  # 初始点选了4个anchor的中点
    tag.append(root(A0_A1_A3_Positioning, [2500, 2500, 1500]).x)  # 初始点选了4个anchor的中点
    tag.append(root(A0_A2_A3_Positioning, [2500, 2500, 1500]).x)  # 初始点选了4个anchor的中点
    tag.append(root(A1_A2_A3_Positioning, [2500, 2500, 1500]).x)  # 初始点选了4个anchor的中点
    return tag


def clustering_4_tag_position(cluster_tag):
    pass


def read_label(file_path):
    pass


def tag_check(cluster_tag, predicted_tag, actual_tag):
    pass


def getData(kind):
    with open("submit/task2/right_data.csv", "w+", newline="") as datacsv:
        # dialect为打开csv文件的方式，默认是excel，delimiter="\t"参数指写入的时候的分隔符
        csvwriter = csv.writer(datacsv, dialect=("excel"))
        # csv文件插入一行数据，把下面列表中的每一项放入一个单元格（可以用循环插入多行）
        csvwriter.writerow(["Number", "x1", "y1", "z1", "x", "y", "z"])

        f = pd.read_table("data/附件1：UWB数据集/Tag坐标信息.txt", delim_whitespace=True)  # 打开文件
        f = np.array(f.drop(columns=f.columns[0]))

        for i in range(1, 325):
            # data = pd.read_csv(f"cleaned_data/{kind}数据/{i}.{kind}.csv")
            # last_line = np.array(data.tail(1))
            read_last_data(f"cleaned_data/{kind}数据/{i}.{kind}.csv")
            cluster_tag = np.array(calculate_4_tag_position())  # 产生4个可行点，用于聚类
            predicted_tag = np.around(np.array(np.sum(cluster_tag, axis=0) / 40.0), 2)

            result = np.append(i, np.append(np.array(predicted_tag.T), np.array(f[i - 1])))
            csvwriter.writerow(result)


if __name__ == '__main__':
    getData("正常")
    breakpoint()
