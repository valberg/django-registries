from django.apps import apps
from django.db import models
from django.utils.module_loading import autodiscover_modules

registries_registry: list[type["Registry"]] = []


def discover_registries():
    autodiscover_modules("registry")

    for registry in registries_registry:
        registry.discover_implementations()


def update_choices_fields():
    for registry in registries_registry:
        for field_name, model_class in registry.choices_fields:
            ModelClass = apps.get_model(
                model_class._meta.app_label,
                model_class._meta.model_name,
            )
            field = ModelClass._meta.get_field(field_name)
            field.choices = registry.get_choices()


class Registry:
    """ """

    implementations: dict[str, type["Implementation"]]
    implementations_module: str

    choices_fields: list[tuple[str, type[models.Model]]]

    def __init_subclass__(cls) -> None:
        """ """
        cls.implementations = {}
        cls.choices_fields = []
        registries_registry.append(cls)

    @classmethod
    def register(cls, implementation: type["Implementation"]):
        """ """
        cls.implementations[implementation.slug] = implementation

    @classmethod
    def discover_implementations(cls):
        """ """
        autodiscover_modules(cls.implementations_module)

    @classmethod
    def get_choices(cls):
        keys = sorted(cls.implementations.keys())
        return list(zip(keys, keys))

    @classmethod
    def get(cls, *, slug: str) -> type["Implementation"] | None:
        return cls.implementations.get(slug)

    @classmethod
    def get_items(cls) -> list[tuple[str, type["Implementation"]]]:
        return list(cls.implementations.items())

    @classmethod
    def choices_field(cls, *args, **kwargs):
        return ChoicesField(*args, registry=cls, **kwargs)


class ChoicesField(models.CharField):
    registry: type[Registry]

    def __init__(self, *args, registry: type[Registry], **kwargs) -> None:
        if not isinstance(registry, type) or not issubclass(registry, Registry):
            raise ValueError(
                "ChoicesField keyword argument 'registry' requires a class "
                "which subclasses Registry.",
            )

        self.registry = registry
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs["registry"] = self.registry
        return name, path, args, kwargs

    @property
    def non_db_attrs(self):
        return super().non_db_attrs + ("registry",)

    def contribute_to_class(self, model_cls, name, **kwargs) -> None:
        self.registry.choices_fields.append((name, model_cls))

        @property
        def getter(_self):
            value = getattr(_self, name)
            return self.registry.get(slug=value)

        setattr(model_cls, f"{name}_implementation", getter)

        super().contribute_to_class(model_cls, name, **kwargs)


class Implementation:
    """ """

    slug: str
    registry: type[Registry]

    def __init_subclass__(cls) -> None:
        """ """
        if len(cls.mro()) == 3:
            return
        cls.registry.register(cls)
