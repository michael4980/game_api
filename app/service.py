from app.misc.base_service import BaseService
from app.gateways.mysql_gateway import LocalMysql
from fastapi import FastAPI


class Service(BaseService):
    def __init__(self, app: FastAPI) -> None:
        super().__init__(app)
        self.resources = [LocalMysql()]
