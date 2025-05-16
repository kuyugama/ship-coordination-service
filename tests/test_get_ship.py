import time


async def test_default(client):
    id_ = "shipid"
    now = int(time.time())
    x = 10
    y = 15
    publish = await client.post(f"/v1/api/ships/{id_}/position", json={"time": now, "x": x, "y": y})
    print("publish", publish.json())

    assert publish.status_code == 200

    response = await client.get(f"/v1/api/ships/{id_}")
    print("info", response.json())

    assert response.status_code == 200

    expected = {
        "id": id_,
        "positions": [
            {
                "time": now,
                "speed": publish.json()["speed"],
                "status": publish.json()["status"],
                "position": {"x": x, "y": y},
            }
        ],
    }

    assert response.json() == expected
