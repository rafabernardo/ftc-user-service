from sqlalchemy import Boolean, Column, Integer, String

from src.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    is_reader = Column(Boolean, default=True)  # Default role
    is_editor = Column(Boolean, default=False)
