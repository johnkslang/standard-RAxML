#!/usr/bin/env python

#
# Changes branch-length support from [postfixed] syntax to prefixed syntax:
#
#     :branch_length[support]    ->    support:branch_length
#
# E.g., for RAxML output files for SH-like aLRT supports.
#
# Usage:
#
#     prefix_support.py example.tre
#
# Expects one argument as the name of the file to open and read.
# Writes the results to stdout, where they can be redirected.
# E.g.:
#    ./prefix_support.py example.tre > example_fixed.tre
# or
#    python prefix_support.py example.tre > example_fixed.tre
#
# Limitations
#  - the :branch_length[support] pattern must not be split across a line
#  - tree topology is not parsed and understood; any occurance of the
#    syntax :decimal-number[number] will be transformed
#
# Works with both Python 2.7 and 3.X
#

import sys
import re

if len(sys.argv) != 2:
    # to support both python 2 and python 3
    message = ["Usage:", sys.argv[0], "<file to convert>"]
    print(" ".join(message))
    sys.exit()

fileName = sys.argv[1]
input = open(sys.argv[1], "r")

# regex for the pattern to rearrange: :floating-point-number[support]
mungeRe = re.compile(r"\:[0-9]\.[0-9]*\[[0-9]*\]")

# regex for just the [support]
supportRe = re.compile(r"\[[0-9]*\]")

for line in input:

    # Break up the line into segments, one for each :branch_length[support]
    # plus one for what is before, between, and after all those.
    nonMunge = mungeRe.split(line)
    munge = mungeRe.findall(line)

    # write out each segment, transforming the :branch_length[support]
    nextMunge = 0
    for segment in nonMunge:
        sys.stdout.write(segment)
        if nextMunge < len(munge):
            mungePart = munge[nextMunge]

            # change :floating-point-number[support] -> support:floating-point-number
            nonSupport = supportRe.split(mungePart)[0]
            support = supportRe.findall(mungePart)[0]

            # print it out in the new order
            sys.stdout.write(support.strip(r'[]'))
            sys.stdout.write(nonSupport)

        nextMunge = nextMunge + 1

input.close()
