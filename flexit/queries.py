import dateparser
import sqlalchemy
from sqlalchemy.orm import Session

from flexit import dto, models
from flexit.config import engine


def shows_of_actor(actor: str) -> list[dto.Show | None]:
    """Return the shows that the given actor has been in."""
    with Session(engine) as session:
        try:
            person = session.query(models.Person).filter_by(person=actor).one()
        except sqlalchemy.exc.NoResultFound:
            raise ValueError("person is not in database, and therefore not an actor.")

        return [
            dto.Show.from_orm(result.show)
            for result in session.query(models.ShowCastIntersection)
            .filter_by(person=person)
            .all()
        ]


def shows_in_category(
    category: str, start: int = 0, stop: int = 20
) -> list[dto.Show | None]:
    """Return the shows that fall within the given category."""

    if abs(start - stop) > 99:
        raise NotImplementedError("Specified range is too great.")

    with Session(engine) as session:
        try:
            category = session.query(models.Category).filter_by(category=category).one()
        except sqlalchemy.exc.NoResultFound:
            raise ValueError("The Category Doesn't exist.")
        return [
            dto.Show.from_orm(result.show)
            for result in session.query(models.ShowCategoryIntersection)
            .filter_by(category_id=category.category_id)
            .slice(start, stop)
            .all()
        ]


def person_is_director_and_actor(person: str) -> bool:
    """Return whether the person is a director and actor."""
    with Session(engine) as session:
        try:
            person = session.query(models.Person).filter_by(person=person).one()
        except sqlalchemy.exc.NoResultFound:
            raise ValueError(
                "person is not in database, and therefore not an actor or director."
            )

        is_director = session.query(models.Show).filter_by(director=person)
        is_actor = session.query(models.ShowCastIntersection).filter_by(person=person)

        # Do show table first to support short-circuiting ShowCastIntersection query
        if is_director.first() and is_actor.first():
            return True
    return False


def person_directed_and_acted_in_same_show(person: str) -> list[dto.Show | None]:
    """Return shows that the person both directed and acted in."""
    with Session(engine) as session:
        try:
            person = session.query(models.Person).filter_by(person=person).one()
        except sqlalchemy.exc.NoResultFound:
            raise ValueError(
                "person is not in database, and therefore not an actor or director."
            )

        sci = session.query(models.ShowCastIntersection).filter_by(person=person)
        return [
            dto.Show.from_orm(result.show)
            for result in sci.all()
            if result.show.director == person
        ]


def shows_added_on_date(date: str) -> list[dto.Show | None]:
    """Return shows that were added on a given date."""
    with Session(engine) as session:
        return (
            session.query(models.Show)
            .filter_by(date_added=dateparser.parse(date))
            .all()
        )


def high_level_stats() -> dict:
    """Return number of tv shows, number of movies, total number of categories, shows released by year."""
    with Session(engine) as session:
        shows = session.query(models.Show)
        tv_shows = shows.filter_by(type="TV Show")
        movies = shows.filter_by(type="Movie")
        movies_per_year = {}
        for year in sorted(
            [
                show.release_year
                for show in shows.distinct(models.Show.release_year).all()
            ]
        ):
            movies_per_year[year] = len(shows.filter_by(release_year=year).all())
        return {
            "tv_shows": len(tv_shows.all()),
            "movies": len(movies.all()),
            "categories": len(session.query(models.Category).all()),
            "movies_per_year": movies_per_year,
        }
