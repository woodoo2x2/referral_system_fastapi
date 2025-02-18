from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime

from app.database.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    registration_date = Column(DateTime, default=datetime.utcnow)

    referral_code  = Column(String, nullable=True, default=None)
    inviter_code  = Column(String, nullable=True, default=None)
