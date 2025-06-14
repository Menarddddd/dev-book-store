from ..database.database import Base
from sqlalchemy import JSON, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    genre = Column(JSON)
    price = Column(Integer)
    available = Column(Boolean)
    seller_id = Column(Integer, ForeignKey("sellers.id"))

    seller = relationship("Seller", back_populates="property") 