# -*- coding: utf-8 -*-
"""
@File    :   bc_model.py
@Time    :   2025/03/20 13:29:09
@Author  :   xuanyabulema@qq.com
@Version :
@Desc    :
"""

import numpy as np

def get_bc_current(v, i_0, i_0_p, n, n_p, k, T, q, i_l, alpha):
    """
    计算BC模型的电流-电压关系

    参数:
        v: 电压数组 (V)
        i_0: 正向饱和电流 (A)
        i_0_p: 反向隧穿饱和电流 (A)
        n: 正向理想因子
        n_p: 反向隧穿理想因子
        k: 玻尔兹曼常数 (J/K)
        T: 温度 (K)
        q: 电子电荷量 (C)
        i_l: 光生电流 (A)
        alpha: 未遮挡比例 (0≤α≤1)

    返回:
        电流数组 (A)
    """
    i = np.zeros_like(v)

    # 正向偏压区 (V≥0)
    mask_forward = v >= 0
    i[mask_forward] = alpha * i_l - i_0 * (
        np.exp(q * v[mask_forward] / (n * k * T)) - 1
    )

    # 反向偏压区 (V<0)
    mask_reverse = v < 0
    i[mask_reverse] = alpha * i_l + i_0_p * (
        np.exp(q * -v[mask_reverse] / (n_p * k * T)) - 1
    )

    return i

# 用 i 计算 v
def get_bc_volte(i, i_0, i_0_p, n, n_p, k, T, q, i_l, alpha):
    """
    计算BC模型的电压-电流关系（反向计算）

    参数:
        i: 电流数组 (A)
        其他参数同上

    返回:
        电压数组 (V)
    """
    v = np.zeros_like(i)

    # 正向工作区 (I≤αI_L)
    mask_forward = i <= alpha * i_l
    v[mask_forward] = n * k * T / q * np.log((alpha * i_l - i[mask_forward]) / i_0 + 1)

    # 反向工作区 (I>αI_L)
    mask_reverse = i > alpha * i_l
    v[mask_reverse] = (
        -n_p * k * T / q * np.log(-(alpha * i_l - i[mask_reverse]) / i_0_p + 1)
    )

    return v    