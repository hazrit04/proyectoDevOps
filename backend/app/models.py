from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Text
from sqlalchemy import relationship
from app.database import Base
import datetime
from datetime import timezone

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    tokens = relationship("Token", back_populates="owner", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")

class Token(Base):
    __tablename__ = "tokens"

    token_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    token = Column(String, nullable=False)
    expire_date = Column(DateTime, nullable=False)

    owner = relationship("User", back_populates="tokens")

class Task(Base):
    __tablename__ = "tasks"

    task_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text)
    state = Column(String, nullable=False)
    creation_date = Column(DateTime, default=lambda: datetime.datetime.now(timezone.utc))
    due_date = Column(DateTime, nullable=True)

    owner = relationship("User", back_populates="tasks")
    history = relationship("TaskHistory", back_populates="task", uselist=False, cascade="all, delete-orphan")

class TaskHistory(Base):
    __tablename__ = "taskhistory"

    history_id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.task_id"), nullable=False)
    last_state = Column(String)
    actual_state = Column(String)
    change_date = Column(DateTime, default=lambda: datetime.datetime.now(timezone.utc))

    task = relationship("Task", back_populates="history")
