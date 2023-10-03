from app.handlers.base_handler import BaseHandler
from app.models.user.requests import NewUserRequest
from app.models.user.responses import StatusOkResponse
from app.gateways.mysql_gateway import LocalMysql
from fastapi.exceptions import HTTPException


class NewUserHandler(BaseHandler):
    @classmethod
    async def handle(cls, request: NewUserRequest):
        if await cls._is_user_exists(request.name):
            raise HTTPException(status_code=409, detail=f"User with name {request.name} already exists")
        await cls._create_user(request)
        return StatusOkResponse()

    @staticmethod
    async def _create_user(user: NewUserRequest):
        sql = """
            INSERT INTO users ({columns})
            VALUES({placeholders})
        """
        args = tuple(value for key, value in user.model_dump().items())
        template = user.model_dump()
        columns = ", ".join(key for key, value in template.items())
        placeholders = ", ".join(["%s"] * len(template))
        sql = sql.format(columns=columns, placeholders=placeholders)
        await LocalMysql().execute(sql, args)

    @staticmethod
    async def _is_user_exists(name: str) -> bool:
        sql = """
            SELECT * FROM users
            WHERE `name`="{value}"
            LIMIT 1;
        """
        sql = sql.format(value=name)
        if await LocalMysql().select(sql):
            return True
        return False
