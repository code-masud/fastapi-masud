from datetime import datetime
from .user_schema import UserResponse
from pydantic import BaseModel


class Post(BaseModel):
    title: str
    slug: str
    content: str
    published: bool


class PostResponse(Post):
    id: int
    created_at: datetime
    owner: UserResponse


class PostWithLikes(BaseModel):
    Post: PostResponse
    likes: int
