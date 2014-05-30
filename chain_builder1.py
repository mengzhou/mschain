# chain_builder1.py: a program to generate intermediate file
# for liftover purpose between musculus and spretus genomic coordinates.
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

def main():
  if len(sys.argv) < 2:
    sys.stdout.write("Usage: %s <indel.vcf>\n"%sys.argv[0])
    sys.exit(1)
    
  vcf = open(sys.argv[1],'r')
  offset = 0
  counter = 1
  rchr = ''
  
  for line in vcf:
    if line.startswith("#"):
      continue
    
    f = line.split()
    chr = "chr" + f[0]
    if not rchr == chr:
      offset = 0
      counter = 1
      rchr = chr
       
    diff = len(f[4])-len(f[3])
    offset += diff
    start = str(int(f[1])-1)
    end = str(int(start)+1)
    sys.stdout.write("\t".join((chr,start,end,">".join((f[3],f[4])),str(offset),'+'))+'\n')
    counter += 1
    
  vcf.close()

if __name__ == '__main__':
  main()
