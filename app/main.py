from dotenv import load_dotenv
from fastapi import FastAPI

from app.routes.user import router as user_router
from app.routes.item import router as item_router
from app.service import Service

load_dotenv()

app = FastAPI(title="game-api")

app.include_router(user_router)
app.include_router(item_router)
service = Service(app)


@app.on_event("startup")
async def _startup() -> None:
    await service.start_and_wait()


@app.on_event("shutdown")
async def _shutdown() -> None:
    await service.shutdown()
