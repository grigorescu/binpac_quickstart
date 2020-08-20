{% set is_open_source = cookiecutter.open_source_license != 'Not open source' -%}

Zeek Package for {{ cookiecutter.project_name }}
================================================

.. image:: https://travis-ci.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}.svg?branch=master
   :target: https://travis-ci.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}
   :alt: Build Status

.. image:: https://coveralls.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}/badge.svg?branch=master
   :target: https://coveralls.io/repos/github/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}?branch=master
   :alt: Coverage Status

{% if is_open_source %}
.. image:: https://img.shields.io/github/license/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }})
   :target: :doc:`LICENSE <./LICENSE>`
   :alt: {{ cookiecutter.open_source_license }}
{% endif %}

![GitHub](

{{ cookiecutter.project_short_description }}

Getting Started
---------------

These instructions will get you a copy of the package up and running on your Zeek cluster. See development for notes on how to install the package in order to hack on or contribute to it.

Prerequisites
-------------

This is a package designed to run with the [Zeek Network Security Monitor](https://zeek.org). First, [get Zeek](https://zeek.org/get-zeek/). We strive to support both the current feature and LTS releases.

The recommended installation method is via the [Zeek package manager, zkg](https://docs.zeek.org/projects/package-manager/en/stable/). On any recent system, run `pip install zkg`. After installation, run `zkg autoconfig`. For more information, see the [zkg documentation](https://docs.zeek.org/projects/package-manager/en/stable/quickstart.html).

Installing
----------

To install the package, run:

```
zkg install https://github.com/{{ cookiecutter.github_username }}/{{ cookiecutter.project_slug }}
```

If this is being installed on a cluster, install the package on the manager, then deploy it via: 

```
zeekctl deploy
```

Running the tests
-----------------

`zkg` will run the test suite before installing. To manually run the tests, go into the `tests` directory, and run `make`.

Contributing
------------

Please read [CONTRIBUTING.md](./docs/CONTRIBUTING.md) for details on how to contribute.

Versioning
----------

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](../../tags). 

Credits
-------

{% for credit in cookiecutter.project_credits.split(', ') %}
* {{ credit }}
{% endfor %}

See also the list of [contributors](contributors) who participated in this project.

License
-------

{% if is_open_source %}This project is licensed under the {{ cookiecutter.open_source_license }}.{% endif %} See the [LICENSE](LICENSE) file for details.

Acknowledgments
---------------

* ESnet team for Zeek Package Cookie Cutter
