Welcome to the django-registries documentation!
=============================================


**django-registries** is a django app that provides a framework for creating
registries of implementations for a given interface.


Let's say you have a project that needs to be able to send emails. You want to
be able to use different email backends, depending on the situation. You could
create a registry for that and register different implementations of the
``EmailBackendInterface``. Then, you could use the registry to get the
implementation you want to use.

By default `django-registries` finds registries in the ``registry`` module of
each app in `INSTALLED_APPS`. So, for example, if you have an app called ``myapp``, you could
create a ``registry.py`` file in that app and define your registry there.

.. code-block:: python

    # myapp/registry.py
    from django_registries import Interface
    from django_registries import Registry

    class EmailBackendRegistry(Registry):
        implementations_module = 'email_backend'


    class EmailBackendInterface(Interface):
        registry = EmailBackendRegistry

        def send_email(self, subject, body, from_email, to_emails):
            raise NotImplementedError()


If we then want to implement this interface, we create a module called
``email_backend.py`` in the an app, lets call it ``great_email_service``.

.. code-block:: python

    # great_email_service/email_backend.py
    from myapp.registry import EmailBackendInterface

    class GreatEmailBackend(EmailBackendInterface):
        slug = 'great_email_backend'

        def send_email(self, *, subject, body, from_email, to_emails):
            # do something great email sending here
            pass

We now have a registry with one implementation, which is neat. But we want to be able to use it in our model.
We can do that by using the ``choices_field`` method.

.. code-block:: python

    # myapp/models.py
    from django.db.models import Model

    from myapp.registry import EmailBackendRegistry


    class User(Model):
        # ...
        email_backend = EmailBackendRegistry.choices_field(max_length=100)


Now we can use the implementation seamlessly:

.. code-block:: python

    user = User.objects.get(pk=1)
    user.email_backend.send_email(
        subject="Hello",
        body="Hello world",
        from_email="user1@example.com",
        to_emails=["user2@example.com"],
    )


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
