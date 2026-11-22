from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator
from enum import Enum

from constants.roles import Roles

EMAIL_PATTERN = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

class Location(Enum):
    MSK = 'MSK'
    SPB = 'SPB'

class TestUser(BaseModel):
    __test__ = False
    """Тело запроса на создание пользователя (POST /register и POST /user)."""

    email: str = Field(..., pattern=EMAIL_PATTERN, description="Email пользователя")
    fullName: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=8, max_length=20)
    passwordRepeat: str = Field(..., min_length=8, max_length=20)
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        """passwordRepeat обязан совпадать с password."""
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("passwordRepeat не совпадает с password")
        return value

class RegisterUserResponse(BaseModel):
    """Ответ на POST /register и POST /user."""

    id: str
    email: str = Field(..., pattern=EMAIL_PATTERN)
    fullName: str = Field(..., min_length=1, max_length=100)
    verified: bool
    roles: list[Roles]
    createdAt: datetime

class Genre(BaseModel):
    name: str

class PostMovies(BaseModel):
    id: int
    name: str
    price: float
    description: str
    imageUrl: str | None
    location: Location
    published: bool
    genreId: int
    genre: Genre
    createdAt: datetime
    rating: float

class GetMoviesResponse(BaseModel):
    """Ответ на GET /movies"""
    movies: list[PostMovies]
    count: int
    page: int
    pageSize: int
    pageCount: int

