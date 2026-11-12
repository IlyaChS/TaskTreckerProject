from sqlalchemy import Column, Integer, String, Boolean, Text
from app.database.db import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    is_completed = Column(Boolean, default=False)