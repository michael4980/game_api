from pydantic import BaseModel, Field
from typing import Literal


class User(BaseModel):
    id: int
    name: str
    points: int


class StatusOkResponse(BaseModel):
    status: Literal["ok"] = "ok"


class UserAlreadyExists(BaseModel):
    message: str = Field(description="User with this name already exists")


class UserNotFound(BaseModel):
    message: str = Field(description="User was not found")
