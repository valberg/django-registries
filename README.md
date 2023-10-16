# Django Registries

[![Tests](https://github.com/valberg/django-registries/actions/workflows/test.yml/badge.svg)](https://github.com/valberg/django-registries/actions/workflows/test.yml)
[![Documentation](https://readthedocs.org/projects/django-registries/badge/?version=latest)](https://django-registries.readthedocs.io/en/latest/?badge=latest)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/valberg/django-registries/main.svg)](https://results.pre-commit.ci/latest/github/valberg/django-registries/main)
[![PyPI - Version](https://img.shields.io/pypi/v/django-registries.svg)](https://pypi.org/project/django-registries)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-registries.svg)](https://pypi.org/project/django-registries)

-----

**django-registries** is a structured way to create registries of implementations.

Let’s say you have a project that needs to be able to send emails. You want to be able to use different email
backends, depending on the situation. You could create a registry for that and register different implementations
of the EmailBackendInterface. Then, you could use the registry to get the implementation you want to use.

**Table of Contents**

- [Installation](#installation)
- [Development](#development)
- [Documentation](#documentation)
- [License](#license)

## Installation

```console
pip install django-registries
```

## Development

```console
git clone
cd django-registries
pip install hatch
hatch run tests:cov
hatch run tests:typecheck
```

## Documentation

[https://django-registries.readthedocs.io/en/latest/](https://django-registries.readthedocs.io/en/latest/)

## License

`django-registries` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
