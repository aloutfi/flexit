import names
import pytest

from flexit import creation, dto


class TestCreation:
    def test_record_does_not_exist(self):
        """Ensure record existence detection works correctly"""
        person = dto.Person(person="Tom Cruise")
        assert not creation.record_does_not_exists(person)

    def test_create_person(self):
        """Ensure person record creation is functioning properly."""
        person = dto.Person(person=names.get_full_name())
        person_record = creation.create_person(person)
        assert person.person == person_record.person

    def test_flunk_create_category(self):
        category = dto.Category(category="TV Thrillers")
        assert creation.create_category(category) is None


class TestShowCreation:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.show = dto.Show(
            title="The Seamless Unspeakable Something",
            type="Movie",
            director=dto.Person(person="David Tipper"),
            country="United States",
            release_year=2022,
            rating="R",
            duration="140 minutes",
            description="""
                   Whomi? Time Waits while I am Daved & Confused in between a Folie a Deux. I equipt my Sponge Mallet
                   to protect me from the Wondering Clown. I fell out the doorway Tripping the Light Fantastic on
                   my way OutsideInsideOut. Things are Odd From Every Angle, treat yourself to a Spun Cookie
                   while contemplating that Everything Is Everywhere.
                    """,
            categories=[
                dto.Category(category="TV Thrillerz"),
                dto.Category(category="TV Action & Adventure"),
                dto.Category(category="Dramas"),
            ],
            actors=[
                dto.Person(person="Deija Morgan"),
                dto.Person(person="Daniel Herman"),
                dto.Person(person="Andrew Loutfi"),
            ],
        )

    def test_create_show(self):
        """Ensure Show creation works."""

        # TODO: ok... this is not end to end as the record already exists.
        #  Mocking the DB would be subject to further implementation.

        show_record = creation.create_show(self.show)
        assert "David Tipper" == show_record.director.person
