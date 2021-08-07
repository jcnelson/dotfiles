#!/bin/sh

hexdump -v -e '10/8 "%016x " 1/1 "%02x\n"'
