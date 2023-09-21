from pydantic import BaseModel, Field


class NewUserRequest(BaseModel):
    name: str
    points: int


class AddPointsRequest(BaseModel):
    points_amount: int = Field(..., gt=0)
