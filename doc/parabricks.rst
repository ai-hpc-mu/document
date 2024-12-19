NVIDIA Parabricks
=========================

NVIDIA® Parabricks® is a scalable genomics analysis software suite that leverages full-stack accelerated computing to process data in minutes. Compatible with all leading sequencing instruments, it supports diverse bioinformatics workflows and integrates AI for accuracy and customization. A cost-effective and space-saving solution, Parabricks is ideal for large-scale genomics projects focused on advancing disease understanding and management.

Test on a compute node
--------------------------------------------------------------------
For testing purpose, user can allocate resource with salloc or SBATH Slurm job submission as


.. code-block:: console

    $ salloc -w <node-name> -t 1:0:0 --gres=gpu:1

EXAMPLE RUN
--------------------------------------------------------------------

Run the fq2bam tool, which aligns, co-ordinate sorts and marks duplicates # in a pair-ended fastq file. Ref.fa is the bwa-indexed reference file.  

You can download a sample dataset using the following command:(We have already downloaded it for you.)


.. code-block:: console

   $ wget -O parabricks_sample.tar.gz \
   "https://s3.amazonaws.com/parabricks.sample/parabricks_sample.tar.gz"

To run the sample dataset:

.. code-block:: console

   $ module load singularity
   $ singularity run --nv -B /cm/shared/dataset/parabricks/sample:/sample \
    ../clara-parabricks_4.4.0-1.sif pbrun fq2bam --ref \
        /sample/Ref/Homo_sapiens_assembly38.fasta \
        --in-fq /sample/Data/sample_1.fq.gz /sample/Data/sample_2.fq.gz --out-bam output.bam


The above test should take under 250 seconds on a 4 V100 and 32 seconds on a A100 GPU system.
Lastly, it is only 21 seconds on H100.

.. code-block:: console

   [PB Info 2024-Dec-19 16:09:56] ------------------------------------------------------------------------------
   [PB Info 2024-Dec-19 16:09:56] ||        Program:                          Marking Duplicates, BQSR        ||
   [PB Info 2024-Dec-19 16:09:56] ||        Version:                                           4.4.0-1        ||
   [PB Info 2024-Dec-19 16:09:56] ||        Start Time:                       Thu Dec 19 16:09:35 2024        ||
   [PB Info 2024-Dec-19 16:09:56] ||        End Time:                         Thu Dec 19 16:09:56 2024        ||
   [PB Info 2024-Dec-19 16:09:56] ||        Total Time:                                     21 seconds        ||
   [PB Info 2024-Dec-19 16:09:56] ------------------------------------------------------------------------------


