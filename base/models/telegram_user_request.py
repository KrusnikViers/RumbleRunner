from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from base.models.base import BaseDBModel


class TelegramUserRequest(BaseDBModel):
    __tablename__ = 'telegram_user_request'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)

    telegram_user_id = Column(Integer, ForeignKey("telegram_user.id"), nullable=False)
    telegram_user = relationship("TelegramUser", back_populates="requests")

    telegram_group_id = Column(Integer, ForeignKey("telegram_group.id"), nullable=True)
    telegram_group = relationship("TelegramGroup", back_populates="user_requests")
