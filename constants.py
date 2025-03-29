# -*- coding: utf-8 -*-
"""
@File    :   constants.py
@Time    :   2025/03/20 13:29:03
@Author  :   xuanyabulema@qq.com
@Version :
@Desc    :
"""
import numpy as np

CONSTANTS = {
    "i_0": 1e-10,  # 正向饱和电流 (A)
    "n": 1.152525,  # 正向理想因子
    "T": 300,  # 温度 (K)
    "q": 1.602e-19,  # 电子电荷量 (C)
    "k": 1.38e-23,  # 玻尔兹曼常数 (J/K)
}

VOLTAGE_RANGE = (-10, 0.75)
VOLTAGE_POINTS = 2000

PLOT_HEIGHT = 300
PLOT_WIDTH = 600
X_RANGE = (-0.9, 1.8)
Y_RANGE = (-2, 24)

INITIAL_ALPHA_SHADED = 0.5
INITIAL_ALPHA_UNSHADED = 1
INITIAL_I_0_P = 1

CELL_COUNT = 24
SHADED_CELL_COUNT = 1
UNSHADED_CELL_COUNT = CELL_COUNT - SHADED_CELL_COUNT

GROUP_COUNT = 3
SHADED_GROUP_COUNT = 1
UNSHADED_GROUP_COUNT = GROUP_COUNT - SHADED_GROUP_COUNT


v_oc = 0.745
i_0 = CONSTANTS["i_0"]
n = CONSTANTS["n"]
T = CONSTANTS["T"]
q = CONSTANTS["q"]
k = CONSTANTS["k"]

# 生成电压数组
v = np.linspace(*VOLTAGE_RANGE, VOLTAGE_POINTS)

# 计算反向理想因子
n_p = q / (k * T)

# 计算开路电压和短路电流
i_sc = i_0 * (np.exp(q * v_oc / (n * k * T)) - 1)
i_l = i_sc
INITIAL_I_L = i_l
