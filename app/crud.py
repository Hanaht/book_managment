from sqlalchemy.orm import Session
from . import models

def create_book(db: Session, title: str, author: str, published_date: str, number_of_pages: int):
    db_book = models.Book(title=title, author=author, publishedDate=published_date, numberOfPages=number_of_pages)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def update_book(db: Session, book_id: int, title: str, author: str, published_date: str, number_of_pages: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    db_book.title = title
    db_book.author = author
    db_book.publishedDate = published_date
    db_book.numberOfPages = number_of_pages
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    db.delete(db_book)
    db.commit()
    return db_book
