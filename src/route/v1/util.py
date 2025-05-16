from typing import Tuple
import math


def vector(p1: tuple[int, int], p2: tuple[int, int]) -> tuple[int, int]:
    return p2[0] - p1[0], p2[1] - p1[1]


def magnitude(v: tuple[float, float]) -> float:
    return math.sqrt(v[0] ** 2 + v[1] ** 2)


def dot(v1: tuple[float, float], v2: tuple[float, float]) -> float:
    return v1[0] * v2[0] + v1[1] * v2[1]


def classify_collision(
    ship_a: tuple[tuple[int, int, int], tuple[int, int, int]],
    ship_b: tuple[tuple[int, int, int], tuple[int, int, int]],
) -> str:
    # ship = ((start x, start y, start time), (end x, end y, end time))
    (x_start_a, y_start_a, time_start_a), (x_end_a, y_end_a, time_end_a) = ship_a
    (x_start_b, y_start_b, time_start_b), (x_end_b, y_end_b, time_end_b) = ship_b

    delta_time_a = time_end_a - time_start_a
    delta_time_b = time_end_b - time_start_b
    if delta_time_a == 0 or delta_time_b == 0:
        return "green"  # insufficient data

    common_start = max(time_start_a, time_start_b)
    common_end = min(time_end_a, time_end_b)

    if common_start >= common_end:
        return "green"

    velocity_a = ((x_end_a - x_start_a) / delta_time_a, (y_end_a - y_start_a) / delta_time_a)
    velocity_b = ((x_end_b - x_start_b) / delta_time_b, (y_end_b - y_start_b) / delta_time_b)
    position_a = (x_start_a, y_start_a)
    position_b = (x_start_b, y_start_b)

    # vector difference
    delta_position = (position_a[0] - position_b[0], position_a[1] - position_b[1])
    delta_velocity = (velocity_a[0] - velocity_b[0], velocity_a[1] - velocity_b[1])

    dot_delta_velocity = dot(delta_velocity, delta_velocity)
    if dot_delta_velocity == 0:
        # parallel or same direction
        distance = magnitude(delta_position)
        if distance == 0:
            return "red"
        elif distance <= 1:
            return "yellow"
        else:
            return "green"

    time_closest = -dot(delta_position, delta_velocity) / dot_delta_velocity
    if time_closest <= 0:
        time_closest = 0

    # Position of ships at time_closest
    c1x = position_a[0] + velocity_a[0] * time_closest
    c1y = position_a[1] + velocity_a[1] * time_closest
    c2x = position_b[0] + velocity_b[0] * time_closest
    c2y = position_b[1] + velocity_b[1] * time_closest

    distance = math.hypot(c1x - c2x, c1y - c2y)

    if distance == 0:
        return "red"
    elif distance <= 1:
        return "yellow"
    else:
        return "green"
