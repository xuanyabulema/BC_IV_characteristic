from bc_model import get_bc_current, get_bc_volte
from constants import INITIAL_ALPHA_UNSHADED, v_oc, GROUP_COUNT
import numpy as np


def update_data(
    attr,
    old,
    new,
    v,
    source_shaded,
    source_unshaded,
    source_parallel_shaded,
    source_series_shaded,
    source_series_shaded_24,
    source_series_24,
    source_shaded_group,
    source_unshaded_group,
    source_bc_all,
    source_bc_all_unshaded,
    legend,
    legend2,
    legend3,
    legend4,
    line_shaded,
    line_unshaded,
    line_parallel_shaded,
    line_series_shaded,
    line_series_shaded_24,
    line_series_24,
    line_shaded_group,
    line_shaded_group_in3,
    line_unshaded_group,
    line_bc_all,
    line_bc_all_unshaded,
    slider_alpha,
    slider_i_l,
    slider_i_0_p,
    slider_cell_count,
    slider_shaded_cell_count,
    slider_shaded_group_count,
    i_0,
    n,
    n_p,
    k,
    T,
    q,
    i_l,
    line_bc_p,
    source_bc_p_all,
    source_bc_p_all_unshaded,
    label,
    label_unshaded,
):
    """
    滑块值改变时更新数据和图例
    """

    # 获取当前滑块的值
    alpha_shaded = 1 - slider_alpha.value
    i_l = slider_i_l.value
    i_0_p = slider_i_0_p.value
    cell_count = slider_cell_count.value
    shaded_cell_count = slider_shaded_cell_count.value
    unshaded_cell_count = cell_count - shaded_cell_count
    shaded_group_count = slider_shaded_group_count.value
    unshaded_group_count = GROUP_COUNT - shaded_group_count

    # i_sc = i_0 * (np.exp(q * v_oc / (n * k * T)) - 1)
    i_sc = i_l

    # 生成新的曲线数据
    i_bc_shaded = get_bc_current(v, i_0, i_0_p, n, n_p, k, T, q, i_l, alpha_shaded)
    i_bc_unshaded = get_bc_current(
        v, i_0, i_0_p, n, n_p, k, T, q, i_l, INITIAL_ALPHA_UNSHADED
    )
    v_parallel_shaded = v
    i_parallel_shaded = i_bc_shaded + i_bc_unshaded

    # 计算遮挡、正常电池串联曲线
    i_series_shaded = i_bc_shaded
    # 用遮挡电池的电流求对应正常电池的电压，用于串联曲线电压相加
    v_series_shaded = v + get_bc_volte(
        i_series_shaded, i_0, i_0_p, n, n_p, k, T, q, i_l, INITIAL_ALPHA_UNSHADED
    )

    # 更新数据源
    source_shaded.data = {"v_values": v, "i_values": i_bc_shaded}
    source_unshaded.data = {"v_values": v, "i_values": i_bc_unshaded}
    source_parallel_shaded.data = {
        "v_values": v_parallel_shaded,
        "i_values": i_parallel_shaded,
    }
    source_series_shaded.data = {
        "v_values": v_series_shaded,
        "i_values": i_series_shaded,
    }

    # 计算 UNSHADED_CELL_COUNT 个正常电池和 SHADED_CELL_COUNT 个遮挡电池串联构成遮挡串
    i_series_shaded_24 = i_bc_shaded
    v_series_shaded_24 = shaded_cell_count * v + unshaded_cell_count * get_bc_volte(
        i_series_shaded,
        i_0,
        i_0_p,
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
    # 更新数据源
    source_series_shaded_24.data = {
        "v_values": v_series_shaded_24,
        "i_values": i_series_shaded_24,
    }

    # 计算正常串
    i_bc_series_24 = i_bc_unshaded
    v_bc_series_24 = v * (shaded_cell_count + unshaded_cell_count)
    # 更新数据源
    source_series_24.data = {
        "v_values": v_bc_series_24,
        "i_values": i_bc_series_24,
    }

    # 遮挡组：遮挡串与正常串并联+并联旁路二极管
    # 用遮挡串的电压去求对应正常串的电流用于相加
    v_shaded_group_temp = v_series_shaded_24
    i_shaded_group_temp = i_series_shaded_24 + get_bc_current(
        v_series_shaded_24 / (shaded_cell_count + unshaded_cell_count),
        i_0,
        i_0_p,
        n,
        n_p,
        k,
        T,
        q,
        i_l,
        INITIAL_ALPHA_UNSHADED,
    )

    # 并联旁路二极管
    v_diode = np.linspace(v_oc * 1.3, 0, 2000)
    i_diode = i_0 * (np.exp(q * v_diode / (n * k * T)) - 1)

    i_for_parallel_shaded_p = i_shaded_group_temp[v_shaded_group_temp >= 0]
    v_for_parallel_shaded_p = v_shaded_group_temp[v_shaded_group_temp >= 0]
    i_shaded_group = np.concatenate(
        [i_diode + i_for_parallel_shaded_p[0], i_for_parallel_shaded_p]
    )
    v_shaded_group = np.concatenate([-v_diode, v_for_parallel_shaded_p])
    # 更新数据源
    source_shaded_group.data = {
        "v_values": v_shaded_group,
        "i_values": i_shaded_group,
    }

    # 计算正常组：正常串与正常串并联+并联旁路二极管
    v_group_temp = v_bc_series_24
    i_group_temp = i_bc_series_24 * 2
    i_for_parallel_unshaded_p = i_group_temp[v_group_temp >= 0]
    v_for_parallel_unshaded_p = v_group_temp[v_group_temp >= 0]
    i_unshaded_group = np.concatenate(
        [i_diode + i_for_parallel_unshaded_p[0], i_for_parallel_unshaded_p]
    )
    v_unshaded_group = np.concatenate([-v_diode, v_for_parallel_unshaded_p])
    source_unshaded_group.data = {
        "v_values": v_unshaded_group,
        "i_values": i_unshaded_group,
    }
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
    v_parallel_diode_smaller_than_2_i_sc = (shaded_cell_count + unshaded_cell_count) * (
        np.log((i_l - i_parallel_shaded_diode_smaller_than_2_i_sc / 2) / i_0 + 1)
        * (n * k * T)
        / q
    )
    v_diode_for_plus = np.concatenate(
        [v_parallel_diode_bigger_than_2_i_sc, v_parallel_diode_smaller_than_2_i_sc]
    )

    V_all = (
        v_diode_for_plus * unshaded_group_count + v_shaded_group * shaded_group_count
    )
    I_all = i_shaded_group
    # 更新数据源
    source_bc_all.data = {"v_values": V_all, "i_values": I_all}

    # 未遮挡
    V_all_unshaded = v_diode_for_plus * GROUP_COUNT
    I_all_unshaded = i_shaded_group
    source_bc_all_unshaded.data = {
        "v_values": V_all_unshaded,
        "i_values": I_all_unshaded,
    }

    source_bc_p_all.data = {"v_values": V_all, "p_values": V_all * I_all}

    # 更新图例标签
    legend.items = [
        (f"遮挡电池：遮挡{1 - alpha_shaded:.0%}", [line_shaded]),
        (f"正常电池", [line_unshaded]),
        (f"遮挡电池、正常电池并联", [line_parallel_shaded]),
        (f"遮挡电池、正常电池串联", [line_series_shaded]),
    ]

    legend2.items = [
        (
            f"遮挡组：正常串+遮挡串+旁路二极管并联",
            [line_shaded_group],
        ),
        (
            f"遮挡串：{shaded_cell_count}个遮挡{1-alpha_shaded:.0%}电池，{unshaded_cell_count}个正常电池",
            [line_series_shaded_24],
        ),
        (
            f"正常串：{shaded_cell_count + unshaded_cell_count}个正常电池",
            [line_series_24],
        ),
    ]

    legend3.items = [
        (f"遮挡组：正常串+遮挡串+旁路二极管并联", [line_shaded_group_in3]),
        (f"正常组：正常串+正常串+并联旁路二极管串联", [line_unshaded_group]),
        (
            f"遮挡BC组件：{shaded_group_count}×遮挡组+{unshaded_group_count}×正常组",
            [line_bc_all],
        ),
        (f"正常BC组件：{GROUP_COUNT}×正常组", [line_bc_all_unshaded]),
    ]

    P_all = V_all * I_all
    v_max = V_all[np.argmax(P_all)]
    i_max = I_all[np.argmax(P_all)]
    p_max = P_all[np.argmax(P_all)]
    P_all_unshaded = V_all_unshaded * I_all_unshaded
    v_max_unshaded = V_all_unshaded[np.argmax(P_all_unshaded)]
    i_max_unshaded = I_all_unshaded[np.argmax(P_all_unshaded)]
    source_bc_p_all_unshaded.data = {
        "v_values": V_all_unshaded,
        "p_values": P_all_unshaded,
    }

    p_max_unshaded = P_all_unshaded[np.argmax(P_all_unshaded)]
    label.text = (
        f"{p_max:.2f}W \n {p_max/p_max_unshaded:.2%} \n {v_max:.2f}V {i_max:.2f}A"
    )
    label.x = v_max
    label.y = p_max

    label_unshaded.text = (
        f"{p_max_unshaded:.2f}W\n{v_max_unshaded:.2f}V {i_max_unshaded:.2f}A"
    )
    label_unshaded.x = v_max_unshaded
    label_unshaded.y = p_max_unshaded
