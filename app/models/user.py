
from ..database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, text, Text
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String)
    posts = relationship("Post", back_populates="owner")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))