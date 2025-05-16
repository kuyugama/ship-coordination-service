import math
import typing

from .schema import PostPositionBody
from .util import classify_collision

data: dict[str, dict] = {}


def latest_positions(
    ship: dict[str, typing.Any],
) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    records = ship["positions"][-2:]

    if len(records) < 2:
        return (
            (records[0]["position"]["x"], records[0]["position"]["y"], records[0]["time"]),
            (records[0]["position"]["x"], records[0]["position"]["y"], records[0]["time"]),
        )

    return (
        (records[0]["position"]["x"], records[0]["position"]["y"], records[0]["time"]),
        (records[1]["position"]["x"], records[1]["position"]["y"], records[1]["time"]),
    )


def find_dangerest_status(ship: dict[str, typing.Any]) -> str:
    last_status = "green"
    for ship_ in data.values():
        if ship_["id"] == ship["id"]:
            continue

        status = classify_collision(latest_positions(ship), latest_positions(ship_))

        if status == "red":
            return "red"

        if last_status == "yellow":
            continue

        last_status = status

    return last_status


def add_ship_position(id_: str, body: PostPositionBody) -> dict[str, typing.Any]:
    ship_data = data.setdefault(
        id_,
        {
            "id": id_,
            "last_time": 0,
            "last_status": "green",
            "last_speed": 0,
            "last_position": None,
            "positions": [],
        },
    )
    ship_data["last_time"] = body.time

    position = {"x": body.x, "y": body.y}

    position_record = {
        "time": body.time,
        "status": "",  # speed and status are defined later
        "speed": 0,
        "position": position,
    }

    ship_data["positions"].append(position_record)
    position_record["status"] = find_dangerest_status(ship_data)
    (x_start, y_start, time_start), (x_end, y_end, time_end) = latest_positions(ship_data)

    delta_time = time_end - time_start
    if delta_time == 0:
        velocity_vector = (0, 0)
    else:
        velocity_vector = ((x_end - x_start) / delta_time, (y_end - y_start) / delta_time)

    velocity = math.hypot(velocity_vector[0], velocity_vector[1])
    position_record["speed"] = round(velocity)

    ship_data["last_position"] = position

    ship_data["last_status"] = position_record["status"]
    ship_data["last_speed"] = position_record["speed"]

    return {
        "time": body.time,
        "status": position_record["status"],
        "speed": position_record["speed"],
        "x": position["x"],
        "y": position["y"],
    }


def list_ships() -> typing.ValuesView[dict[str, typing.Any]]:
    return data.values()


def get_ship(id_: str) -> dict[str, typing.Any]:
    return data.get(id_)


def flush_data():
    data.clear()
