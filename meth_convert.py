#!/usr/bin/env python
# meth_convert.py: a program to convert methcounts new/old format.
# 
# Copyright (C) 2014 University of Southern California and
#                          Meng Zhou
# 
# Authors: Meng Zhou
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Methpipe methcounts format convertion. Since the new methcounts format
is no long BED, but this liftOver program is designed for BED, this program
is needed for fast convertion.
Usage: %prog <input_file or piped from stdin> > <output/stdout(default)>
No parameter is needed. Automatic conversion.
"""

import sys, re

def format(line):
  """Determine input format. Return True if input is not the new format.
  """
  new_pattern = "[^\s]+\t[0-9]+\t\+"
  if re.match(new_pattern, line):
    return False
  else:
    return True

def parse_new(line):
  """Break new format lines to list.
  """
  f = line.split()
  end = str(int(f[1]) + 1)
  name = f[3] + ":" + f[5]
  outline = "\t".join((f[0], f[1], end, name, f[4], f[2])) + "\n"

  return outline

def parse_old(line):
  """Break BED lines to list.
  """
  f = line.split()
  name, coverage = f[3].split(":")
  outline = "\t".join((f[0], f[1], f[5], name, f[4], coverage)) + "\n"

  return outline

def main():
  if len(sys.argv) == 1:
    inf = sys.stdin
  else:
    inf = open(sys.argv[1], 'r')

  l = inf.readline()
  isBED = format(l)
  if isBED:
    parse = parse_old
  else:
    parse = parse_new
  
  while l:
    sys.stdout.write(parse(l))
    l = inf.readline()

if __name__ == '__main__':
  main()
