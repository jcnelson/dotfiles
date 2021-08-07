#!/bin/sh

if [ -z "$1" ]; then 
   echo "Usage: $0 enable/disable"
   exit 1
fi

ID="$(xinput list | grep -i wacom | egrep -o id=[0-9]+ | sed -r 's/id=//g')"
if [ -z "$ID" ]; then 
   echo "No touchscreen found"
   exit 1
fi

if [ "$1" = "enable" ]; then 
    xinput enable "$ID"
else
    xinput disable "$ID"
fi

exit 0
