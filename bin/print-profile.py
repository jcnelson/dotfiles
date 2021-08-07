#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
"""analyze_dmp.py takes the file INFILEPATH [a pstats dump file] Producing OUTFILEPATH [a human readable python profile]
Usage:   analyze_dmp.py INFILEPATH  OUTFILEPATH
Example: analyze_dmp.py stats.dmp   stats.log
"""
# --------------------------------------------------------------------------
# Copyright (c) 2019 Joe Dorocak  (joeCodeswell at gmail dot com)
# Distributed under the MIT/X11 software license, see the accompanying
# file license.txt or http://www.opensource.org/licenses/mit-license.php.
# --------------------------------------------------------------------------
# I added the above License by request here are my research links
#    https://meta.stackexchange.com/q/18883/311363
#    https://meta.stackexchange.com/q/128840/311363
#    https://codereview.stackexchange.com/q/10746

import sys, os
import cProfile, pstats, StringIO

def analyze_dmp(myinfilepath='stats.dmp', myoutfilepath='stats.log'):
    out_stream = open(myoutfilepath, 'w')
    ps = pstats.Stats(myinfilepath, stream=out_stream)
    sortby = 'cumulative'

    #ps.strip_dirs().sort_stats(sortby).print_stats(.3)  # plink around with this to get the results you need
    ps.sort_stats(sortby).print_stats(.3)  # plink around with this to get the results you need

NUM_ARGS = 2
def main():
    args = sys.argv[1:]
    if len(args) != NUM_ARGS or "-h" in args or "--help" in args:
        print __doc__
        s = raw_input('hit return to quit')
        sys.exit(2)
    analyze_dmp(myinfilepath=args[0], myoutfilepath=args[1])

if __name__ == '__main__':
    main()
