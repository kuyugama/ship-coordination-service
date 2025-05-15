import typing

from src.route.v1.schema import PostPositionBody


data: dict[str, dict] = {}


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
    # TODO: Speed and status
    position_record = {"time": body.time, "status": "green", "speed": 0, "position": position}

    ship_data["positions"].append(position_record)
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
