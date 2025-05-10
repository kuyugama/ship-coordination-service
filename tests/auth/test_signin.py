import time


async def test_default(client, user, password):
    response = await client.post(
        "/auth/signin", json={"nickname": user.nickname, "password": password}
    )
    print(response.json())
    assert response.status_code == 200

    assert response.json()["expires"] > time.time()


async def test_invalid_secret(client, user, password):
    response = await client.post(
        "/auth/signin", json={"nickname": user.nickname, "password": password + " invalid"}
    )
    print(response.json())
    assert response.status_code == 403

    assert response.json()["category"] == "auth"
    assert response.json()["code"] == "invalid-password"
