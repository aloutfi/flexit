from pydantic import BaseModel
import datetime


class Category(BaseModel):
    category_id: int
    category: str

    class Config:
        orm_mode = True


class Person(BaseModel):
    person_id: int
    person: str

    class Config:
        orm_mode = True


class Show(BaseModel):
    show_id: str
    type: str
    title: str
    director: Person | None
    country: str | None
    date_added: datetime.date | None
    release_year: int
    rating: str | None
    duration: str | None
    description: str

    class Config:
        orm_mode = True
