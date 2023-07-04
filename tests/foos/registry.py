

from django_registries.registry import Implementation, Registry


class FooRegistry(Registry):
    implementations_module = "foos"


class FooImplementation(Implementation):
    slug = "foo" 
    registry = FooRegistry

    def process_foo(self):
        raise NotImplementedError()
