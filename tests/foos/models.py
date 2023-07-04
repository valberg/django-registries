from django.db import models

from tests.foos.registry import FooRegistry


class Foo(models.Model):
    foo_type = FooRegistry.choices_field(max_length=100)
