from ..database.database import Base
from sqlalchemy import Boolean, Column, String, Integer
from sqlalchemy.orm import relationship


class Seller(Base):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    balance = Column(Integer, default=1000)
    username = Column(String)
    password = Column(String)
    role = Column(String) 

    property = relationship("Book", back_populates="seller")
