# This test ensures that the script can be parsed in bare mode. If this is the only test that fails,
# you likely didn't `@load` scripts from the base directory which your script relies on.
#
# @TEST-EXEC: zeek --bare-mode --parse-only {{ cookiecutter.project_namespace }}/{{ cookiecutter.project_slug }}
