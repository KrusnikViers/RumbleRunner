from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship

from app.internal.storage.models.base import BaseDBModel


class TelegramUserInGroup(BaseDBModel):
    __tablename__ = 'telegram_user_in_group'

    telegram_user_id = Column(ForeignKey('telegram_user.id'), primary_key=True, nullable=False)
    telegram_user = relationship("TelegramUser", back_populates="memberships")

    telegram_group_id = Column(ForeignKey('telegram_group.id'), primary_key=True, nullable=False)
    telegram_group = relationship("TelegramGroup", back_populates="members")
