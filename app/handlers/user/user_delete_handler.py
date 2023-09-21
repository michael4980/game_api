from app.handlers.base_handler import BaseHandler
from app.gateways.mysql_gateway import LocalMysql
from fastapi.exceptions import HTTPException
from app.models.user.responses import StatusOkResponse


class DeleteUserHandler(BaseHandler):
    @classmethod
    async def handle(cls, user_id: str):
        if user_check := await cls._check_user_existance(user_id):
            await cls._delete_user(user_id)
            return StatusOkResponse()
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

    @staticmethod
    async def _check_user_existance(user_id: str) -> bool:
        sql = """
            SELECT * FROM users
            WHERE `id`="{value}"
            LIMIT 1;
        """
        sql = sql.format(value=user_id)
        if response := await LocalMysql().select(sql):
            return True
        return False

    @staticmethod
    async def _delete_user(user_id: str):
        sql = """
            DELETE FROM users
            WHERE `id` = "{id}"
        """
        sql = sql.format(id=user_id)
        response = await LocalMysql().execute(sql)
        return response
