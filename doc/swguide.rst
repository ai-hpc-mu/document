Software Guide
==============

The following guides are intend to introduce basic tools for HPC Bioinformatics tools.

RNA and ChIP-sequencing analysis
---------------------
`RNASeq ChIPseq <https://github.com/vclabsysbio/AI-MD_RNASeq_ChIPseq>`_

`Single-cell RNA-seq <https://github.com/vclabsysbio/AI-MD_scRNAseq>`_

Single Particle Analysis: 
-------------------------
relion (for REgularised LIkelihood OptimisatioN, pronounce rely-on) is a software package that employs an empirical Bayesian approach for electron cryo-microscopy (cryo-EM) structure determination. It is developed in the group of Sjors Scheres at the `MRC Laboratory of Molecular Biology <https://relion.readthedocs.io/en/release-4.0/index.html>`_

Allocate resource for one compute node.
Benchmark result compare to RTX3090 time reduced from 72 minutes to 30 minutes

`RTX3090 and V100 Benchmark <https://www.linuxvixion.com/blog/relion-fastest-ever-benchmark/>`_

Console::


$ cp /shared/dataset/relion/relion_benchmark ~/fastdata -r 
$ cd ~/fastdata/relion_benchmark 
$ singularity -nv -B $PWD:/host_pwd --pwd /host_pwd /shared/software/singularity/images/relion_3.1.3.sif run_relion.sh 


