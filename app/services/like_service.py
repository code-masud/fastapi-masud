from fastapi import Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user
from ..schemas.user_schema import UserResponse
from ..schemas.like_schema import LikeRequest
from ..models.like import Like
from ..models.post import Post


def like(like_data: LikeRequest, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    post = db.get(Post, like_data.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Post id: {like_data.post_id} not found')

    query = db.query(Like).filter(
        Like.user_id == current_user.id, Like.post_id == like_data.post_id)

    db_like = query.first()

    if like_data.like:
        if db_like:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail='Already liked')

        new_like = Like(user_id=current_user.id, post_id=like_data.post_id)
        db.add(new_like)
        db.commit()
        return {'message': 'Like successfully.'}
    else:
        if not db_like:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Like not found')

        query.delete(synchronize_session=False)
        db.commit()
        return {'message': 'Unlike successfully.'}
