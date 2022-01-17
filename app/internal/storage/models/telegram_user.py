from sqlalchemy import Column, String, Integer, BigInteger
from sqlalchemy.orm import relationship

from app.internal.storage.models.base import BaseDBModel


class TelegramUser(BaseDBModel):
    __tablename__ = 'telegram_user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(BigInteger, nullable=False, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String)
    username = Column(String)

    requests = relationship("TelegramUserRequest", back_populates="telegram_user")
    memberships = relationship("TelegramUserInGroup", back_populates="telegram_user")
