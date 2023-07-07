from django.db import models

from django_registries.registry import ChoicesField
from tests.foos.registry import FooRegistry


class Foo(models.Model):
    foo_type = ChoicesField(registry=FooRegistry, max_length=100)
