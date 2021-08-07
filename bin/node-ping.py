#!/usr/bin/env python2

import blockstack.lib.client as client
import sys
print client.getinfo(hostport=sys.argv[1])
