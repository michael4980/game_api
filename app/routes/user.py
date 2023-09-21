from fastapi import APIRouter, Depends
from app.models.user.responses import StatusOkResponse, UserAlreadyExists, UserNotFound, User
from app.models.user.requests import NewUserRequest, AddPointsRequest
from app.misc.helpers import check_static_token
from app.handlers.user.new_user_handler import NewUserHandler
from app.handlers.user.user_info_handler import UserInfoHandler
from app.handlers.user.user_delete_handler import DeleteUserHandler
from app.handlers.user.user_points_handler import UserPointsHandler

router = APIRouter(prefix="/api/user", tags=["User"])


@router.post(
    "/",
    dependencies=[Depends(check_static_token)],
    responses={200: {"model": StatusOkResponse}, 409: {"model": UserAlreadyExists}},
)
async def create_new_user(request: NewUserRequest):
    return await NewUserHandler.handle(request)


@router.get(
    "/{user_id}",
    dependencies=[Depends(check_static_token)],
    responses={200: {"model": User}, 404: {"model": UserNotFound}},
)
async def get_user_info(user_id: str):
    return await UserInfoHandler.handle(user_id)


@router.put(
    "/{user_id}",
    dependencies=[Depends(check_static_token)],
    responses={200: {"model": StatusOkResponse}, 404: {"model": UserNotFound}},
)
async def increase_points(user_id: str, request: AddPointsRequest) -> StatusOkResponse:
    return await UserPointsHandler.handle(user_id, request)


@router.delete("/{user_id}", dependencies=[Depends(check_static_token)])
async def delete_user(user_id: str) -> StatusOkResponse:
    return await DeleteUserHandler.handle(user_id)
