
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, or_
from ..oauth2 import get_current_user
from ..database import get_db
from ..schemas.post_schema import Post
from ..schemas.user_schema import UserResponse
from ..models.post import Post
from ..models.like import Like


def read_posts(db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user),
               limit: int = 10, skip: int = 0, search: str = ""):
    post_query = (
        db.query(
            Post,
            func.count(Like.post_id).label("likes")
        )
        .outerjoin(Like, Post.id == Like.post_id)
        .group_by(Post.id)
    )

    post_query = post_query.filter(Post.author == current_user.id)

    if search:
        post_query = post_query.filter(
            or_(
                Post.title.contains(search),
                Post.content.contains(search)
            )
        )

    posts = post_query.limit(limit).offset(skip).all()

    return posts


def read_post(post_id: int, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    post_query = (
        db.query(
            Post,
            func.count(Like.post_id).label("likes")
        )
        .outerjoin(Like, Post.id == Like.post_id)
        .group_by(Post.id)
    )

    db_post = post_query.filter(
        Post.id == post_id, Post.author == current_user.id).first()
    return db_post


def create_post(post_data: Post, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    db_post = Post(
        **post_data.model_dump(),
        author=current_user.id
    )

    db.add(db_post)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')

    db.refresh(db_post)
    return db_post


def update_post(post_id: int, post_data: Post, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    db_post = db.get(Post, post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post id: {post_id} not found')

    if db_post.author != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'You are not authorized to perform the request')

    for field, value in post_data.model_dump().items():
        setattr(db_post, field, value)

    setattr(db_post, 'author', current_user.id)

    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')

    db.refresh(db_post)
    return db_post


def delete_post(post_id: int, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    db_post = db.get(Post, post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post id: {post_id} not found')

    if db_post.author != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'You are not authorized to perform the request')

    db.delete(db_post)
    db.commit()
