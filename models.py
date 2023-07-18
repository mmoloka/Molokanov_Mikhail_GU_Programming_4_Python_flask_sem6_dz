from pydantic import BaseModel, ConfigDict, Field, EmailStr
from settings import settings
from datetime import date


class OrderIn(BaseModel):
    user_id: int
    product_id: int
    order_date: date = Field(..., format='%Y-%m-%d')
    status: bool


class Order(OrderIn):
    id: int


class UserIn(BaseModel):
    first_name: str = Field(..., min_length=2, max_length=settings.NAME_MAX_LENGTH)
    last_name: str = Field(..., min_length=2, max_length=settings.NAME_MAX_LENGTH)
    email: EmailStr = Field(..., max_length=settings.EMAIL_MAX_LENGTH)
    password: str = Field(..., min_length=8, max_length=128, pattern='[A-Z][a-z][0-9]')


class User(UserIn):
    id: int
    orders: list[Order] = []


class ProductIn(BaseModel):
    title: str = Field(..., min_length=5, max_length=settings.TITLE_MAX_LENGTH)
    description: str = Field(max_length=settings.DESCRIPTION_MAX_LENGTH)
    price: float


class Product(ProductIn):
    id: int
    orders: list[Order] = []
