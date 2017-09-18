#! /bin/sh
#
# release.sh
# Copyright (C) 2015 FBruynbroeck <francois.bruynbroeck@hotmail.com>
#
# Distributed under terms of the LICENCE.txt license.
#


remove_hooks ${1:-.};
fullrelease;
reload_hooks ${1:-.};
for buildout in $BUILDOUT
do
    echo "Changelog for $buildout";
    BUILDOUT=$buildout changelogrelease;
done
