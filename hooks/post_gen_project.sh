#!/bin/bash

if [ -d "zeek_v{{ cookiecutter.zeek_version }}" ]
then
   SOURCE="zeek_v{{ cookiecutter.zeek_version }}"
else
   VERSION=$(zeek-config --version || echo "4.0")
   VERSION=$(echo "$VERSION" | cut -f -2 -d.)
   SOURCE="zeek_v$VERSION"
fi

cp -Rv "$SOURCE"/* .
rm -Rf zeek_v*

git init
git add .
git commit -m "Initial commit [cookiecutter-zeekpackage]"

