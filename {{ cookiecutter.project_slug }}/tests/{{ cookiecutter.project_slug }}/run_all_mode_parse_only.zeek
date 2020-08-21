# This test ensures that the script works with all policy scripts loaded. If this is the only test that fails,
# you likely are conflicting with an identifier declared in stock Zeek scripts. The `@ifdef` directive might fix things.
#
# @TEST-EXEC: zeek test-all-policy --parse-only {{ cookiecutter.project_namespace }}/{{ cookiecutter.project_slug }}
