from datetime import datetime
from sqlalchemy import BigInteger, String, Integer, Float, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import enum

class Base(DeclarativeBase):
    pass

class TaskStatus(enum.Enum):
    PENDING = "pending"
    DONE = "done"
    FAILED = "failed"

class FinanceType(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"
    ASSET = "asset"

class MetricCategory(enum.Enum):
    SPORT = "sport"
    STUDY = "study"
    PROJECT = "project"

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)  # Telegram user ID
    balance: Mapped[float] = mapped_column(Float, default=0.0)
    registered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    tasks: Mapped[list["Task"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    goals: Mapped[list["Goal"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    finances: Mapped[list["Finance"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    metrics: Mapped[list["Metric"]] = relationship(back_populates="user", cascade="all, delete-orphan")

class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), default=TaskStatus.PENDING)
    due_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    reward: Mapped[float] = mapped_column(Float, default=10.0)

    user: Mapped["User"] = relationship(back_populates="tasks")

class Goal(Base):
    __tablename__ = 'goals'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    title: Mapped[str] = mapped_column(String(255))
    target_value: Mapped[float] = mapped_column(Float)
    current_value: Mapped[float] = mapped_column(Float, default=0.0)
    deadline: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    user: Mapped["User"] = relationship(back_populates="goals")

class Finance(Base):
    __tablename__ = 'finances'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    type: Mapped[FinanceType] = mapped_column(Enum(FinanceType))
    name: Mapped[str] = mapped_column(String(255))
    amount: Mapped[float] = mapped_column(Float)

    user: Mapped["User"] = relationship(back_populates="finances")

class Metric(Base):
    __tablename__ = 'metrics'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    category: Mapped[MetricCategory] = mapped_column(Enum(MetricCategory))
    name: Mapped[str] = mapped_column(String(255))
    value: Mapped[float] = mapped_column(Float)
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="metrics")
