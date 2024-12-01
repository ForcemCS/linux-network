#!/usr/bin/bash

# INCLUDE ALL COMMANDS NEEDED TO PERFORM THE LAB
# This file will get called from capture_submission.sh

sw   ip link add name mybridge type bridge
sw   ip link set mybridge up
sw   ip link set eth1 master mybridge
sw   ip link set eth2 master mybridge
sw   ip link set eth3 master mybridge
sw   ip link set eth4 master mybridge
