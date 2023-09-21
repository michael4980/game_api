from app.handlers.base_handler import BaseHandler
from app.models.item.requests import NewItemRequest
from app.models.user.responses import StatusOkResponse
from app.gateways.mysql_gateway import LocalMysql
from fastapi.exceptions import HTTPException


class NewItemHandler(BaseHandler):
    @classmethod
    async def handle(cls, request: NewItemRequest):
        if item_exists := await cls._check_item_existance(request.name):
            raise HTTPException(status_code=409, detail=f"Item with name {request.name} already exists")
        await cls._create_item(request)
        return StatusOkResponse()

    @staticmethod
    async def _create_item(item: NewItemRequest):
        sql = """
            INSERT INTO items ({columns})
            VALUES({placeholders})
        """
        args = tuple(value for key, value in item.model_dump().items())
        template = item.model_dump()
        columns = ", ".join(key for key, value in template.items())
        placeholders = ", ".join(["%s"] * len(template))
        sql = sql.format(columns=columns, placeholders=placeholders)
        await LocalMysql().execute(sql, args)

    @staticmethod
    async def _check_item_existance(name: str) -> bool:
        sql = """
            SELECT * FROM items
            WHERE `name`="{value}"
            LIMIT 1;
        """
        sql = sql.format(value=name)
        if response := await LocalMysql().select(sql):
            return True
        return False
