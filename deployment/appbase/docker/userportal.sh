#!/bin/bash
pwd=$(cd `dirname $0`;pwd)
$pwd/docker_run.sh userportal -p 16005:8888 
