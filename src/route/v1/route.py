from fastapi import APIRouter


router = APIRouter(prefix="/api/ships")


@router.post("/{id_}/position", summary="Add ship position", operation_id="ships.add_position")
def add_ship_position(id_: int):
    pass


@router.get("", summary="Get known ships statuses", operation_id="ships.list_all")
def list_ships():
    pass


@router.get("/{id_}", summary="Get ship details", operation_id="ships.get_ship")
def get_ship(id_: int):
    pass
