from fastapi import APIRouter, Depends, status
from typing import List
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user
from ..schemas.user_schema import UserResponse
from ..schemas.post_schema import Post, PostResponse, PostWithLikes
from ..services import post_service

router = APIRouter(
    prefix='/posts',
    tags=['Post']
)


@router.get('/', response_model=List[PostWithLikes])
def read_posts(db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user),
               limit: int = 10, skip: int = 0, search: str = ""):
    return post_service.read_posts(db, current_user, limit, skip, search)


@router.get('/{post_id}', response_model=PostWithLikes)
def read_post(post_id: int, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    return post_service.read_post(post_id, db, current_user)


@router.post('/', response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post_data: Post, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    return post_service.create_post(post_data, db, current_user)


@router.put('/{post_id}', response_model=PostResponse)
def update_post(post_id: int, post_data: Post, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    return post_service.update_post(post_id, post_data, db, current_user)


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    return post_service.delete_post(post_id, db, current_user)
