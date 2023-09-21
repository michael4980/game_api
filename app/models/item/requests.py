from pydantic import BaseModel


class BuyItemRequest(BaseModel):
    user_id: str
    item_name: str


class NewItemRequest(BaseModel):
    name: str
    price: int
