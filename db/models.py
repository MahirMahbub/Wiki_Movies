from fastapi_users import models as user_models, FastAPIUsers
from fastapi_users.authentication import JWTAuthentication
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

from .database import Base, database


class User(user_models.BaseUser):
    pass


class UserCreate(user_models.BaseUserCreate):
    # @validator('password')
    # def valid_password(cls, v: str):
    #     if len(v) < 6:
    #         raise ValueError('Password should be at least 6 characters')
    #     return v
    pass


class UserUpdate(User, user_models.BaseUserUpdate):
    pass


class UserDB(User, user_models.BaseUserDB):
    pass


class UserTable(Base, SQLAlchemyBaseUserTable):
    pass


SECRET = "SECRET"
users = UserTable.__table__
user_db = SQLAlchemyUserDatabase(UserDB, database, users)
jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=3600, tokenUrl="/auth/jwt/login")
fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)
