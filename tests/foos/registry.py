from django_registries.registry import Interface
from django_registries.registry import Registry


class FooRegistry(Registry["FooInterface"]):
    implementations_module = "foos"


class FooInterface(Interface):
    slug = "foo"
    registry = FooRegistry

    def process_foo(self):
        raise NotImplementedError()
