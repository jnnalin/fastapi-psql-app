import uuid
from typing import Union

from pydantic import BaseModel


class ItemResponse(BaseModel):
    id: Union[str, uuid.UUID]
    name: str
    description: str
    price: float
    quantity: int
    user_id: Union[str, uuid.UUID]


class UserCreate1(BaseModel):
    username: str


class UserResponse(UserCreate1):
    id: Union[str, uuid.UUID]


class DatabaseRequest(BaseModel):
    customer_count: int = 500
    product_count: int = 10000
    order_count: int = 20000

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str