#! /bin/sh
if [ "${VIRTUALENV27}" ]; then
    VIRT27=${VIRTUALENV27}
else
    VIRT27='virtualenv'
fi

${VIRT27} -p python2.7 .
./bin/pip install setuptools==33.1.1 zc.buildout==2.9.5
./bin/buildout "$@"
