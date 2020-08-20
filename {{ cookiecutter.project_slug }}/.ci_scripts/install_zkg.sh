#!/bin/bash

source $GITHUB_WORKSPACE/.ci_scripts/set_env_path.sh

pip3 install -U sphinx_rtd_theme zkg
zkg autoconfig
