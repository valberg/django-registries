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
    def choices_field(cls, **kwargs):
        class ChoicesField(models.CharField):
            def contribute_to_class(self, model_cls, name, **kwargs):
                cls.choices_fields.append((name, model_cls))
                super().contribute_to_class(model_cls, name, **kwargs)

        return ChoicesField(**kwargs)


"""
Integration = self.get_model("Integration")
Integration._meta.get_field(
    "slug",
).choices = IntegrationRegistry.get_choices()
"""


class Implementation:
    """ """

    slug: str
    registry: type[Registry]

    def __init_subclass__(cls) -> None:
        """ """
        if len(cls.mro()) == 3:
            return
        cls.registry.register(cls)
