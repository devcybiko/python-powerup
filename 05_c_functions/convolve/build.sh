#!/bin/bash -v
set -e 
cc -O3 -fPIC -shared conv2d.c -o libconv2d.so -lm
