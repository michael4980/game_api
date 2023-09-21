from app.handlers.base_handler import BaseHandler
from app.models.item.requests import BuyItemRequest
from app.gateways.mysql_gateway import LocalMysql
from app.models.item.responses import BuyItemResponse
from fastapi.exceptions import HTTPException


class BuyItemHandler(BaseHandler):
    @classmethod
    async def handle(cls, request: BuyItemRequest):
        points = await cls._get_points_amount(request.user_id)
        if points is None:
            raise HTTPException(status_code=404, detail=f"User with id {request.user_id} not found")
        price = await cls._get_item_price(request.item_name)
        if price is None:
            raise HTTPException(status_code=404, detail=f"Item with name {request.item_name} not found")
        if points < price:
            raise HTTPException(
                status_code=400, detail=f"You haven`t enough points: {points} to buy this item with price: {price}"
            )
        await cls._buy_item(request.user_id, price)
        return BuyItemResponse(balance_remain=points - price)

    @staticmethod
    async def _get_points_amount(user_id: str) -> int | None:
        sql = """
            SELECT points FROM users
            WHERE `id`="{value}";
        """
        sql = sql.format(value=user_id)
        if response := await LocalMysql().select(sql):
            return response[0].get("points")
        return None

    @staticmethod
    async def _get_item_price(name: str) -> int | None:
        sql = """
            SELECT price FROM items
            WHERE `name`="{value}";
        """
        sql = sql.format(value=name)
        if response := await LocalMysql().select(sql):
            return response[0].get("price")
        return None

    @staticmethod
    async def _buy_item(user_id: str, price: str):
        sql = """
            UPDATE users
            SET `points` = `points` - "{value}"
            WHERE `id` = "{id}"
        """
        sql = sql.format(id=user_id, value=price)
        response = await LocalMysql().execute(sql)
        return response
