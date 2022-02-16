from pydantic import BaseModel
import datetime


class Category(BaseModel):
    category_id: int | None
    category: str

    class Config:
        orm_mode = True


class Person(BaseModel):
    person_id: int | None
    person: str

    class Config:
        orm_mode = True


class Show(BaseModel):
    show_id: str | None
    type: str
    title: str
    director: Person | None
    country: str | None
    date_added: datetime.date | None
    release_year: int
    rating: str | None
    duration: str | None
    description: str
    categories: list[Category] | None = None
    actors: list[Person] | None = None

    class Config:
        orm_mode = True
