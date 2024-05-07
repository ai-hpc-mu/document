Biomedical Application 
=========================

The following is note taking for applications for Bioinformatics.

BLAST
------
BLAST (basic local alignment search tool)[3] is an algorithm and program for comparing primary biological sequence information, such as the amino-acid sequences of proteins or the nucleotides of DNA and/or RNA sequences.

`BLAST  <https://en.wikipedia.org/wiki/BLAST_(biotechnology)>`_

Allocate resource for testing
----------------------------------
To test an example on a compute node

.. code-block:: console

   $ salloc -t 1:0:0 -c 32 --mem=64GB 
   $ ssh <allocated node>


Making example file
--------------------

.. code-block:: console

   $ printf ">NR_024570.1 Escherichia coli strain U 5/41 16S ribosomal RNA, partial sequence
   AGTTTGATCATGGCTCAGATTGAACGCTGGCGGCAGGCCTAACACATGCAAGTCGAACGGTAACAGGAAGCAGCTTGCTGCTTTGCTGACGAGTGGCGGACGGGTGAGTAATGTCTGGGAAACTGCCTGATGGAGGGGGATAACTACTGGAAACGGTAGCTAATACCGCATAACGTCGCAAGCACAAAGAGGGGGACCTTAGGGCCTCTTGCCATCGGATGTGCCCAGATGGGATTAGCTAGTAGGTGGGGTAACGGCTCACCTAGGCGACGATCCCTAGCTGGTCTGAGAGGATGA
   >NR_169460.1 Pseudomonas aylmerensis strain S1E40 16S ribosomal RNA, partial sequence
   CTCAGATTGAACGCTGGCGGCAGGCCTAACACATGCAAGTCGAGCGGTAGAGAGAAGCTTGCTTCTCTTGAGAGCGGCGGACGGGTGAGTAATGCCTAGGAATCTGCCTGGTAGTGGGGGATAACGTTCGGAAACGGACGCTAATACCGCATACGTCCTACGGGAGAAAGCAGGGGACCTTCGGGCCTTGCGCTATCAGATGAGCCTAGGTCGGATTAGCTAGTTGGTGGGGTAATGGCTCACCAAGGCGACGATCCGTAACTGGTCTGAGAGGATGATCAGTCACACTGGAACTGA
   " > refs.fa



   $ printf ">Q1
   AGTTTGATCATGGCTCAGATTGAACGCTGGCGGCAGGCCTAACACATGCAAGTCGAACGGTAACAGGAAGCAGCTTGCGGGGGTGCTGACGAGTGGCGGACGGGTGAGTAATGTCTGGGAAACTGCCTGATGGAGGGGGATAACTACTGGAAACGGTAGCTAATACCGCATAACGTCGCAAGCACAAAGAGGGGGACCTTAGGGCCTCTTGCCCCCCCATGTGCCCAGATGGGATTAGCTAGTAGGTGGGGTAACGGCTCACCTAGGCGACGATCCCTAGCTGGTCTGAGAGGATGA
   >Q2
   CTCAGATTGAACGCTGGCGGCAGGCCTAACACATGCAAGTCGAGCGGTAGAGAGAAGCTTGCTTCTCTTGAGAGCGGCGGACCCCCGAGTAATGCCTAGGAATCTGCCTGGTAGTGGGGGATAACGTTCGGAAACGGACGCTAATACCGCATACGTCCTACGGGAGAAAGCAGGGGACCTTCGGGCCTTGCGCTATCAGATGAGGGGGGGTCGGATTAGCTAGTTGGTGGGGTAATGGCTCACCAAGGCGACGATCCGTAACTGGTCTGAGAGGATGATCAGTCACACTGGAACTGA
   >Q3_exact
   AGTTTGATCATGGCTCAGATTGAACGCTGGCGGCAGGCCTAACACATGCAAGTCGAACGGTAACAGGAAGCAGCTTGCTGCTTTGCTGACGAGTGGCGGACGGGTGAGTAATGTCTGGGAAACTGCCTGATGGAGGGGGATAACTACTGGAAACGGTAGCTAATACCGCATAACGTCGCAAGCACAAAGAGGGGGACCTTAGGGCCTCTTGCCATCGGATGTGCCCAGATGGGATTAGCTAGTAGGTGGGGTAACGGCTCACCTAGGCGACGATCCCTAGCTGGTCTGAGAGGATGA
   >Q4_exact
   CTCAGATTGAACGCTGGCGGCAGGCCTAACACATGCAAGTCGAGCGGTAGAGAGAAGCTTGCTTCTCTTGAGAGCGGCGGACGGGTGAGTAATGCCTAGGAATCTGCCTGGTAGTGGGGGATAACGTTCGGAAACGGACGCTAATACCGCATACGTCCTACGGGAGAAAGCAGGGGACCTTCGGGCCTTGCGCTATCAGATGAGCCTAGGTCGGATTAGCTAGTTGGTGGGGTAATGGCTCACCAAGGCGACGATCCGTAACTGGTCTGAGAGGATGATCAGTCACACTGGAACTGA
   " > queries.fa

Blasting
--------------------

To run blast tools in singularity container with specific command blastn

.. code-block:: console

   $ singularity exec /app/blast.2.11.sif blastn -query queries.fa -subject refs.fa -outfmt "6 qseqid qlen sseqid slen length pident evalue bitscore" -max_hsps 1 -max_target_seqs 1 | sort -nrk 8 > blast-results.tmp 

Typically we want things in table form, here's one way to run it for that and sort by bitscore: Adding a header


.. code-block:: console
  
   $ cat <(printf "qseqid\tqlen\tsseqid\tslen\tlength\tpident\tevalue\tbitscore\n") blast-results.tmp > blast-results.tsv 


   $ rm blast-results.tmp 
   $ column -ts $'\t' blast-results.tsv 

Reproducting research results with Python and Conda Package management
======================================================================
In many cases, researcher need system adminstrators to install new library for their project. This is somehow taking longer time then we expected. So one solution in sharing system cluster, we are learing how to use 'module' system environment or singularity container. They are general usage. For Python eco-system, conda package management and conflict library resolver save us a lot when it comes to customization library for us.

We use newly release(two years)  and request from user for PSSMPRO.

How to
------
Setup Conda (once time setup)


.. code-block:: console

   $ module load anaconda3

   $ conda init bash


Then logout and relogin again.

Create Conda Environment(one time  only) 


.. code-block:: console

   $ conda create -n bio python=3.9 scikit-learn pandas jupyter blast bioconductor-kebabs=1.24.0 -c conda-forge -c bioconda  

Wait....!


Activate environment when you want to work on project environment


.. code-block:: console

   $ conda env list

   $  conda activate bio


 Add new library to Working Environment 


.. code-block:: console

   $ pip install pssmpro

   $ jupyter notebook

In side your notebook your can verify that you can work with new installed package 


.. code-block:: console

   from pssmpro.features import create_pssm_profile 


Reference:
   `Command-line blast example <https://hackmd.io/@AstrobioMike/command-line-blast-example>`_

   `Generate PSSM profiles for protein sequences <https://github.com/deeprob/pssmpro>`_

   `Thioesterases based on ensemble learning <https://github.com/deeprob/ThioesteraseEnzymeSpecificity>`_

