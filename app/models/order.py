from ..database.database import Base
from sqlalchemy import JSON, Column, DateTime, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("users.id"))
    books_id = Column(JSON)
    time_order = Column(DateTime)
    original_price = Column(Integer)
    discounted_price = Column(Integer)
    total_amount = Column(Integer)

    customer = relationship("User", back_populates="orders")
 