import time

from fastapi import APIRouter
from starlette.responses import JSONResponse

from . import service

from .schema import (
    GetShipResponse,
    PostPositionBody,
    ListShipsResponse,
    PostPositionResponse,
)

router = APIRouter(prefix="/api")

ships_router = APIRouter(prefix="/ships")


@ships_router.post(
    "/{id_}/position",
    summary="Add ship position",
    operation_id="ships.add_position",
    response_model=PostPositionResponse,
)
def add_ship_position(id_: str, body: PostPositionBody):
    if body.time < int(time.time()):
        return JSONResponse({"error": "time out of range"}, 422)

    return service.add_ship_position(id_, body)


@ships_router.get(
    "",
    summary="Get known ships statuses",
    operation_id="ships.list_all",
    response_model=ListShipsResponse,
)
def list_ships():
    return {"ships": service.list_ships()}


@ships_router.get(
    "/{id_}",
    summary="Get ship details",
    operation_id="ships.get_ship",
    response_model=GetShipResponse,
)
def get_ship(id_: str):
    return service.get_ship(id_)


router.include_router(ships_router)


@router.post("/flush", summary="Flush data", operation_id="flush")
def flush():
    service.flush_data()
