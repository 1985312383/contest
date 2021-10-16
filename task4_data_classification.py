import numpy as np
import pandas as pd
from task1_plotFourPictures import data_process, clean_similar_data

def get_dissimilar_data_mean_std(file_path):
    data = pd.read_csv(file_path,usecols=[1],encoding="gbk")
    the_number_of_data = np.array(data).reshape(-1)
    return the_number_of_data.mean(), the_number_of_data.std()

if __name__ == '__main__':
    the_number_of_normal_data_mean,the_number_of_normal_data_std = get_dissimilar_data_mean_std(
        "./submit/task1/正常数据/清洗后的正常数据的数据数量.csv")
    the_number_of_abnormal_data_mean,the_number_of_abnormal_data_std = get_dissimilar_data_mean_std(
        "./submit/task1/异常数据/清洗后的异常数据的数据数量.csv")
    proceessed_test_data = data_process("./data/附件4：测试集（实验场景1）")
    breakpoint()
