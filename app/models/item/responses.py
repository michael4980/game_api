from pydantic import BaseModel, Field
from typing import Literal


class Item(BaseModel):
    id: int
    name: str
    value: int


class InsuficcientBalance(BaseModel):
    message: str = Field(description="You don`t have enough balance to buy this item")


class ItemAlreadyExists(BaseModel):
    message: str = Field(description="Item with this name already exists")


class BuyItemResponse(BaseModel):
    balance_remain: int
    status: Literal["ok"] = "ok"
