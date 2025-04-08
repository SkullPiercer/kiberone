from fastapi import APIRouter
from fastapi.params import Depends

from app.core.user import auth_backend, fastapi_users, current_user
from app.models import User
from app.schemas.user import UserCreate, UserRead, UserUpdate

router = APIRouter()


@router.get("me")
def get_users_data(user: User = Depends(current_user)):
    return user.email


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

users_router = fastapi_users.get_users_router(UserRead, UserUpdate)

users_router.routes = [
    rout for rout in users_router.routes if rout.name != "users:delete_user"
]

router.include_router(
    users_router,
    prefix="/users",
    tags=["users"],
)
