from django.apps import AppConfig


class RegistriesAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_registries"
    verbose_name = "Django Registries"

    def ready(self) -> None:
        """ """
        from .registry import discover_registries

        discover_registries()
