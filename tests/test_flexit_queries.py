from datetime import datetime

import pytest
from flexit import queries


class TestQueries:
    @pytest.mark.parametrize("actor", ["Kevin Bacon", "Trey Parker", "Kyle MacLachlan"])
    def test_shows_of_actor(self, actor: str):
        """Ensure expected results for shows_of_actor query."""
        shows = queries.shows_of_actor(actor)

        match actor:
            case "Kevin Bacon":
                expected_shows = 7
            case "Trey Parker":
                expected_shows = 2
            case "Kyle MacLachlan":
                expected_shows = 4
            case _:
                expected_shows = 0
        assert len(shows) == expected_shows

    def test_person_is_director_and_actor(self, person: str):
        """Ensure expected results for person_is_director_and_actor."""

    def test_person_directed_and_acted_in_same_show(self, person: str):
        """Ensure expected results for person_directed_and_acted_in_same_show query."""

    def test_shows_added_on_date(self, date: datetime.date):
        """Ensure expected results for test_shows_added_on_date query."""
