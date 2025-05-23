from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, TIMESTAMP, func
from sqlalchemy.orm import relationship


    
class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

class Post(Base):

    __tablename__ = "posts"

    id= Column(Integer, primary_key=True, nullable=False)
    title= Column(String, nullable=False)
    content= Column(String, nullable=False)
    published= Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    category = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE") )
    owner = relationship("User")

class vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)

       