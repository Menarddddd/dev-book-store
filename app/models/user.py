from ..database.database import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    balance = Column(Integer, default=1000)
    username = Column(String)
    password = Column(String)
    member_type = Column(String)

    orders = relationship("Order", back_populates="customer")