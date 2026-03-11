from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database import get_db
from ..utils import get_password_hash
from ..oauth2 import get_current_user
from ..schemas.user_schema import User, UserResponse
from ..models.user import User


def read_users(db: Session = Depends(get_db), current_user: UserResponse = Depends(get_current_user)):
    users = db.query(User).all()
    return users


def read_user(user_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User id: {user_id} not found')
    return user


def create_user(user: User, db: Session = Depends(get_db)):
    user.password = get_password_hash(user.password)
    db_user = User(**user.model_dump())

    db.add(db_user)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')
    db.refresh(db_user)
    return db_user


def update_user(user_id: int, user_data: User, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User id: {user_id} not found')

    for field, value in user_data.model_dump().items():
        if field == 'password':
            setattr(db_user, field, get_password_hash(value))
        else:
            setattr(db_user, field, value)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e}')
    db.refresh(db_user)
    return db_user


def delete_user(user_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'User id: {user_id} not found')

    db.delete(user)
    db.commit()
