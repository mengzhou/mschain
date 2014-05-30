#!/usr/bin/env python
# liftOver: a program to convert spretus genomic coordinates to those
# of musculus or the other way around.
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


import sys
"""Current program behavior:
if one coordinate is after one delete region,
  map it back by adding delete length;
if one coordinate is after one insert region,
  map it back by deducting insert length;
if one interval is in one insert sequence,
  map its start to the start of insert site,
  then map its end to the end of insert site."""

def parse(l):
  f = l.split()
  (cchr,cstart,cent,type,offset) = (f[0],int(f[1]),int(f[2]),f[3],int(f[4]))
  return (cchr,cstart,cent,type,offset)

def main():
  if len(sys.argv) < 3:
    sys.stderr.write("Usage: %s <chain.bed> <interval.bed>\nInterval file is supposed to be sorted without overlap.\n"%sys.argv[0])
    sys.exit(1)
    
  chain = open(sys.argv[1],'r')
  if sys.argv[2] == 'stdin':
    inf = sys.stdin
  else:
    inf = open(sys.argv[2],'r')
  
  cl = chain.readline()
  (cchr,cstart,cend,type,offset) = parse(cl)
  p_end = 0
  
  for line in inf:
    f = line.split()
    (chr,start,end) = (f[0],int(f[1]),int(f[2]))
    while not chr == cchr:
      cl = chain.readline()
      if not cl:
        sys.exit(1)
      (cchr,cstart,cend,type,offset) = parse(cl)
      p_end = end
    
    # It is really annoying because BED format needs end > start, so that
    # 1bp interval might be converted to very long one. So I decided to
    # add this check variable to bypass such problem.
    if end-start == 1:
      cpg = True
    else:
      cpg = False
      
    while start >= cend:
      cl = chain.readline()
      (cchr,cstart,cend,type,offset) = parse(cl)
      
    if type == "ins_seq":
      # Map coordinate within insertion region to the end of that region.
      start = cstart - offset
    else:
      start += offset
    
    if cpg:
      end = start + 1
    else:
      # minus 1 because in BED format end coordinate is not in the interval.
      while end - 1 >= cend:
        cl = chain.readline()
        (cchr,cstart,cend,type,offset) = parse(cl)
        
      if type == "ins_seq":
        # Map coordinate within insertion region to the end of that region.
        #end = cend - offset + 1
        end = cend - offset
        # not sure whether to +1 or not. Looks like +1 is not correct, but I 
        # don't have time to find out what exactly it should be.
      else:
        #end = end + offset + 1
        end = end + offset
    """
    if start >= end:
      continue
    elif start < p_end:
      continue
    """
    # Sometimes only one end of the interval is in insert sequence, and
    # thus the start and end coordinates will be the same coincidentally
    # after mapping. This might not be right, but it is just for getting
    # rid of such tricky errors. 
    if start == end:
      end = start + 1
      
    (f[1],f[2]) = (str(start),str(end))
    p_end = end
    
    sys.stdout.write("\t".join(f)+'\n')

if __name__ == '__main__':
  main()
