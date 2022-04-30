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

    def test_flunk_over_range_shows_is_in_category_queries(self):
        """Ensure max pagination range check works correctly."""
        with pytest.raises(NotImplementedError):
            queries.shows_in_category("Independent Movies", 0, 101)

    def test_flunk_non_existent_category(self):
        """Ensure graceful handling of shows_in_category query if category doesn't exist."""
        with pytest.raises(ValueError):
            queries.shows_in_category("Eric Cartman", 0, 20)

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

    @pytest.mark.parametrize(
        "a_date, expected_val",
        [("2021-02-14", 1), ("Dec 1 2019", 27), ("Fri, 12 Dec 201 10:55:50", 11)],
    )
    def test_shows_added_on_date(self, a_date, expected_val):
        """Ensure expected results for test_shows_added_on_date query."""
        shows = queries.shows_added_on_date(a_date)
        assert len(shows) == expected_val

    def test_high_level_stats(self):
        """Ensure high level stats function produces the expected results."""
        stats = queries.high_level_stats()
        assert stats["tv_shows"] >= 2676
        assert stats["movies"] >= 6131
        assert len(stats["movies_per_year"]) >= 74
        assert stats["categories"] >= 42
