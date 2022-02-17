from sqlalchemy.orm import Session
from flexit.config import engine
from flexit import models, dto


def _get_record_if_exists(
    dto_record: dto.Person | dto.Category | dto.Show,
) -> models.Base | None:
    """Return the record if it exists."""
    match dto_record:
        case dto.Person():
            model = models.Person
            field = models.Person.person
            value = dto_record.person
        case dto.Category():
            model = models.Category
            field = models.Category.category
            value = dto_record.category
        case dto.Show():
            model = models.Show
            field = models.Show.title
            value = dto_record.title
        case _:
            raise ValueError("Unhandled dto type was passed in.")

    with Session(engine) as session:
        return session.query(model).filter(field == value).one_or_none()


def record_does_not_exists(dto_record: dto.Person | dto.Category | dto.Show) -> bool:
    """Search to see if a record exists based on pre-defined values."""
    return _get_record_if_exists(dto_record) is None


def _create_person(person: dto.Person, session) -> models.Person | None:
    """Create a person record."""
    person_record = models.Person(**dict(person))
    session.add(person_record)
    session.commit()
    return person_record


def create_person(person: dto.Person) -> dto.Person | None:
    """Check if the person exists. Create a new person record if not."""
    with Session(engine) as session:
        if record_does_not_exists(person):
            return dto.Person.from_orm(_create_person(person, session))


def create_category(category: dto.Category) -> dto.Category | None:
    """Check if the category exists. Create new category if not."""
    with Session(engine) as session:
        if record_does_not_exists(category):
            return dto.Category.from_orm(_create_category(category, session))


def _create_category(category: dto.Category, session) -> models.Category | None:
    """Create a record for a new category"""
    category_record = models.Category(**dict(category))
    session.add(category_record)
    session.commit()
    return category_record


def _create_show(show: dto.Show, session) -> models.Show | None:
    """Create a record for a new show."""
    show_record = models.Show(**show.dict(exclude={"categories", "actors", "director"}))
    if show.director:
        show_record.director = _get_record_if_exists(show.director) or _create_person(
            show.director, session
        )
    session.add(show_record)
    session.commit()
    return show_record


def _create_show_category_intersection(
    show_record: models.Show, category_record: models.Category, session
):
    """Create record to associate a category with a show."""
    session.add(
        models.ShowCategoryIntersection(show=show_record, category=category_record)
    )
    session.commit()


def _create_show_cast_intersection(
    show_record: models.Show, actor_record: models.Person, session
):
    """Create record to associate a person (actor) with a show."""
    session.add(models.ShowCastIntersection(show=show_record, person=actor_record))
    session.commit()


def create_show(show: dto.Show) -> dto.Show:
    """Check if the show exists. Create new show if not."""
    with Session(engine) as session:
        show_record = _get_record_if_exists(show)
        if not show_record:
            show_record = _create_show(show, session)

            # Associate categories
            for category in show.categories:
                _create_show_category_intersection(
                    show_record,
                    _get_record_if_exists(category)
                    or _create_category(category, session),
                    session,
                )

            # Associate actors
            for actor in show.actors:
                _create_show_cast_intersection(
                    show_record,
                    _get_record_if_exists(actor) or _create_person(actor, session),
                    session,
                )

        return dto.Show.from_orm(show_record)
