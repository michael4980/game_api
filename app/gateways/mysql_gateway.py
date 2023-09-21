from app.misc.base_mysql import MysqlGateway


class LocalMysql(MysqlGateway):
    def __init__(self) -> None:
        super().__init__("LOCAL_MYSQL")
