from app.handlers.base_handler import BaseHandler
from app.models.user.requests import AddPointsRequest
from app.gateways.mysql_gateway import LocalMysql
from app.models.user.responses import StatusOkResponse
from fastapi.exceptions import HTTPException


class UserPointsHandler(BaseHandler):
    @classmethod
    async def handle(cls, user_id: str, request: AddPointsRequest):
        if await cls._check_user_existance(user_id):
            await cls._add_user_points(user_id, request.points_amount)
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
        if await LocalMysql().select(sql):
            return True
        return False

    @staticmethod
    async def _add_user_points(user_id: str, amount: int) -> None:
        sql = """
            UPDATE users
            SET `points` = `points` + "{value}"
            WHERE `id` = "{id}"
        """
        sql = sql.format(id=user_id, value=amount)
        response = await LocalMysql().execute(sql)
        return response
