import pytest as pytest
from tests.foo_implementation.foos import Bar

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
