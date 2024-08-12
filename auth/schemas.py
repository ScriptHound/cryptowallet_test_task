from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str
    full_name: str
    disabled: bool = False

    class Config:
        from_attributes = True


class UserInDB(User):
    hashed_password: str
