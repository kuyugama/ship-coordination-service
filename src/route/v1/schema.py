from src.schema import Schema


class PostPositionBody(Schema):
    time: int
    x: int
    y: int


class Position(Schema):
    x: int
    y: int


class PostPositionResponse(Position):
    time: int
    status: str
    speed: int


class PositionRecord(Schema):
    time: int
    status: str
    speed: int
    position: Position


class GetShipResponse(Schema):
    id: str
    positions: list[PositionRecord]


class Ship(Schema):
    id: str
    last_time: int
    last_status: str
    last_speed: int
    last_position: Position


class ListShipsResponse(Schema):
    ships: list[Ship]
