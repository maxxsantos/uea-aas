#!/bin/bash

docker-compose -p mqtt5 down -v

docker-compose -p mqtt5 up -d