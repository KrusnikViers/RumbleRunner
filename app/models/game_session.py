from sqlalchemy import Boolean, Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from base.api.models import BaseDBModel


class GameSession(BaseDBModel):
    __tablename__ = 'game_session'

    id = Column(Integer, autoincrement=True, primary_key=True)

    start_time = Column(DateTime(timezone=True), server_default=func.now())
    is_ongoing = Column(Boolean, nullable=False, default=False)

    game_ranking_id = Column(ForeignKey('game_ranking.id'), nullable=False)
    game_ranking = relationship("GameRanking", back_populates="game_sessions")

    players = relationship("Player", back_populates="game_session")
    participations = relationship("Participation", back_populates="game_session", cascade="all, delete")
