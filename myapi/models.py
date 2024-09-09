from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
class Post(Base):
  __tablename__ = 'posts'
  id = Column(Integer, primary_key=True,nullable=False)
  title = Column(String, nullable=False)
  body = Column(String, nullable=False)
  published = Column(Boolean, default=True)
  ratings = Column(Integer, nullable=False, default=0)
  user_id = Column(Integer, ForeignKey("users.id", ondelete='CASCADE'), nullable=False, )
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
  owner = relationship("User")
  
  
class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key=True,nullable=False)
  email = Column(String, nullable=False, unique=True)
  password = Column(String, nullable=False)
  created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

  
  
