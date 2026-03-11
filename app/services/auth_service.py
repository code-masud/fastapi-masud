from fastapi import Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..schemas.user_schema import User
from ..database import get_db
from ..models.user import User
from ..utils import verify_password
from ..oauth2 import create_access_token
from ..schemas.token_schema import Token


def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.username).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )

    if not verify_password(credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
        )

    access_token = create_access_token(data={'user_id': user.id})
    return {'access_token': access_token, 'token_type': 'bearer'}
