#! /bin/sh
#
# release.sh
# Copyright (C) 2015 FBruynbroeck <francois.bruynbroeck@hotmail.com>
#
# Distributed under terms of the LICENCE.txt license.
#


remove_hooks $1;
fullrelease $1;
reload_hooks $1;
changelogrelease;
