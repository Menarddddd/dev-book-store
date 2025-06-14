from ..schemas.book_schemas import CreateBook
from sqlalchemy.orm import Session
from ..models.book import Book
from fastapi.responses import JSONResponse
from fastapi import status



def create_book(book: CreateBook, db: Session, seller_id: int):
    new_book = Book(
        title = book.title,
        author = book.author,
        genre = book.genre,
        price = book.price,
        available = book.available,
        seller_id = seller_id
    )

    db.add(new_book)
    db.commit()

    return JSONResponse(
        status_code = status.HTTP_201_CREATED,
        content = {"message": f"Book {book.title} is for sale now!"}

    )
