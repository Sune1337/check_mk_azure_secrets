#!/bin/bash

pushd $WORKSPACE

NAME=$(python -c 'print(eval(open("package").read())["name"])')
rm -f /omd/sites/cmk/var/check_mk/packages_local/* ||:
mkp -v package $WORKSPACE/package
cp -d /omd/sites/cmk/var/check_mk/packages_local/*.mkp $WORKSPACE/packages/

popd
