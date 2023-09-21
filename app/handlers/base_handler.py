from abc import ABCMeta, abstractmethod


class BaseHandler(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    async def handle(cls):
        pass
