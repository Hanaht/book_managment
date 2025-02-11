from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, crud, database

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.post("/api/books")
def add_book(title: str, author: str, published_date: str, number_of_pages: int, db: Session = Depends(database.get_db)):
    return crud.create_book(db, title, author, published_date, number_of_pages)

@app.get("/api/books")
def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_books(db, skip=skip, limit=limit)

@app.get("/api/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(database.get_db)):
    db_book = crud.get_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.put("/api/books/{book_id}")
def update_book(book_id: int, title: str, author: str, published_date: str, number_of_pages: int, db: Session = Depends(database.get_db)):
    db_book = crud.update_book(db, book_id, title, author, published_date, number_of_pages)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.delete("/api/books/{book_id}")
def delete_book(book_id: int, db: Session = Depends(database.get_db)):
    db_book = crud.delete_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted"}
