from datetime import datetime
import random
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
        assert len(shows) <= expected_shows

    def test_actor_dne(self):
        """Ensure non-existant actors are caught prior to execution."""
        with pytest.raises(ValueError):
            queries.shows_of_actor("Notan Actor")

    @pytest.mark.parametrize(
        "category, start, stop",
        [
            ("Independent Movies", random.randint(0, 10), random.randint(20, 40)),
            ("TV Comedies", 0, 99),
            ("Dramas", 1, 6),
        ],
    )
    def test_show_is_in_category(self, category: str, start: int, stop: int):
        """Ensure expected results for test_show_is_in_category query"""
        shows = queries.shows_in_category(category, start, stop)
        assert len(shows) == abs(start - stop)

    def test_flunk_unhandled_test_show_is_in_category_queries(self):
        with pytest.raises(NotImplementedError):
            queries.shows_in_category("Eric Cartman", 0, 101)

    @pytest.mark.parametrize(
        "person, is_actor_and_director",
        [("Clint Eastwood", True), ("The Notorious B.I.G.", False)],
    )
    def test_person_is_director_and_actor(
        self, person: str, is_actor_and_director: bool
    ):
        """Ensure expected results for person_is_director_and_actor query."""
        assert queries.person_is_director_and_actor(person) == is_actor_and_director

    def test_person_directed_and_acted_in_same_show(self):
        """Ensure expected results for person_directed_and_acted_in_same_show query."""
        person = "Clint Eastwood"
        shows = queries.person_directed_and_acted_in_same_show(person)
        assert all(show.director.person == person for show in shows)

    def test_shows_added_on_date(self, date: datetime.date):
        """Ensure expected results for test_shows_added_on_date query."""
