import time
import base64
from src import util


async def test_default(client):

    response = await client.post(
        "/auth/signup",
        json={"nickname": "nickname", "password": "password"},
    )
    print(response.json())
    assert response.status_code == 200

    assert response.json()["expires"] > time.time()
