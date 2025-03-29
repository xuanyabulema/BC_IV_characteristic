import numpy as np
from constants import *
from bc_model import get_bc_current, get_bc_volte


def generate_initial_data():
    # 提取常量
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

    # 计算初始电流
    i_bc_shaded = get_bc_current(
        v, i_0, INITIAL_I_0_P, n, n_p, k, T, q, i_l, INITIAL_ALPHA_SHADED
    )
    i_bc_unshaded = get_bc_current(
        v, i_0, INITIAL_I_0_P, n, n_p, k, T, q, i_l, INITIAL_ALPHA_UNSHADED
    )

    # 计算遮挡、正常电池并联曲线
    v_parallel_shaded = v
    i_parallel_shaded = i_bc_shaded + i_bc_unshaded

    # 计算遮挡、正常电池串联曲线
    i_series_shaded = i_bc_shaded
    # 用遮挡电池的电流求对应正常电池的电压，用于串联曲线电压相加
    v_series_shaded = v + get_bc_volte(
        i_series_shaded,
        i_0,
        INITIAL_I_0_P,
        n,
        n_p,
        k,
        T,
        q,
        i_l,
        INITIAL_ALPHA_UNSHADED,
    )

    # 遮挡串
    # 计算 UNSHADED_CELL_COUNT 个正常电池和 SHADED_CELL_COUNT 个遮挡电池串联构成遮挡串
    i_series_shaded_24 = i_bc_shaded
    v_series_shaded_24 = SHADED_CELL_COUNT * v + UNSHADED_CELL_COUNT * get_bc_volte(
        i_series_shaded,
        i_0,
        INITIAL_I_0_P,
        n,
        n_p,
        k,
        T,
        q,
        i_l,
        INITIAL_ALPHA_UNSHADED,
    )
    if v_series_shaded_24[0] > 0:
        v_series_shaded_24 = np.insert(v_series_shaded_24, 0, 0)
        i_series_shaded_24 = np.insert(i_series_shaded_24, 0, i_series_shaded_24[0])

    # 计算正常串
    i_bc_series_24 = i_bc_unshaded
    v_bc_series_24 = v * (SHADED_CELL_COUNT + UNSHADED_CELL_COUNT)

    # 遮挡组：遮挡串与正常串并联+并联旁路二极管
    # 用遮挡串的电压去求对应正常串的电流用于相加
    v_shaded_group_temp = v_series_shaded_24
    i_shaded_group_temp = i_series_shaded_24 + get_bc_current(
        v_series_shaded_24 / (SHADED_CELL_COUNT + UNSHADED_CELL_COUNT),
        i_0,
        INITIAL_I_0_P,
        n,
        n_p,
        k,
        T,
        q,
        i_l,
        INITIAL_ALPHA_UNSHADED,
    )
    # 并联旁路二极管
    v_diode = np.linspace(v_oc * 1.3, 0, 200)
    i_diode = i_0 * (np.exp(q * v_diode / (n * k * T)) - 1)

    i_for_parallel_shaded_p = i_shaded_group_temp[v_shaded_group_temp >= 0]
    v_for_parallel_shaded_p = v_shaded_group_temp[v_shaded_group_temp >= 0]
    i_shaded_group = np.concatenate(
        [i_diode + i_for_parallel_shaded_p[0], i_for_parallel_shaded_p]
    )
    v_shaded_group = np.concatenate([-v_diode, v_for_parallel_shaded_p])

    # 计算正常组：正常串与正常串并联+并联旁路二极管
    v_group_temp = v_bc_series_24
    i_group_temp = i_bc_series_24 * 2
    i_for_parallel_unshaded_p = i_group_temp[v_group_temp >= 0]
    v_for_parallel_unshaded_p = v_group_temp[v_group_temp >= 0]
    i_unshaded_group = np.concatenate(
        [i_diode + i_for_parallel_unshaded_p[0], i_for_parallel_unshaded_p]
    )
    v_unshaded_group = np.concatenate([-v_diode, v_for_parallel_unshaded_p])

    # 遮挡组 正常组 串联成组件
    # 利用遮挡组的电流 求正常组 对应的电压
    i_parallel_shaded_diode_bigger_than_2_i_sc = (
        i_shaded_group[i_shaded_group >= 2 * i_sc] - i_sc * 2
    )
    v_parallel_diode_bigger_than_2_i_sc = (
        -np.log((i_parallel_shaded_diode_bigger_than_2_i_sc) / i_0 + 1)
        * (n * k * T)
        / q
    )
    # 利用遮挡组的电流 求正常组 其他部分电压
    i_parallel_shaded_diode_smaller_than_2_i_sc = i_shaded_group[
        i_shaded_group < i_sc * 2
    ]
    v_parallel_diode_smaller_than_2_i_sc = (SHADED_CELL_COUNT + UNSHADED_CELL_COUNT) * (
        np.log((i_l - i_parallel_shaded_diode_smaller_than_2_i_sc / 2) / i_0 + 1)
        * (n * k * T)
        / q
    )
    v_diode_for_plus = np.concatenate(
        [v_parallel_diode_bigger_than_2_i_sc, v_parallel_diode_smaller_than_2_i_sc]
    )

    V_all = (
        v_diode_for_plus * UNSHADED_GROUP_COUNT + v_shaded_group * SHADED_GROUP_COUNT
    )
    I_all = i_shaded_group

    # 未遮挡
    V_all_unshaded = v_diode_for_plus * GROUP_COUNT
    I_all_unshaded = i_shaded_group

    return (
        v,
        i_bc_shaded,
        i_bc_unshaded,
        v_parallel_shaded,
        i_parallel_shaded,
        v_series_shaded,
        i_series_shaded,
        i_0,
        n,
        n_p,
        k,
        T,
        q,
        i_l,
        i_series_shaded_24,
        v_series_shaded_24,
        v_bc_series_24,
        i_bc_series_24,
        v_shaded_group,
        i_shaded_group,
        v_unshaded_group,
        i_unshaded_group,
        V_all,
        I_all,
        V_all_unshaded,
        I_all_unshaded,
    )
