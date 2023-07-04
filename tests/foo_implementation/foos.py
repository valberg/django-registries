from tests.foos.registry import FooImplementation


class Bar(FooImplementation):

    slug = "bar"

    def process_foo(self):
        return "processed"
