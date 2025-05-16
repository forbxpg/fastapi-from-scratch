import json

import pytest


async def test_create_user_valid_data(client, get_user_from_db):
    """Тест для создания пользователя."""
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "examplemail@mail.com",
        "phone": "934949999",
    }
    response = await client.post("/api/v1/users/", json=user_data)
    assert response.status == 200
    response_data = response.json()
    assert response_data["first_name"] == user_data["first_name"]
    assert response_data["last_name"] == user_data["last_name"]
    assert response_data["email"] == user_data["email"]
    assert response_data["phone"] == user_data["phone"]
    user_from_db = await get_user_from_db(user_data["user_id"])
    assert len(user_from_db) == 1
    data = dict(user_from_db[0])
    assert data["first_name"] == user_data["first_name"]
    assert data["last_name"] == user_data["last_name"]
    assert data["email"] == user_data["email"]
    assert data["phone"] == user_data["phone"]
