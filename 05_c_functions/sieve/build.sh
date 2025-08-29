#!/bin/bash -v
set -e 
cc -O3 -fPIC -shared sieve.c -o libsieve.so -lm
