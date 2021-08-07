#!/bin/bash

message="$1"

if [ -z "$message" ]; then
   echo >&2 "Usage: $0 MESSAGE"
   exit 1
fi

if ! [ -f "$message" ]; then
   echo >&2 "No such file or directory: $message"
   exit 1
fi

set -ueo pipefail

gpg2 --clearsign -a -u "jude@blockstack.com" -o - "$message" > /tmp/stacks-signed-message.txt
gpg2 --verify /tmp/stacks-signed-message.txt >/dev/null 2>&1 || ( echo >&2 "GPG verify failed"; exit 1 )
cat /tmp/stacks-signed-message.txt
