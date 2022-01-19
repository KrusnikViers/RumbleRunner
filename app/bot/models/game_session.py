from sqlalchemy import Boolean
from sqlalchemy import Column, Integer, DateTime, func

from app.public.models import BaseDBModel


class GameSession(BaseDBModel):
    __tablename__ = 'game_session'

    id = Column(Integer, autoincrement=True, primary_key=True)

    start_time = Column(DateTime(timezone=True), server_default=func.now())
    is_ongoing = Column(Boolean, nullable=False, default=False)
