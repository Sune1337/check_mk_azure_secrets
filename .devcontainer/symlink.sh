#!/bin/bash

rm -rfv $OMD_ROOT/local/lib/python3/cmk_addons/plugins/azure_secrets
ln -sv $WORKSPACE/plugins/azure_secrets $OMD_ROOT/local/lib/python3/cmk_addons/plugins/azure_secrets

rm -rfv $OMD_ROOT/local/share/check_mk/web
ln -sv $WORKSPACE/web $OMD_ROOT/local/share/check_mk/web

source /omd/sites/cmk/.profile && echo 'cmkadmin' | /omd/sites/cmk/bin/cmk-passwd -i cmkadmin
