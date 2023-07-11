# Generated by Django 4.2.3 on 2023-07-11 07:03

from django.db import migrations, models
import django_registries.registry
import tests.foos.registry


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Foo",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "foo_type",
                    django_registries.registry.ChoicesField(
                        choices=[("bar", "bar")],
                        max_length=100,
                        registry=tests.foos.registry.FooRegistry,
                    ),
                ),
            ],
        ),
    ]