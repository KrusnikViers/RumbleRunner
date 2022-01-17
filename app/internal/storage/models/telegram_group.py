from sqlalchemy import Column, Integer, BigInteger
from sqlalchemy.orm import relationship

from app.internal.storage.models.base import BaseDBModel


class TelegramGroup(BaseDBModel):
    __tablename__ = 'telegram_group'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(BigInteger, nullable=False, unique=True)

    user_requests = relationship("TelegramUserRequest", back_populates="telegram_group")
    members = relationship("TelegramUserInGroup", back_populates="telegram_group")
