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
            .filter_by(person_id=person.person_id)
            .all()
        ]
