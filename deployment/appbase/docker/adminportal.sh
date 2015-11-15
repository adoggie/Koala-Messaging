#!/bin/bash
pwd=$(cd `dirname $0`;pwd)
$pwd/docker_run.sh adminportal -p 16006:3000 

