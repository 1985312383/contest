import pandas as pd
import numpy as np

f = pd.read_table("data/附件1：UWB数据集/Tag坐标信息.txt", delim_whitespace=True)  # 打开文件
f = np.array(f.drop(columns=f.columns[0]))
f = f[0]
breakpoint()