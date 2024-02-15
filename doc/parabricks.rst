NVIDIA Parabricks
=========================

NVIDIA® Parabricks® is a scalable genomics analysis software suite that leverages full-stack accelerated computing to process data in minutes. Compatible with all leading sequencing instruments, it supports diverse bioinformatics workflows and integrates AI for accuracy and customization. A cost-effective and space-saving solution, Parabricks is ideal for large-scale genomics projects focused on advancing disease understanding and management.

NODE LOCK LICENSE
--------------------------------------------------------------------
Omega compute node is locked license for running NVIDIA Parabricks, user can allocate resource with salloc or SBATH Slurm job submission as


   $ salloc -w omega -t 1:0:0 --gres=gpu:1
.. code-block:: console


EXAMPLE RUN
--------------------------------------------------------------------

Run the fq2bam tool, which aligns, co-ordinate sorts and marks duplicates # in a pair-ended fastq file. Ref.fa is the bwa-indexed reference file.  

You can download a sample dataset using the following command:

 $ wget -O parabricks_sample.tar.gz \
"https://s3.amazonaws.com/parabricks.sample/parabricks_sample.tar.gz"
.. code-block:: console

To run the sample dataset:

   $ module load parabricks/3.7.0-1.ampere-extra-tools

   $ pbrun fq2bam --ref \
/shared/dataset/parabricks_sample/Ref/Homo_sapiens_assembly38.fasta \
--in-fq /shared/dataset/parabricks_sample/Data/sample_1.fq.gz /shared/dataset/parabricks_sample/Data/sample_2.fq.gz --out-bam output.bam\

.. code-block:: console

The above test should take under 250 seconds on a 4 V100 and 32 seconds on a A100 GPU system.

