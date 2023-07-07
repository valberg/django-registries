from tests.foos.registry import FooImplementation


class Bar(FooImplementation):
    slug = "bar"

    @classmethod
    def process_foo(cls):
        return "processed"
