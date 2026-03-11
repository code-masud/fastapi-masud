from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user
from ..schemas.user_schema import UserResponse
from ..schemas.like_schema import LikeRequest
from ..services import like_service

router = APIRouter(
    prefix='/like',
    tags=['Like']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def like(like_data: LikeRequest, db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    return like_service.like(like_data, db, current_user)
