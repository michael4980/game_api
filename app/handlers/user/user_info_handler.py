from app.handlers.base_handler import BaseHandler
from app.models.user.responses import User
from app.gateways.mysql_gateway import LocalMysql
from fastapi.exceptions import HTTPException


class UserInfoHandler(BaseHandler):
    @classmethod
    async def handle(cls, user_id: str) -> User | None:
        if user := await cls._get_user_info(user_id):
            return User(**user)
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

    @staticmethod
    async def _get_user_info(user_id: str) -> dict | None:
        sql = """
            SELECT * FROM users
            WHERE `id`="{value}";
        """
        sql = sql.format(value=user_id)
        if response := await LocalMysql().select(sql):
            return response[0]
        return None
