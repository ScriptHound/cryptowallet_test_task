from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Body
import bcrypt

from auth.containers import UserContainer
from auth.schemas import User
from auth.services import UserService

router = APIRouter()


def hash_password(password: str) -> str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password_bytes = bcrypt.hashpw(password_bytes, salt)
    hashed_password = hashed_password_bytes.decode('utf-8')
    return hashed_password


@router.post("/user")
@inject
async def create_user(
    username: str = Body(...),
    password: str = Body(...),
    email: str = Body(...),
    full_name: str = Body(...),
    user_service: UserService = Depends(Provide[UserContainer.user_service])
):
    hashed_password = hash_password(password)
    user = User(username=username, email=email, full_name=full_name, hashed_password=hashed_password)
    await user_service.create_user(user)
