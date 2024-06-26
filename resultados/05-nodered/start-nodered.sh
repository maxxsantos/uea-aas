#!/bin/bash

# docker container rm mynodered

# docker run -it -p 1880:1880 -v node_red_data:/data --network=host --name mynodered nodered/node-red

docker-compose -p nodered up -d