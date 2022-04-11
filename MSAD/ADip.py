#!/bin/env python -tt
####################################################################
#
# This script was created to pull out a single random IP address
# from the ADenv file containing the variable ip, in the following
# format:
# 
#      ip = "127.0.0.1,127.1.0.1,127.1.1.1"
#
# Created by: J.Lickey
# 20220303 
#
####################################################################
import ADenv
import random

ip_lst = []

for ips in ADenv.ip.split(','):
    ip_lst.append(ips)

ip = random.choice(ip_lst)
