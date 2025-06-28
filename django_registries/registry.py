from __future__ import annotations

from typing import Any
from typing import Generic
from typing import TypeVar

from django.db import models
from django.db.models.base import Model
from django.utils.module_loading import autodiscover_modules

Intf = TypeVar("Intf", bound="Interface")

registries_registry: list[type[Registry[Any]]] = []


def discover_registries() -> None:
    autodiscover_modules("registry")

    for registry in registries_registry:
        registry.discover_implementations()


class ImplementationNotFound(KeyError):
    pass


class Registry(Generic[Intf]):

    implementations: dict[str, type[Intf]]
    implementations_module: str

    choices_fields: list[tuple[str, type[models.Model]]]

    def __init_subclass__(cls) -> None:
        """ """
        cls.implementations = {}
        cls.choices_fields = []
        registries_registry.append(cls)

    @classmethod
    def register(cls, implementation: type[Intf]) -> None:
        """ """
        cls.implementations[implementation.slug] = implementation

    @classmethod
    def discover_implementations(cls) -> None:
        """ """
        autodiscover_modules(cls.implementations_module)

    @classmethod
    def get_choices(cls) -> list[tuple[str, str]]:
        keys = sorted(cls.implementations.keys())
        return list(zip(keys, keys))

    @classmethod
    def get(cls, *, slug: str) -> Intf:
        if slug not in cls.implementations:
            raise ImplementationNotFound(f"No implementation exists for slug '{slug}'")
        return cls.implementations[slug]()

    @classmethod
    def get_items(cls) -> list[tuple[str, type[Intf]]]:
        return list(cls.implementations.items())

    @classmethod
    def choices_field(cls, *args: Any, **kwargs: Any) -> ChoicesField:
        return ChoicesField(*args, registry=cls, **kwargs)


class ChoicesField(models.CharField):
    registry: type[Registry[Any]]

    def __init__(
        self,
        *args: Any,
        registry: type[Registry[Any]],
        **kwargs: Any,
    ) -> None:
        if not isinstance(registry, type) or not issubclass(registry, Registry):
            raise ValueError(
                "ChoicesField keyword argument 'registry' requires a class "
                "which subclasses Registry.",
            )

        self.registry = registry
        kwargs["choices"] = registry.get_choices
        super().__init__(*args, **kwargs)

    def deconstruct(self) -> Any:
        name, path, args, kwargs = super().deconstruct()
        kwargs["registry"] = self.registry
        return name, path, args, kwargs

    @property
    def non_db_attrs(self) -> tuple[str, ...]:
        return super().non_db_attrs + ("registry",)

    @non_db_attrs.setter
    def non_db_attrs(self, value: tuple[str, ...]) -> None:
        self.non_db_attrs = value

    def contribute_to_class(
        self,
        model_cls: type[Model],
        name: str,
        **kwargs: Any,
    ) -> None:
        self.registry.choices_fields.append((name, model_cls))

        def getter(_self: type) -> type[Interface]:
            value = getattr(_self, name)
            return self.registry.get(slug=value)

        setattr(model_cls, f"{name}_implementation", property(getter))

        super().contribute_to_class(model_cls, name, **kwargs)


class Interface:
    """ """

    slug: str
    registry: type[Registry[Any]]

    def __init_subclass__(cls) -> None:
        """ """
        if len(cls.mro()) == 3:
            return
        cls.registry.register(cls)
