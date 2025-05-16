import time


async def test_default(client):
    id_ = "shipid"
    now = int(time.time())
    x = 10
    y = 15
    publish = await client.post(f"/v1/api/ships/{id_}/position", json={"time": now, "x": x, "y": y})
    print("publish", publish.json())

    assert publish.status_code == 200

    response = await client.get("/v1/api/ships/")
    print("list", response.json())

    assert response.status_code == 200

    expected = [
        {
            "id": id_,
            "last_time": now,
            "last_status": publish.json()["status"],
            "last_speed": publish.json()["speed"],
            "last_position": {"x": x, "y": y},
        }
    ]

    assert response.json()["ships"] == expected
