#!/bin/bash

if ! command -v dasel &> /dev/null
then
    echo "dasel could not be found"
    exit
fi

VERSION=$(dasel -f pack.toml 'version')

sed -i "s/version = .*/version = \"$VERSION\"/" build.gradle

CHANGELOG=$(sed '/___/Q' CHANGELOG.md | grep -v '# ') gradle modrinth
#CHANGELOG="${CHANGELOG//'%'/'%25'}"
#CHANGELOG="${CHANGELOG//$'\n'/'%0A'}"
#CHANGELOG="${CHANGELOG//$'\r'/'%0D'}" gradle modrinth
