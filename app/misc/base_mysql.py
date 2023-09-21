import aiomysql
import os
from app.misc.singleton import Singleton
from typing import Optional


class MysqlGateway(metaclass=Singleton):
    __slots__ = ("__db_config", "__pool", "env_prefix")

    def __init__(self, db_env_prefix: Optional[str] = None):
        self.env_prefix = db_env_prefix
        self.__db_config = {
            "host": os.getenv(self.env_prefix + "_HOST"),
            "port": int(os.getenv(self.env_prefix + "_PORT") or 3306),
            "user": os.getenv(self.env_prefix + "_USERNAME") or os.getenv(self.env_prefix + "_USER"),
            "password": os.getenv(self.env_prefix + "_PASSWORD"),
            "db": os.getenv(self.env_prefix + "_DB"),
        }

    async def __aenter__(self):
        if not self.__db_config:
            raise ValueError("self.db_config must be set")
        for option in ("host", "port", "user", "password"):
            if not self.__db_config.get(option, None):
                raise ValueError(f"self.db_config.{option} must be set")

        await self.__create_pool()

    async def __create_pool(self):
        self.__pool = await aiomysql.create_pool(
            host=self.__db_config["host"],
            port=self.__db_config["port"],
            user=self.__db_config["user"],
            password=self.__db_config["password"],
            db=self.__db_config["db"],
            maxsize=10,
            autocommit=True,
            pool_recycle=600,
        )

    async def __aexit__(self, exc_type, exc, tb):
        self.__pool.close()
        await self.__pool.wait_closed()

    async def __execute_cursor(self, cur, sql, args):
        sql = sql.replace("?", "%s")
        await cur.execute(query=sql, args=args)

    async def __execute(self, sql, args):
        async with self.__pool.acquire() as conn:
            cur = await conn.cursor()
            await self.__execute_cursor(cur=cur, sql=sql, args=args)
            await cur.close()
            return cur

    async def execute(self, sql, args=()):
        return await self.__execute(sql=sql, args=args)

    async def __select(self, sql, args, size):
        async with self.__pool.acquire() as conn:
            cur = await conn.cursor(aiomysql.DictCursor)
            await self.__execute_cursor(cur=cur, sql=sql, args=args)

        if size:
            rs = await cur.fetchmany(size)
        else:
            rs = await cur.fetchall()
        await cur.close()
        return rs

    async def select(self, sql, args=(), size=None):
        return await self.__select(sql=sql, args=args, size=size)
