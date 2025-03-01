import numpy as np
import pyautogui
import time
import math


def bezier_curve(control_points, num_points=100):
    n = len(control_points) - 1
    curve_points = np.zeros((num_points, 2))
    b = np.copy(control_points)

    for i in range(num_points):
        t = i / (num_points - 1)
        for r in range(1, n + 1):
            for j in range(n - r + 1):
                b[j] = (1 - t) * b[j] + t * b[j + 1]
        curve_points[i] = b[0]

    return curve_points
    pass


def move_mouse_along_bezier(start, end, control_points=[], speed=0.1, num_points=100, delay=0.01):
    # 将起点和终点添加到控制点列表中（如果它们还没有被作为控制点提供）
    if start not in control_points:
        control_points.insert(0, start)
    if end not in control_points:
        control_points.append(end)

    # 确保控制点是一个numpy数组
    control_points = np.array(control_points)

    # 计算贝塞尔曲线上的点
    curve_points = bezier_curve(control_points, num_points)

    # 计算每两点之间移动的总时间（基于速度参数，但这里速度实际上是时间间隔的倒数）
    # 由于我们没有实际的距离信息，我们只能基于点的数量来分配时间
    # 因此，这里的'speed'参数实际上表示每两点之间的固定延时（秒），但为了与原始要求保持一致，我们保留了这个名称
    # 总时间 = (num_points - 1) * delay（但这里的delay实际上是由speed参数间接控制的，如果我们想保持一致的移动速率）
    # 然而，为了简单起见，我们将直接使用提供的delay参数，并忽略speed参数的实际速度含义
    # 如果想要基于实际速度（如米/秒）来控制，我们需要额外的信息来计算每两点之间的距离

    # 移动鼠标沿曲线
    for i in range(num_points - 1):
        current_point = curve_points[i].astype(int)
        next_point = curve_points[i + 1].astype(int)

        pyautogui.moveTo(current_point[0], current_point[1], duration=0)  # 瞬间移动到当前点（因为我们是在一系列点之间平滑移动）
        time.sleep(delay)  # 在移动到下一点之前等待

        # 注意：这里我们没有使用pyautogui的moveTo的duration参数来平滑移动，
        # 因为这会导致在每个点之间有一个加速和减速的过程，而不是沿着曲线的平滑移动。
        # 相反，我们通过连续调用moveTo并添加延时来模拟平滑移动。
        # 如果想要真正的平滑移动，可能需要使用其他库或方法来实现曲线的插值和平滑动画。

    # 最后，确保鼠标停留在终点
    pyautogui.moveTo(curve_points[-1].astype(int), duration=0)

