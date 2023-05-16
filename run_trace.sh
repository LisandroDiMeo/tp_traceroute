#!/bin/bash

IP=$1
TTL=$2
BURST=$3

sudo python3 traceroute.py --ip "$IP" --ttl "$TTL" --burst "$BURST"