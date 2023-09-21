from unittest.mock import AsyncMock, patch

import pytest


@patch("app.handlers.user.new_user_handler.NewUserHandler._check_user_existance", return_value=None)
@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_create_new_user(user_exist, anyio_backend, test_app):
    async with test_app as client:
        with patch("app.handlers.user.new_user_handler.NewUserHandler._create_user"):
            response = await client.post("/api/user/", json={"name": "test_user", "points": 100})
            response_body = response.json()
            assert response.status_code == 200
            assert response_body.get("status") == "ok"


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_get_user_info(anyio_backend, test_app):
    user_info = AsyncMock(return_value={"id": 1, "name": "test_user", "points": 0})
    async with test_app as client:
        with patch("app.handlers.user.user_info_handler.UserInfoHandler._get_user_info", user_info):
            response = await client.get("/api/user/1")
            response_body = response.json()
            assert response.status_code == 200
            assert response_body.get("id") == 1
            assert response_body.get("name") == "test_user"


@patch("app.handlers.user.user_points_handler.UserPointsHandler._check_user_existance", return_value=True)
@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_increase_points(user_exist, anyio_backend, test_app):
    async with test_app as client:
        with patch("app.handlers.user.user_points_handler.UserPointsHandler._add_user_points"):
            response = await client.put("/api/user/1", json={"points_amount": 100})
            response_body = response.json()
            assert response.status_code == 200
            assert response_body.get("status") == "ok"


@patch("app.handlers.user.user_delete_handler.DeleteUserHandler._check_user_existance", return_value=True)
@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_delete_user(user_exist, anyio_backend, test_app):
    async with test_app as client:
        with patch("app.handlers.user.user_delete_handler.DeleteUserHandler._delete_user"):
            response = await client.delete("/api/user/1")
            response_body = response.json()
            assert response.status_code == 200
            assert response_body.get("status") == "ok"


@patch("app.handlers.item.item_handler.BuyItemHandler._get_points_amount", return_value=200)
@patch("app.handlers.item.item_handler.BuyItemHandler._get_item_price", return_value=100)
@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_buy_item(balance, price, anyio_backend, test_app):
    async with test_app as client:
        with patch("app.handlers.item.item_handler.BuyItemHandler._buy_item"):
            response = await client.post("/api/item/buy", json={"user_id": "test_user", "item_name": "AK-47"})
            response_body = response.json()
            assert response.status_code == 200
            assert response_body.get("balance_remain") == 100


@patch("app.handlers.item.add_item_handler.NewItemHandler._check_item_existance", return_value=None)
@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_add_item(item_exist, anyio_backend, test_app):
    async with test_app as client:
        with patch("app.handlers.item.add_item_handler.NewItemHandler._create_item"):
            response = await client.post("/api/item/add", json={"name": "AK-47", "price": 100})
            response_body = response.json()
            assert response.status_code == 200
            assert response_body.get("status") == "ok"
