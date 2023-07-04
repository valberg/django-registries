import pytest as pytest

from tests.foo_implementation.foos import Bar
from tests.foos.models import Foo
from tests.foos.registry import FooRegistry


@pytest.mark.django_db
@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        username="test",
        password="test",
    )


def test_get_items():
    expected = [("bar", Bar)]
    assert FooRegistry.get_items() == expected


def test_get_choices():
    expected = [("bar", "bar")]
    assert FooRegistry.get_choices() == expected


def test_get():
    assert FooRegistry.get(slug="bar") == Bar


def test_choices_set_on_field():
    expected = [("bar", "bar")]
    field = Foo._meta.get_field("foo_type")
    assert field.choices == expected
