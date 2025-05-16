import time


async def test_default(client):
    now = int(time.time())
    x = 10
    y = 15
    response = await client.post(
        "/v1/api/ships/shipid/position", json={"time": now, "x": x, "y": y}
    )
    print(response.json())

    assert response.status_code == 200

    assert response.json() == {"time": now, "x": x, "y": y, "speed": 0, "status": "green"}


async def test_invalid_time(client):
    response = await client.post("/v1/api/ships/shipid/position", json={"time": 1, "x": 0, "y": 0})
    print("past", response.json())
    assert response.status_code == 422
    assert response.json() == {"error": "time out of range"}

    response = await client.post(
        "/v1/api/ships/shipid/position", json={"time": 1.2, "x": 0, "y": 0}
    )
    print("fraction", response.json())
    assert response.status_code == 422
    assert (
        response.json()["general"]
        == "Invalid field time: Input should be a valid integer, got a number with a fractional part"
    )


async def test_invalid_position(client):
    now = int(time.time())

    response = await client.post(
        "/v1/api/ships/shipid/position", json={"time": now, "x": 0.1, "y": 0}
    )
    print("x", response.json())
    assert response.status_code == 422
    assert (
        response.json()["general"]
        == "Invalid field x: Input should be a valid integer, got a number with a fractional part"
    )

    response = await client.post(
        "/v1/api/ships/shipid/position", json={"time": now, "x": 0, "y": 0.1}
    )
    print("y", response.json())
    assert response.status_code == 422
    assert (
        response.json()["general"]
        == "Invalid field y: Input should be a valid integer, got a number with a fractional part"
    )
