from fastapi import APIRouter, status, Depends
from typing import List
from sqlalchemy.orm import Session
from ..schemas.user_schema import UserResponse, User
from ..database import get_db
from ..oauth2 import get_current_user
from ..services import user_service

router = APIRouter(
    prefix='/users',
    tags=['User']
)


@router.get('/', response_model=List[UserResponse])
def read_users(db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    return user_service.read_users(db, current_user)


@router.get('/{user_id}', response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return user_service.read_user(user_id, db, current_user)


@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: User, db: Session = Depends(get_db)):
    return user_service.create_user(user, db)


@router.put('/{user_id}', response_model=UserResponse)
def update_user(user_id: int, user_data: User, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return user_service.update_user(user_id, user_data, db, current_user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    return user_service.delete_user(user_id, db, current_user)
