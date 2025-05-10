async def test_default(client, user):
    response = await client.get(f"/user/")
    print(response.json())
    assert response.status_code == 200

    assert response.json()["pagination"] == {"total": 1, "pages": 1, "page": 1}

    item = response.json()["items"][0]

    assert item["nickname"] == user.nickname
    assert item["id"] == user.id
