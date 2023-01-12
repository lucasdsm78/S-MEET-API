from typing import List

from pydantic import BaseModel


# Article inside UserDisplay
class Article(BaseModel):
    title: str
    content: str
    published: bool

    class Config():
        orm_mode = True


# User inside ArticleDisplay
class User(BaseModel):
    id: int
    username: str

    class Config():
        orm_mode = True


# article that we receive

class ArticleBase(BaseModel):
    title: str
    content: str
    published: bool
    creator_id: int


# Return the response, type fo data we provide
class ArticleDisplay(BaseModel):
    title: str
    content: str
    published: bool
    user: User

    class Config():
        orm_mode = True


# type of data we receive

class UserBase(BaseModel):
    username: str
    email: str
    password: str


# Return the response, type fo data we provide

class UserDisplay(BaseModel):
    username: str
    email: str
    items: List[Article] = []

    class Config():
        orm_mode = True


class ProductBase(BaseModel):
    title: str
    description: str
    price: float
