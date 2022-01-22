from sqlalchemy import Column, Integer, BigInteger, String
from sqlalchemy.orm import relationship

from base.models.base import BaseDBModel


class TelegramGroup(BaseDBModel):
    __tablename__ = 'telegram_group'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(BigInteger, nullable=False, unique=True)

    name = Column(String, nullable=False)

    user_requests = relationship("TelegramUserRequest", back_populates="telegram_group", cascade="all, delete")
    members = relationship("TelegramUserInGroup", back_populates="telegram_group", cascade="all, delete")
