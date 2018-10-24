#!/bin/bash

cd $(dirname "$0")

xhost + 

docker-compose build

docker-compose run -p 4000:80 affectiva_mod_container