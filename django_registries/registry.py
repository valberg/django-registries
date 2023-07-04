from django.utils.module_loading import autodiscover_modules

registries_registry: list[type["Registry"]] = []


def discover_registries():
    autodiscover_modules("registry")

    for registry in registries_registry:
        registry.discover_implementations()


class Registry:
    """
    """
    
    implementations: dict[str, type["Implementation"]]
    implementations_module: str

    def __init_subclass__(cls) -> None:
        """
        """
        cls.implementations = {}
        registries_registry.append(cls)

    @classmethod
    def register(cls, implementation: type["Implementation"]):
        """
        """
        cls.implementations[implementation.slug] = implementation

    @classmethod
    def discover_implementations(cls):
        """
        """
        autodiscover_modules(cls.implementations_module)

    @classmethod
    def get_choices(cls):
        keys = sorted(cls._registry.keys())
        return list(zip(keys, keys))

    @classmethod
    def get(cls, *, slug: str) -> type["Implementation"] | None:
        return cls.implementations.get(slug)

    @classmethod
    def get_items(cls) -> list[tuple[str, type["Implementation"]]]:
        return list(cls.implementations.items())


class Implementation:
    """
    """

    slug: str
    registry: type[Registry]

    def __init_subclass__(cls) -> None:
        """
        """
        if len(cls.mro()) == 3:
            return
        cls.registry.register(cls)

