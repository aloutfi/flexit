import pytest
from flexit import queries


class TestQueries:
    @pytest.mark.parametrize("actor", ["Kevin Bacon", "Trey Parker", "Kyle MacLachlan"])
    def test_shows_of_actor(self, actor):
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
