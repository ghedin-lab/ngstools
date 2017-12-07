# Influenza NGS analysis

# Introduction

Congratulations you sequenced Influenza!! .. what's next.
The goal of this pipeline is to gauge the quality and coverage of your samples and to discover minor variants. There are scripts provided to show these in a visually pleasing big picture way to better understand emerging patterns in the data.   

![](https://d2mxuefqeaa7sj.cloudfront.net/s_B86D2B23CDD34FE7256B52AD38AAE99CE8F73F47041F31892C3989A95E31A700_1461707731102_Screen+Shot+2016-04-26+at+5.55.05+PM.png)

            **Figure 1.**  Coverage plots of samples


![](https://d2mxuefqeaa7sj.cloudfront.net/s_B86D2B23CDD34FE7256B52AD38AAE99CE8F73F47041F31892C3989A95E31A700_1461707894470_Screen+Shot+2016-04-26+at+5.57.23+PM.png)

            **Figure 2.**  Minor variant grid. Each row is a sample, each column is a nucleotide position. The color indicates a different nucleotide (ATCG). The smaller squares indicate a minor variant, if it has a bolded border it is a non-synonymous change. 
            
## What can this pipeline do?
- Provide coverage and quality of reads
- Generate a consensus sequence
- Discover minor variants and provide
  - a csv file containing the read coverage and base information for every nucleotide position
- Estimate a diversity index (Shannon index) based on minor variants
- ~~Put some pep in your step~~
- And more with your creativity! 


## Requirements

To undergo this Influenza pipeline you’ll need to have some software installed and ready to use:

- **For mapping**: bwa or bowtie2 
- samtools
- **python 2.7** 
  - pysam
- **R**
  - ggplot2

And you should be pretty comfortable with the terminal.



# Mapping
## Picking a reference strain

This will depend on where your samples are coming from.
A controlled experiment with infected ferrets challenged with the pandemic H1N1 strain? You’ll want to grab the A/California/7/2009 reference. 
Are they patients from a seasonal flu? You can narrow down the reference by year and location from flu databases:

  - [NCBI flu database](http://www.ncbi.nlm.nih.gov/genomes/FLU/FLU.html) 
  - [Influenza Research Database](http://www.fludb.org/brc/home.spg?decorator=influenza) 

You’ll need to grab the relevant Influenza A subtypes (H3N2, H1N1, etc.) from that seasonal year. In addition, if samples are infected with Influenza B you’ll have to be careful with choosing the correct lineage (Yamagata or Victoria). Half of the time an Influenza B strain found in a database won’t be annotated with the lineage. 

**Influenza database notes**
Select for completed Influenza genome sets when searching (each set will have 8 segments). 

When downloading the fasta, I usually just select for the coding regions. The exception for this is MP and NS segments, where I will take the first ATG to the last stop codon of the entire segments. This is because of the alternative splicing in those segments. 

You can choose the header annotations when downloading to fasta or you can modify them afterwards. For consistency across all sample types instead of the header beginning with the gene accession number, I use the abbreviated segment name:
>HA
ATGNNNNNNNN
>PB2
ATGNNNNNNNN

Also keep the original strain accession stored somewhere! 

Once you have selected the correct strain and the adjusted fasta file (one fasta file for each strain), keep it in a safe place! It’ll be used throughout the pipeline. 


## Now for real mapping

I use either [bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml) or [bwa](http://bio-bwa.sourceforge.net/)
BUT.
Depending what sequencer platform you used you may need to use different mapping software. 
For MiSeq and HiSeq reads I found either software works well in capturing reads that should be mapping to the reference strain. 
For PacBio reads I use **bwa mem**. This [blog post](http://lh3.github.io/2014/12/10/bwa-mem-for-long-error-prone-reads/) details the reasoning behind it. The default parameters should work well enough. There are alternative mapping software for long error prone reads, such as [blasr](https://github.com/PacificBiosciences/blasr). 

**Bowtie 2 parameters**
I like to use the parameters --local and if my reads are paired end, --no-mixed.

The local parameter performs a local alignment of reads rather than a global alignment. I have found that the extreme 5’ and 3’ ends of a read are often lower in quality anyway, so the local alignment will help with that. [Note: Often the ends of the reads are “soft clipped” which means it does not actually trim the reads off, but marks them and are not used in variant analysis]

The --no-mixed makes sure that both paired end reads are aligned to the reference strain otherwise both reads are thrown out. 
You can tweak and add/remove parameters depending on your specific needs. The bowtie 2 manual is very well documented. 

**Example bowtie2 Run**
You need to index the reference first

    >>>bowtie2-build h1n1ref.fa h1n1ref

Then perform mapping

    >>>bowtie2 -x h1n1ref -1 rawreads/sample402_1.fastq -2 rawreads/sample402_1.fastq -S 402.sam --no-mixed -p 15 --local --un-conc unmapped/unmapped.402.fastq

The -p specifies the number of cores used.
The —un-conc outputs the unmapped reads to a separate file. 

Then next steps converts the resulting sam file to a sorted bam file.

    >>>samtools view -bS 402.sam > 402.bam
    >>>samtools sort -T /temp/402.sorted -o 402.sorted.bam 402.bam
    >>>samtools index 402.sorted.bam
    #At this step it is safe to remove 402.sam and 402.bam

The sorted bamfile will be the basis of our downstream analysis. 

I use a python script to batch process all of my samples. 


# Variant calling

There are many ways to discover minor variants in your sample [gatk](https://www.broadinstitute.org/gatk/) , LoFreq, and many others found through a simple literature search. And you can make an educated decision on which tools you decide to use.

I wrote my own script using a python package [pysam](https://github.com/pysam-developers/pysam) which is a wrapper for samtools. 
The benefit of writing your own script helps you understand how the reads are mapped and you can make fine tune adjustments depending on the sample. This can include observing the number of forward and reverse reads, distribution of insert sizes and read quality, and tailoring the output for your graphing needs. 

The current version of my readreport.py script displays the following:

- *name* 
- *segment*
- *ntpos*
- *binocheck*  We use a [binomial test](https://en.wikipedia.org/wiki/Binomial_test) to make sure that reads that contain the minor variant do not overwhelmingly come from either orientation (forward vs reverse). 
- *major*
- *majorfreq* 
- *minor*
- *minorfreq*
- *A* These are the raw read counts for each base
- *C*
- *G*
- *T*
- *totalcount*
- *ref_nt* Indicates the reference strain nucleotide
- *reference=major* This flag helps indicate a consensus change from the reference
- *aapos*
- *majorcodon*
- *majoraa*
- *minorcodon*
- *minoraa*
- *nonsyn_syn* If the minor variant is a consensus change or not



![](https://d2mxuefqeaa7sj.cloudfront.net/s_B86D2B23CDD34FE7256B52AD38AAE99CE8F73F47041F31892C3989A95E31A700_1462203849239_Screen+Shot+2016-05-02+at+11.43.31+AM.png)

                **Figure 3.** Example output of readreport.py

The defaults for the script gives this information for each position regardless if a minor variant was found or not. The reasoning for this is that if there a complete consensus change relative to the reference strain or a change relative to the rest of the other samples, it would not be apparent if only minor variants were selected.

Of course this will take up more space so an alternative way to print out a list of variants with only variants that pass certain thresholds. 


## What qualifies as a minor variant?

This is widely debated and is the reason for so many different programs/papers/scripts attempting to find the true positive minor variant.  
I use three baseline qualifiers to filter out most minor variants:

- Quality
  - The average phred quality > 20
- Coverage
  - While low coverage may still be sufficient enough to generate a consensus sequence. We try to aim for > 200 coverage when detecting minor variants. This can change depending on the sample set and how much was sequenced. 
- Strand bias
  - In paired end sequencing there may be bias where a majority of reads with a minor variant only come from the forward strand. We use a binomial test to determine if the number of reads from both the forward and reverse reads are what we expect (assuming an equal number from both forward and reveres). 
  - This is marked under the **binocheck** label as T or F depending if it passed the test or not. 
  - Nakamura, Kensuke, et al. "Sequence-specific error profile of Illumina sequencers." *Nucleic acids research* 39.13 (2011): e90-e90.
  

Following that there are equally important factors to consider:

- Establish a minor variant threshold
  -  It is **important** that you have a control that goes along with your samples to the sequencer. This helps establish a baseline of noise for the machine. 
  - We use a default of 1% - 3% minor variant threshold depending on the control.
- How often does the minor variant occur across your samples?
  - If it occurs across all the samples it can follow that it is a real underlying minor variant in your population or on the opposite end, you have discovered a sequence specific error and should be disregarded.
- Does the minor variant exist as a consensus in other Influenza strains? Possible it could contribute to some degree of antigenicity?

Taking all of the above into consideration will help establish minor variants in your sample set.
These measures may be a bit too conservative, which is why I include the raw read counts in my output. There may be something interesting here that the automated cutoffs don’t capture. 
Which also leads to the next point of


# Graphical representation

There are two figures that I presented in the Introduction. While it may not be incredibly informative of the exact frequencies of the minor variants, it gives a general idea of how the viral diversity is present in an individual compared to the other samples. 

#  ****

