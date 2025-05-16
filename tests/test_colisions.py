import pytest
from math import sqrt
from src.route.v1.util import classify_collision


def test_no_risk_far_apart():
    ship_a = ((0, 0, 0), (10, 0, 1))
    ship_b = ((0, 100, 0), (10, 100, 1))
    assert classify_collision(ship_a, ship_b) == "green"


def test_possible_collision_exact():
    ship_a = ((0, 0, 0), (10, 0, 1))
    ship_b = ((10, 0, 0), (0, 0, 1))
    assert classify_collision(ship_a, ship_b) == "red"


def test_tangent_path_yellow_zone():
    ship_a = ((0, 0, 0), (10, 0, 1))
    ship_b = ((10, 1, 0), (0, 1, 1))
    assert classify_collision(ship_a, ship_b) == "yellow"


def test_same_direction_different_speed_green():
    ship_a = ((0, 0, 0), (10, 0, 1))
    ship_b = ((0, 0, 1), (5, 0, 2))
    assert classify_collision(ship_a, ship_b) == "green"


def test_same_position_same_direction_red():
    ship_a = ((0, 0, 0), (10, 0, 1))
    ship_b = ((0, 0, 0), (10, 0, 1))
    assert classify_collision(ship_a, ship_b) == "red"


def test_insufficient_data():
    ship_a = ((0, 0, 0), (0, 0, 0))
    ship_b = ((10, 10, 0), (20, 20, 1))
    assert classify_collision(ship_a, ship_b) == "green"
