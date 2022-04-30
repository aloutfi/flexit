import datetime

from pydantic import BaseModel


class Category(BaseModel):
    _category_id: int | None
    category: str

    class Config:
        orm_mode = True
        underscore_attrs_are_private = True


class Person(BaseModel):
    _person_id: int | None
    person: str

    class Config:
        orm_mode = True
        underscore_attrs_are_private = True


class Show(BaseModel):
    _show_id: str | None
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
        underscore_attrs_are_private = True
