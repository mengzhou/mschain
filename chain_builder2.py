import sys
CORRECT = 0

def parse(line):
  global CORRECT
  f = line.split()
  chr = f[0]
  start = int(f[1])
  offset = int(f[4]) + CORRECT
  name = f[3]
  return (chr,start,offset,name)

def main():
  global CORRECT
  if len(sys.argv) < 2:
    chain = sys.stdin
  else:
    chain = open(sys.argv[1],'r')
    
  l = chain.readline()
  (p_chr,p_start,p_offset,name) = parse(l)
  sys.stdout.write("\t".join((p_chr,"0",str(p_start+1),"X","0",'+'))+'\n')
  
  while l:
    l = chain.readline()
    if l == '':
      sys.stdout.write("\t".join((chr,str(p_start+1),"999999999","X",str(-1*p_offset),"+"))+"\n")
      break
    
    (chr,start,offset,name) = parse(l)
    if not chr == p_chr:
      sys.stdout.write("\t".join((p_chr,str(p_start+1),"999999999","X",str(-1*p_offset),"+"))+"\n")
      (p_chr,p_start,p_offset,name) = parse(l)
      CORRECT = 0
      sys.stdout.write("\t".join((p_chr,"0",str(p_start+1),"X","0",'+'))+'\n')
      continue
    
    # all offset values are negative!
    if p_offset > offset:
      # deletion. Shift coordinates rightwards.
      start = start+p_offset
      
      # This case is really tricky... Some indel is made in sequence that has been
      # deleted in the reference.
      if start <= p_start:
        CORRECT -= start - p_start
        p_offset += CORRECT
        offset += CORRECT
        start = p_start + 1
      
      sys.stdout.write("\t".join((chr,str(p_start+1),str(start+1),name,str(-1*p_offset),'+',str(CORRECT)))+'\n')
      p_chr = chr
      p_start = start
      p_offset = offset
    elif p_offset < offset:
      # insertion. Mark insertion sequence to void, and shift other parts rightwards.
      start = start+p_offset
      if start <= p_start:
        CORRECT += start - p_start - 1
        p_offset += CORRECT
        offset += CORRECT
        start = p_start + 1
      #sys.stdout.write("\t".join((chr,str(p_start+1),str(p_start+(offset-p_offset+1)),name,'-1','+'))+'\n')
      sys.stdout.write("\t".join((chr,str(p_start+1),str(start+1),name,str(-1*p_offset),'+',str(CORRECT)))+'\n')
      #sys.stdout.write("\t".join((chr,str(p_start+(offset-p_offset+1)),str(start+1),name,str(-1*p_offset),'+'))+'\n')
      sys.stdout.write("\t".join((chr,str(start+1),str(start+1+offset-p_offset),"ins_seq",str(p_offset),'+',str(CORRECT)))+'\n')
      p_chr = chr
      p_start = start+offset-p_offset
      p_offset = offset
    
  chain.close()
    

if __name__ == '__main__':
  main()