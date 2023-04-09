from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
import secrets

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    tasks = relationship("Task", back_populates="user")


class Task(Base):
    __tablename__ = 'task'
    id = Column(String, primary_key=True, default=lambda: secrets.token_hex(16))
    title = Column(String, nullable=False)
    date_of_insertion = Column(DateTime, nullable=False, default=datetime.now())
    date_to_conclude = Column(DateTime, nullable=False)
    text = Column(String)
    concluded = Column(Boolean, default=False)
    trashed = Column(Boolean, default=False)
    user_id = Column(String, ForeignKey('user.id'))
    user = relationship("User", back_populates="tasks")
    color = Column(String, nullable=False)
