from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str
    description: str

class BookResponse(BookCreate):
    id: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True
