from fastapi import FastAPI
from .models.user import User
from .models.book import Book
from .models.order import Order
from .models.seller import Seller
from .database.database import Base, engine
from .routes import user_routes


app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_routes.route)
