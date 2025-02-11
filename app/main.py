from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, crud, database
from database import SessionLocal, engine  
from .auth import create_access_token, authenticate_user, get_current_user
from pydantic import BaseModel
from models import User
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

@app.post("/api/books")
def add_book(title: str, author: str, published_date: str, number_of_pages: int, db: Session = Depends(database.get_db), current_user: User = Depends(get_current_user)):
    return crud.create_book(db, title, author, published_date, number_of_pages)

@app.get("/api/books")
def get_books(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db), current_user: User = Depends(get_current_user)):
    return crud.get_books(db, skip=skip, limit=limit)

@app.get("/api/books/{book_id}")
def get_book(book_id: int, db: Session = Depends(database.get_db),current_user: User = Depends(get_current_user)):
    
    db_book = crud.get_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.put("/api/books/{book_id}")
def update_book(book_id: int, title: str, author: str, published_date: str, number_of_pages: int, db: Session = Depends(database.get_db),current_user: User = Depends(get_current_user)):
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

class LoginRequest(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    username: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/token", response_model=str)
def login_for_access_token(
    form_data: LoginRequest, db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
