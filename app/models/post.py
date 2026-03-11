
from ..database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, ForeignKey, Integer, String, text, Text
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True, index=True)
    content = Column(Text, nullable=False)
    author = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    published = Column(Boolean, server_default='True', index=True)
    owner = relationship("User", back_populates="posts")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))