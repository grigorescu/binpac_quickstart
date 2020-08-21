# This test ensures that the script loads in bare mode. If this is the only test that fails,
# you have a runtime error.
#
# @TEST-EXEC: zeek --bare-mode {{ cookiecutter.project_namespace }}/{{ cookiecutter.project_slug }}
