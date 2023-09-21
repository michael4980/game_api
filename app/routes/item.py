from fastapi import APIRouter, Depends

from app.misc.helpers import check_static_token
from app.handlers.item.item_handler import BuyItemHandler
from app.handlers.item.add_item_handler import NewItemHandler
from app.models.item.requests import BuyItemRequest, NewItemRequest
from app.models.user.responses import StatusOkResponse
from app.models.item.responses import BuyItemResponse, InsuficcientBalance, ItemAlreadyExists

router = APIRouter(prefix="/api/item", tags=["Item"])


@router.post(
    "/buy",
    dependencies=[Depends(check_static_token)],
    responses={200: {"model": BuyItemResponse}, 400: {"model": InsuficcientBalance}},
)
async def buy_item(request: BuyItemRequest):
    return await BuyItemHandler.handle(request)


@router.post(
    "/add",
    dependencies=[Depends(check_static_token)],
    responses={200: {"model": StatusOkResponse}, 409: {"model": ItemAlreadyExists}},
)
async def add_new_item(request: NewItemRequest):
    return await NewItemHandler.handle(request)
