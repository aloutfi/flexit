from sqlalchemy import Column, Date, ForeignKey, Integer, SmallInteger, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Category(Base):
    __tablename__ = "categories"

    category_id = Column(
        SmallInteger,
        primary_key=True,
        unique=True,
        autoincrement=True
    )
    category = Column(Text, nullable=False)


class Person(Base):
    __tablename__ = "persons"

    person_id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )
    person = Column(Text, nullable=False)


class Show(Base):
    __tablename__ = "shows"

    show_id = Column(
        Integer, primary_key=True, unique=True, autoincrement=True
    )
    type = Column(Text)
    title = Column(Text)
    director_id = Column(ForeignKey("persons.person_id"))
    country = Column(Text)
    date_added = Column(Date)
    release_year = Column(Integer)
    rating = Column(Text)
    duration = Column(Text)
    description = Column(Text)

    director = relationship("Person", lazy="joined")


class ShowCastIntersection(Base):
    __tablename__ = "show_cast_intersection"

    show_id = Column(ForeignKey("shows.show_id"))
    person_id = Column(ForeignKey("persons.person_id"))
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    person = relationship("Person")
    show = relationship("Show")


class ShowCategoryIntersection(Base):
    __tablename__ = "show_category_intersection"

    show_id = Column(ForeignKey("shows.show_id"))
    category_id = Column(ForeignKey("categories.category_id"))
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    category = relationship("Category", lazy="joined")
    show = relationship("Show")
