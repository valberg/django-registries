import pytest
from django.db import models

from django_registries.registry import ChoicesField
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


@pytest.mark.django_db
def test_access_implementation_via_FIELD_implementation():
    foo = Foo.objects.create(
        foo_type=Bar.slug,
    )
    assert foo.foo_type_implementation == Bar
    assert foo.foo_type_implementation.process_foo() == "processed"


def test_non_registry_raises_value_error():
    with pytest.raises(ValueError):

        class Baz(models.Model):
            foo = ChoicesField(registry="wrong", max_length=100)
