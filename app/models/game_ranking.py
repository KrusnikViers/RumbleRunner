from sqlalchemy import Column, Integer, BigInteger
from sqlalchemy.orm import relationship

from base.api.models import BaseDBModel


class GameRanking(BaseDBModel):
    __tablename__ = 'game_ranking'

    id = Column(Integer, autoincrement=True, primary_key=True)

    tg_group_id = Column(BigInteger, nullable=False, unique=True)

    game_sessions = relationship("GameSession", back_populates="game_ranking", cascade="all, delete")
    players = relationship("Player", back_populates="game_ranking", cascade="all, delete")
