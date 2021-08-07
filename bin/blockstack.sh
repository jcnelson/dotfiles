#!/bin/sh

PORTNUM=3000
PORTAL_URL="http://localhost:$PORTNUM"

# logging...
echo "request: $@" >> /tmp/blockstack.log

# expect blockstack:AUTHENTICATION_TOKEN
if [ -z "$1" ]; then 
   exit 1
fi

AUTH_TOKEN="$(echo "$1" | sed -r 's/blockstack://g')"
exec chromium-browser "$PORTAL_URL/auth?authRequest=$AUTH_TOKEN"
