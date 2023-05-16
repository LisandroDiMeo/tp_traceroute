#!/bin/bash

IP=$1
TTL=$2
BURST=$3

sudo /home/tobi/micromamba/bin/python traceroute.py --ip "$IP" --ttl "$TTL" --burst "$BURST"