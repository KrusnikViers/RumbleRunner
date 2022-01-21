from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from base.api.models import BaseDBModel


class Participation(BaseDBModel):
    __tablename__ = 'participation'

    id = Column(Integer, autoincrement=True, primary_key=True)

    is_winner = Column(Boolean, nullable=False)

    game_session_id = Column(ForeignKey('game_session.id'), nullable=True)
    game_session = relationship("GameSession")
    match_number = Column(Integer, nullable=False)

    player_id = Column(ForeignKey('player.id'), nullable=False)
    player = relationship("Player")
