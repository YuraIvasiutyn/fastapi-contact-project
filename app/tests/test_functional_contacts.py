import pytest
from httpx import AsyncClient
from fastapi import status
from main import app


@pytest.mark.asyncio
async def test_get_all_contacts():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/contacts", headers={"Authorization": "Bearer <your_token>"})
        assert response.status_code == status.HTTP_200_OK
        assert "contacts" in response.json()
