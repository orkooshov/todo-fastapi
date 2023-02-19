from sqlalchemy import MetaData, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.types import String
from datetime import datetime
from enum import IntEnum

from app.database.mixins import TimestampMixin


_metadata = MetaData()


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True)
    metadata = _metadata


class Gender(IntEnum):
    UNKNOWN = 0
    MALE = 1
    FEMALE = 2


class User(Base):
    __tablename__ = 'user'

    username: Mapped[str] = mapped_column(String(64), unique=True)
    password: Mapped[str] = mapped_column(String(64))
    first_name: Mapped[str] = mapped_column(String(64), default='')
    last_name: Mapped[str] = mapped_column(String(64), default='')
    middle_name: Mapped[str] = mapped_column(String(64), default='')
    email: Mapped[str] = mapped_column(String(64), unique=True, default='')
    gender: Mapped[Gender] = mapped_column(default=Gender.UNKNOWN)
    tasks: Mapped[list['Task']] = relationship(back_populates='user')


class Task(Base, TimestampMixin):
    __tablename__ = 'task'

    title: Mapped[str] = mapped_column(String(32))
    description: Mapped[str] = mapped_column(String(128), default='')
    is_done: Mapped[bool] = mapped_column(default=False)
    is_favorite: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id, ondelete='CASCADE'))
    user: Mapped[User] = relationship(back_populates='tasks')
    date_until: Mapped[datetime] = mapped_column(nullable=True)
    subtasks: Mapped[list['Subtask']] = relationship(back_populates='task')


class Subtask(Base):
    __tablename__ = 'subtask'

    title: Mapped[str] = mapped_column(String(32))
    is_done: Mapped[bool] = mapped_column(default=False)
    task_id: Mapped[int] = mapped_column(ForeignKey(Task.id, ondelete='CASCADE'))
    task: Mapped[Task] = relationship(back_populates='subtasks')
