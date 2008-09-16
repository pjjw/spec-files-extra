#!/bin/sh
# Idea from pkgsrc GD 20080916

if ! [ -d ${HOME}/.blender ]; then
	echo Softlinking ${HOME}/.blender to point to global /usr/share/blender settings.
	ln -s /usr/share/blender ${HOME}/.blender
fi

exec /usr/bin/blender.exe "$@"
