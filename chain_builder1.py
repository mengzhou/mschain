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