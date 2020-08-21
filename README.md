Cookiecutter Zeek BinPAC Package
--------------------------------

Cookiecutter template for a Zeek package implementing a protocol analyzer written in BinPAC.

* GitHub repo: https://github.com/grigorescu/binpac_quickstart
* Free software: BSD license

Features
--------

* Script testing with ``btest``
* GitHub integration: Actions for testing and building documentation as GitHub Pages
* GitLab CI support
* Code coverage analysis

Quickstart
----------

Install the latest Cookiecutter if you haven't installed it yet (this requires
Cookiecutter 1.4.0 or higher):

    pip install -U cookiecutter

Generate a Zeek package project:

    cookiecutter https://github.com/grigorescu/binpac_quickstart.git

Answer some questions, and it will create a new directory for you, initialized as a git repo.

If you'd like free Zeek script coverage reports via [Coveralls](https://coveralls.io), login and sync your repositories.

Configuration
-------------

Some of the questions that that cookiecutter will prompt you for will likely be the same across many different packages. You can create a [cookiecutter configuration file](https://cookiecutter.readthedocs.io/en/1.7.2/advanced/user_config.html) as `~/.cookiecutterrc`, which will be read as the defaults:

``` yaml
default_context:
    github_username: "grigorescu"
    project_credits: "Vlad Grigorescu <vlad@es.net>"
    project_namespace: "ESnet"
    copyright_owner: "Energy Sciences Network"
    open_source_license: "BSD license"
```
