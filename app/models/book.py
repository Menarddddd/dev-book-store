from ..database.database import Base
from sqlalchemy import JSON, Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    genre = Column(JSON)
    member_type = Column(String)
    available = Column(Boolean)
    order_id = Column(Integer, ForeignKey("orders.id")) 
    seller_id = Column(Integer, ForeignKey("sellers.id"))


    order = relationship("Order", back_populates="books")
    seller = relationship("Seller", back_populates="property")