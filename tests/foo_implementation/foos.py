from tests.foos.registry import FooInterface


class Bar(FooInterface):
    slug = "bar"

    def process_foo(self):
        return "processed"
