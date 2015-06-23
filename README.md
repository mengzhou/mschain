mschain
=======

Scripts for making chain file for mm10 - ms10 liftover based on VCF indel
information.

Usage
=====

* Step 0
  Firstly make sure the input VCF is in correct format. See 
  [VCF format specification](http://vcftools.sourceforge.net/specs.html) for 
  more information.
* Step 0.5
  It is worth noting that this program requires proper preprocessing for VCF 
  file. The ALT field of VCF must be only one allele without multiple ones
  separating by comma. This requires manually selection by referring to the
  last SAMPLE field of VCF and decide which allele is required. The script 
  `vcfutils.pl` in [`bcftools`](https://github.com/samtools/bcftools) has such
  funtionality. Run the following command to select one sample from a VCF file:

    > ./vcfutils.pl subsam <in.vcf> SAMPLE_NAME > out.vcf

* Step 1
  Run chain_builder1.py. Assume the input VCF file is ms_indel.vcf:

    > python chain_builder1.py ms_indel.vcf

  The program will generate a intermedia file to stdout, you can pipe it to 
  `chain_builder2.py` or keep it for debugging purposes.

* Step 2
  Run chain_builder2.py. By default it tries to read from stdin, so using pipe
  in Step 1 is recommended.

    > python chain_builder1.py ms_indel.vcf | python chain_builder2.py > ms_chain.bed

  This will generates the chain file to be used for lift over.

* Step 3
  The script liftOver.py will do the lift over for ms coordinates.

    > python liftOver.py ms_chain.bed SPRETUS_BED_TO_BE_CONVERTED

Notes
=====

The scripts are poorly commented and the output is hardly human-readable. But
they work. There are some other tricky situations that are not yet solved and
marked in liftOver.py, but I think they are not important so maybe no further
fix.

More notes
==========
The chain file is directional. i.e. for the steps above you will only get a
ms_chain.bed that can be used only for converting ms coordinates to mm. To make
a chain for mm to ms, just need to swap the REF and ALT column in input VCF for
Step 0.5.
