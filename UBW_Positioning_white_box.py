# -*- coding: utf-8 -*-
import numpy as np
from scipy.optimize import fsolve
import pandas as pd

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
    d0, d1, d2, d3 = last_distance[1:5]


def calculate_4_tag_position():
    tag = []
    tag.append(fsolve(A0_A1_A2_Positioning, [2500, 2500, 1500]))  # 初始点选了4个anchor的中点
    tag.append(fsolve(A0_A1_A3_Positioning, [2500, 2500, 1500]))  # 初始点选了4个anchor的中点
    tag.append(fsolve(A0_A2_A3_Positioning, [2500, 2500, 1500]))  # 初始点选了4个anchor的中点
    tag.append(fsolve(A1_A2_A3_Positioning, [2500, 2500, 1500]))  # 初始点选了4个anchor的中点
    return tag


def clustering_4_tag_position(cluster_tag):
    pass


def read_label(file_path):
    pass


def tag_check(cluster_tag, predicted_tag, actual_tag):
    pass


if __name__ == '__main__':
    read_last_data("./附件1：UWB数据集/dataset/normal_data/24.normal.csv")
    cluster_tag = np.array(calculate_4_tag_position())  # 产生4个可行点，用于聚类
    predicted_tag = cluster_tag.sum(axis=0) / 4.0
    breakpoint()
