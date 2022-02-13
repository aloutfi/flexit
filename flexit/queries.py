from flexit.config import engine
from flexit import models

from sqlalchemy.orm import Session


def shows_of_actor(actor: str) -> list[models.Show | None]:
    """Return the shows that the given actor has been in."""
    with Session(engine) as session:
        person = session.query(models.Person).filter_by(person=actor).one()
        return [
            result.show
            for result in session.query(models.ShowCastIntersection)
            .filter_by(person_id=person.person_id)
            .all()
        ]
