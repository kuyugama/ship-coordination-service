async def test_default(client, user, token):
    response = await client.get("/user/me", headers={"X-Token": token.body})
    print(response.json())
    assert response.status_code == 200

    assert response.json()["nickname"] == user.nickname
    assert response.json()["id"] == user.id
