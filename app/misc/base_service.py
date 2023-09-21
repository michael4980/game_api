from contextlib import AsyncExitStack
from app.misc.singleton import Singleton
from asyncio import Task, create_task
from anyio import sleep


class BaseService(object, metaclass=Singleton):
    async def start_and_wait(self):
        task = create_task(self.start())
        await self.wait_started(task)
        if task.done() and (exception := task.exception()):
            raise exception

    def __init__(self, app=None):
        self.__resources = []
        self.resources = []
        self.started = False
        self.wait = 10000000000

    async def start(self) -> None:
        self.__resources.extend(self.resources)
        while 1:
            async with AsyncExitStack() as stack:
                [await stack.enter_async_context(resource) for resource in self.__resources]
                self.started = True
                await sleep(self.wait)

    async def wait_started(self, task: Task = None) -> None:
        while not (self.started or (task and task.done())):
            await sleep(0.1)

    async def shutdown(self):
        print("SHUTING DOWN")
