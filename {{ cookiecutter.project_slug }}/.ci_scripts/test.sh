#!/bin/bash

set -e

function debug_and_die {
    OUTPUT_PATH=$HOME/.zkg/testing/{{ cookiecutter.project_slug }}/clones/{{ cookiecutter.project_slug }}
    if [ -s $OUTPUT_PATH/zkg.test_command.stdout ]; then
	echo "zkg test command stdout"
	echo "-----------------------"
	cat $OUTPUT_PATH/zkg.test_command.stdout
    fi

    if [ -s $OUTPUT_PATH/zkg.test_command.stderr ]; then
	echo "zkg test command stderr"
	echo "-----------------------"
	cat $OUTPUT_PATH/zkg.test_command.stderr
    fi

    if [ -s $HOME/.zkg/logs/{{ cookiecutter.project_slug }}-build.log ]; then
	echo "zkg build command output"
	echo "-----------------------"
	cat $HOME/.zkg/logs/{{ cookiecutter.project_slug }}-build.log
    fi

    exit 1
}

source $GITHUB_WORKSPACE/.ci_scripts/set_env_path.sh

echo "Running zkg test..."
zkg test "$PWD" || debug_and_die
echo "Tests succeeded. Running zkg install..."
zkg install --force --skiptests "$PWD" || debug_and_die
echo "Install succeeded."
`
