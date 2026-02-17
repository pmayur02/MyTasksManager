from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database.db import Base
from datetime import datetime
import enum


class UserStatus(enum.Enum):
    active = "active"
    inactive = "inactive"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False,unique=True)
    password = Column(String(200), nullable=False)
    status = Column(Enum(UserStatus, name="user_status"),default=UserStatus.active,nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    tasks = relationship("Task",back_populates="user",cascade="all, delete")



class TaskStatus(enum.Enum):
    pending = "pending"
    in_progress = "in-progress"
    complete = "complete"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    description = Column(String(200), nullable=False)
    status = Column(Enum(TaskStatus, name="task_status"),default=TaskStatus.pending,nullable=False)
    user_id = Column(Integer,  ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="tasks")
