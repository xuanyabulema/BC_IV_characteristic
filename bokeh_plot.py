# -*- coding: utf-8 -*-
"""
@File    :   bokeh_plot.py
@Time    :   2025/03/20 13:29:16
@Author  :   xuanyabulema@qq.com
@Version :
@Desc    :
"""

import numpy as np
from bokeh.io import curdoc
from bokeh.layouts import column, row, gridplot
from bokeh.models import ColumnDataSource, Slider, Legend, Div, Label
from bokeh.plotting import figure
from constants import *
from data_generator import generate_initial_data
from plot_updater import update_data


def plot_style_set(plot):
    """绘制 x 轴和 y 轴"""
    # 绘制 x 轴虚线
    x_axis_x = [-1000, 1000]
    x_axis_y = [0, 0]
    plot.line(x_axis_x, x_axis_y, line_dash="dashed", line_color="black", line_width=1)
    # 绘制 y 轴虚线
    y_axis_x = [0, 0]
    y_axis_y = [-1000, 1000]
    plot.line(y_axis_x, y_axis_y, line_dash="dashed", line_color="black", line_width=1)

    plot.title.align = "center"


# 生成初始数据
(
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
) = generate_initial_data()

# 创建数据源
source_shaded = ColumnDataSource(data={"v_values": v, "i_values": i_bc_shaded})
source_unshaded = ColumnDataSource(data={"v_values": v, "i_values": i_bc_unshaded})
source_parallel_shaded = ColumnDataSource(
    data={"v_values": v_parallel_shaded, "i_values": i_parallel_shaded}
)
source_series_shaded = ColumnDataSource(
    data={"v_values": v_series_shaded, "i_values": i_series_shaded}
)
source_series_shaded_24 = ColumnDataSource(
    data={"v_values": v_series_shaded_24, "i_values": i_series_shaded_24}
)
source_series_24 = ColumnDataSource(
    data={"v_values": v_bc_series_24, "i_values": i_bc_series_24}
)
source_shaded_group = ColumnDataSource(
    data={"v_values": v_shaded_group, "i_values": i_shaded_group}
)
source_unshaded_group = ColumnDataSource(
    data={"v_values": v_unshaded_group, "i_values": i_unshaded_group}
)
source_bc_all = ColumnDataSource(data={"v_values": V_all, "i_values": I_all})
source_bc_all_unshaded = ColumnDataSource(
    data={"v_values": V_all_unshaded, "i_values": I_all_unshaded}
)

# 创建绘图对象
plot = figure(
    height=PLOT_HEIGHT,
    width=PLOT_WIDTH,
    title="BC 电池 IV 曲线",
    tools="crosshair,pan,reset,save,wheel_zoom",
    x_range=X_RANGE,
    y_range=Y_RANGE,
    x_axis_label="电压 (V)",  # 添加 x 轴坐标名称
    y_axis_label="电流 (A)",  # 添加 y 轴坐标名称
    hidpi=True,
)

# 绘制曲线
line_shaded = plot.line(
    "v_values",
    "i_values",
    source=source_shaded,
    line_width=4,
    line_alpha=0.6,
    line_color="red",
    line_dash="dashed",
)
line_unshaded = plot.line(
    "v_values",
    "i_values",
    source=source_unshaded,
    line_width=3,
    line_alpha=0.6,
    line_color="black",
)

line_parallel_shaded = plot.line(
    "v_values",
    "i_values",
    source=source_parallel_shaded,
    line_width=3,
    line_alpha=0.6,
    line_color="blue",
    line_dash="dotted",
)

line_series_shaded = plot.line(
    "v_values",
    "i_values",
    source=source_series_shaded,
    line_width=3,
    line_alpha=0.6,
    line_color="green",
    line_dash="dotdash",
)

plot_style_set(plot)

# 创建图例
legend = Legend(
    items=[
        (f"遮挡电池：遮挡{1 - INITIAL_ALPHA_SHADED:.0%}", [line_shaded]),
        (f"正常电池", [line_unshaded]),
        (f"遮挡电池、正常电池并联", [line_parallel_shaded]),
        (f"遮挡电池、正常电池串联", [line_series_shaded]),
    ]
)
plot.add_layout(legend)

plot.legend.click_policy = "hide"  # 点击图例隐藏曲线

# 创建绘图对象
plot2 = figure(
    height=PLOT_HEIGHT,
    width=PLOT_WIDTH,
    title="遮挡串、正常串、并联旁路二极管",
    tools="crosshair,pan,reset,save,wheel_zoom",
    x_range=(-5, 20),
    y_range=(-2, 24),
    x_axis_label="电压 (V)",  # 添加 x 轴坐标名称
    y_axis_label="电流 (A)",  # 添加 y 轴坐标名称
    output_backend="webgl",
    hidpi=True,
)

plot_style_set(plot2)

# 绘制曲线：遮挡串
line_series_shaded_24 = plot2.line(
    "v_values",
    "i_values",
    source=source_series_shaded_24,
    line_width=4,
    line_alpha=0.6,
    line_color="red",
    # line_dash="dotdash",
)

# 正常串
line_series_24 = plot2.line(
    "v_values",
    "i_values",
    source=source_series_24,
    line_width=3,
    line_alpha=0.6,
    line_color="green",
)

# 遮挡组
line_shaded_group = plot2.line(
    "v_values",
    "i_values",
    source=source_shaded_group,
    line_width=3,
    line_alpha=0.6,
    line_color="blue",
    line_dash="dotted",
)

# 创建图例
legend2 = Legend(
    items=[
        (
            f"遮挡组：正常串+遮挡串+旁路二极管并联",
            [line_shaded_group],
        ),
        (
            f"遮挡串：{SHADED_CELL_COUNT}个遮挡{1-INITIAL_ALPHA_SHADED:.0%}电池，{UNSHADED_CELL_COUNT}个正常电池",
            [line_series_shaded_24],
        ),
        (
            f"正常串：{SHADED_CELL_COUNT+UNSHADED_CELL_COUNT}个正常电池",
            [line_series_24],
        ),
    ],
    location="top_right",
    ncols=2,
)
plot2.add_layout(legend2)

plot2.legend.click_policy = "hide"  # 点击图例隐藏曲线

# 创建绘图对象
plot3 = figure(
    height=PLOT_HEIGHT,
    width=PLOT_WIDTH,
    title="BC 组件 IV 曲线",
    tools="crosshair,pan,reset,save,wheel_zoom",
    x_range=(-5, 65),
    y_range=(-2, 24),
    x_axis_label="电压 (V)",  # 添加 x 轴坐标名称
    y_axis_label="电流 (A)",  # 添加 y 轴坐标名称
    output_backend="webgl",
    hidpi=True,
)

plot_style_set(plot3)


# BC组件
line_bc_all = plot3.line(
    "v_values",
    "i_values",
    source=source_bc_all,
    line_width=6,
    line_alpha=0.6,
    line_color="red",
    # line_dash="dotdash",
)

line_bc_all_unshaded = plot3.line(
    "v_values",
    "i_values",
    source=source_bc_all_unshaded,
    line_width=2,
    line_alpha=0.8,
    line_color="black",
)

line_shaded_group_in3 = plot3.line(
    "v_values",
    "i_values",
    source=source_shaded_group,
    line_width=3,
    line_alpha=0.6,
    line_color="blue",
    line_dash="dotted",
)

line_unshaded_group = plot3.line(
    "v_values",
    "i_values",
    source=source_unshaded_group,
    line_width=3,
    line_alpha=0.6,
    line_color="green",
)

legend3 = Legend(
    items=[
        (f"遮挡组：正常串+遮挡串+旁路二极管并联", [line_shaded_group_in3]),
        (f"正常组：正常串+正常串+并联旁路二极管串联", [line_unshaded_group]),
        (f"遮挡BC组件：1×遮挡组+2×正常组", [line_bc_all]),
        (f"正常BC组件：3×正常组", [line_bc_all_unshaded]),
    ],
    location="top_right",
    ncols=2,
)
plot3.add_layout(legend3)

plot3.legend.click_policy = "hide"  # 点击图例隐藏曲线

# 创建绘图对象
plot4 = figure(
    height=PLOT_HEIGHT,
    width=PLOT_WIDTH,
    title="BC 组件 PV 曲线",
    tools="crosshair,pan,reset,save,wheel_zoom",
    x_range=(-5, 65),
    y_range=(-100, 900),
    x_axis_label="电压 (V)",  # 添加 x 轴坐标名称
    y_axis_label="功率 (W)",  # 添加 y 轴坐标名称
    output_backend="webgl",
    hidpi=True,
)

plot_style_set(plot4)

plot4.legend.click_policy = "hide"  # 点击图例隐藏曲线

P_all = V_all * I_all
source_bc_p_all = ColumnDataSource(data={"v_values": V_all, "p_values": P_all})
P_all_unshaded = V_all_unshaded * I_all_unshaded
source_bc_p_all_unshaded = ColumnDataSource(
    data={"v_values": V_all_unshaded, "p_values": P_all_unshaded}
)

line_bc_p = plot4.line(
    "v_values",
    "p_values",
    source=source_bc_p_all,
    line_width=4,
    line_alpha=0.6,
    line_color="red",
    # line_dash="dotdash",
)

line_bc_p_unshaded = plot4.line(
    "v_values",
    "p_values",
    source=source_bc_p_all_unshaded,
    line_width=2,
    line_alpha=0.8,
    line_color="black",
    line_dash="dashed",
)

legend4 = Legend(
    items=[
        (f"遮挡BC组件", [line_bc_p]),
        (f"正常BC组件", [line_bc_p_unshaded]),
    ],
    location="top_left",
)
plot4.add_layout(legend4)

v_max = V_all[np.argmax(P_all)]
i_max = I_all[np.argmax(P_all)]
p_max = P_all[np.argmax(P_all)]
v_max_unshaded = V_all_unshaded[np.argmax(P_all_unshaded)]
i_max_unshaded = I_all_unshaded[np.argmax(P_all_unshaded)]
p_max_unshaded = P_all_unshaded[np.argmax(P_all_unshaded)]
# 创建标注
label = Label(
    x=v_max,
    y=p_max,
    text=f"{p_max:.2f}W \n {p_max/p_max_unshaded:.2%} \n {v_max:.2f}V {i_max:.2f}A",
    x_offset=0,
    y_offset=-30,
    text_align="center",
    text_baseline="top",
    # text_font_size="12pt",
    text_color="red",
)
plot4.add_layout(label)
label_unshaded = Label(
    x=v_max_unshaded,
    y=p_max_unshaded,
    text=f"{p_max_unshaded:.2f}W\n{v_max_unshaded:.2f}V {i_max_unshaded:.2f}A",
    x_offset=0,
    y_offset=0,
    text_align="center",
    text_baseline="bottom",
    # text_font_size="12pt",
)
plot4.add_layout(label_unshaded)

# 创建滑块小部件
slider_alpha = Slider(
    title="遮挡比例", value=INITIAL_ALPHA_SHADED, start=0, end=1.0, step=0.25
)
slider_i_l = Slider(
    title="光生电流", value=INITIAL_I_L, start=0, end=INITIAL_I_L + 2, step=1.0
)
slider_i_0_p = Slider(
    title="反向隧穿系数", value=INITIAL_I_0_P, start=0, end=1, step=0.1
)

slider_cell_count = Slider(
    title="单串电池数量", value=CELL_COUNT, start=20, end=26, step=2
)

slider_shaded_cell_count = Slider(
    title="遮挡电池数量", value=SHADED_CELL_COUNT, start=1, end=10, step=1
)

slider_shaded_group_count = Slider(
    title="遮挡电池组数量", value=1, start=0, end=3, step=1
)

# 为每个滑块添加值改变时的回调函数
for w in [
    slider_alpha,
    slider_i_l,
    slider_i_0_p,
    slider_cell_count,
    slider_shaded_cell_count,
    slider_shaded_group_count,
]:
    w.on_change(
        "value",
        lambda attr, old, new: update_data(
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
        ),
    )

# 设置布局并添加到文档
inputs1 = gridplot(
    [
        [
            slider_cell_count,
            slider_i_l,
            slider_i_0_p,
            slider_alpha,
            slider_shaded_cell_count,
            slider_shaded_group_count,
        ]
    ],
    sizing_mode="stretch_width",
)
plots_top = gridplot([[plot, plot2]], sizing_mode="stretch_width")
plots_bottom = gridplot([[plot3, plot4]], sizing_mode="stretch_width")
curdoc().add_root(column(plots_top, inputs1, plots_bottom, sizing_mode="stretch_both"))

curdoc().title = "BC IV曲线动画展示"
