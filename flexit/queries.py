from datetime import datetime

from flexit.config import engine
from flexit import models, dto

from sqlalchemy.orm import Session


def shows_of_actor(actor: str) -> list[dto.Show | None]:
    """Return the shows that the given actor has been in."""
    with Session(engine) as session:
        person = session.query(models.Person).filter_by(person=actor).one()
        return [
            dto.Show.from_orm(result.show)
            for result in session.query(models.ShowCastIntersection)
            .filter_by(person=person)
            .all()
        ]


def shows_in_category(category: str) -> list[dto.Show | None]:
    """Return the shows that fall within the given category."""
    with Session(engine) as session:
        category = session.query(models.Category).filter_by(category).one()
        return [
            dto.Show.from_orm(result.show)
            for result in session.query(models.ShowCategoryIntersection)
            .filter_by(category=category)
            .all()
        ]


def person_is_director_and_actor(person: str) -> bool:
    """Return whether the person is a director and actor."""


def person_directed_and_acted_in_same_show(person: str) -> list[dto.Show | None]:
    """Return shows that the person both directed and acted in."""


def shows_added_on_date(date: datetime.date) -> list[dto.Show | None]:
    """Return shows that were added on a given date."""


def high_level_stats() -> dict:
    """Return number of tv shows, number of movies, total number of categories, shows released by year."""
