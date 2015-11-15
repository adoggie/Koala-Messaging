#!/bin/bash
dest=$1
if [ ! -d $1 ];then
	mkdir -p ${dest}
fi

if [ $# -lt 1 ];then
	echo 'error: parameter insufficient, please specify output dir'
	exit 1
fi

cp -rfv appbase/* ${dest}
