# Built-in packages
from decimal import Decimal

# Third-party packages
from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError
from graphql_relay import to_global_id
from pytest import mark, raises, fixture

# Local packages
from api_v1.domain.starship.models import Starship
from api_v1.domain.starship.data import (
    create_starship,
    get_starship,
    update_starship,
    delete_starship,
)
from .utils import create_random_starship


@fixture
def starship_one():
    return create_random_starship()


@fixture
def starship_two():
    return create_random_starship()


@fixture
def starship_three():
    return create_random_starship()


@mark.django_db
@mark.parametrize(
    "valid_case",
    [
        ({"name": "Starship 1", "length": 12}, "Starship 1"),
        ({"name": "Starship 2", "length": 12.65}, "Starship 2"),
        ({"name": "Starship 4", "length": Decimal("12.65")}, "Starship 4"),
        ({"name": "Starship 6", "length": "12.65"}, "Starship 6"),
    ],
)
def test_create_starship_valid_cases(valid_case):
    data, expected_output = valid_case
    starship = create_starship(data)

    assert starship is not None
    assert starship.name == expected_output


@mark.django_db
@mark.parametrize(
    "invalid_case",
    [
        ({}, ValidationError),
        ({"name": None, "length": None}, ValidationError),
        ({"name": "Starship", "length": None}, ValidationError),
        ({"name": None, "length": Decimal("12.65")}, ValidationError),
        ({"name": "Starship", "length": Decimal(12.65)}, ValidationError),
    ],
)
def test_create_starship_invalid_cases(invalid_case):
    data, expected_error = invalid_case

    with raises(expected_error):
        create_starship(data)


@mark.django_db
def test_get_starship(starship_one):
    where = {"id": to_global_id(Starship.__name__, starship_one.id)}
    starship = get_starship(where)

    assert starship is not None
    assert starship.id == starship_one.id


@mark.django_db
def test_get_starship_does_not_exist():
    where = {"id": to_global_id(Starship.__name__, "0")}

    with raises(ObjectDoesNotExist):
        get_starship(where)


@mark.django_db
@mark.parametrize(
    "valid_case",
    [
        ({"name": "Starship Updated"}, [("name", "Starship Updated")]),
        ({"length": 5}, [("length", Decimal("5.00"))]),
        (
            {"name": "Starship Updated", "length": Decimal("5.00")},
            [("name", "Starship Updated"), ("length", Decimal("5.00"))],
        ),
    ],
)
def test_update_starship_valid_cases(starship_two, valid_case):
    where = {"id": to_global_id(Starship.__name__, starship_two.id)}
    data, expected_outputs = valid_case
    starship = update_starship(where, data)

    assert starship is not None

    for field, expected_output in expected_outputs:
        assert getattr(starship, field) == expected_output


@mark.django_db
@mark.parametrize(
    "invalid_case",
    [
        ({"name": None, "length": None}, ValidationError),
        ({"name": "Starship", "length": None}, ValidationError),
        ({"name": None, "length": Decimal("12.65")}, ValidationError),
        ({"name": "Starship", "length": Decimal(12.65)}, ValidationError),
    ],
)
def test_update_starship_invalid_cases(starship_three, invalid_case):
    where = {"id": to_global_id(Starship.__name__, starship_three.id)}
    data, expected_error = invalid_case

    with raises(expected_error):
        update_starship(where, data)


@mark.django_db
def test_delete_starship(starship_three):
    where = {"id": to_global_id(Starship.__name__, starship_three.id)}
    delete_starship(where)

    with raises(ObjectDoesNotExist):
        get_starship(where)


@mark.django_db
def test_delete_starship_does_not_exist():
    where = {"id": to_global_id(Starship.__name__, 0)}

    with raises(ObjectDoesNotExist):
        delete_starship(where)

