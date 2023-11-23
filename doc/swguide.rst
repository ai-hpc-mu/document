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
$ singularity run --nv -B $PWD:/host_pwd --pwd /host_pwd /shared/software/singularity/images/relion_3.1.3.sif ./run_relion.sh 

Software Define Radio and Cloud Radio Access Network:
-----------------------------------------------------
GNU Radio is a free & open-source software development toolkit that provides signal processing blocks to implement software radios. It can be used with readily-available low-cost external RF hardware to create software-defined radios, or without hardware in a simulation-like environment. It is widely used in research, industry, academia, government, and hobbyist environments to support both wireless communications research and real-world radio systems.

`GNURadio <https://https://www.gnuradio.org/>`_

Console::

$ salloc -w turing -t 1:0:0 -c 8 --mem=16G --gres=gpu:1
$ ssh turing
$ singularity shell --nv /app/gnuradio-3.10.sif
$ gnuradio-companion &

Macromolecular Modeling and Visualization:
==========================================
Biomolecular simulation

VMD:
---

VMD is designed for modeling, visualization, and analysis of biological systems such as proteins, nucleic acids, lipid bilayer assemblies, etc. It may be used to view more general molecules, as VMD can read standard Protein Data Bank (PDB) files and display the contained structure. VMD provides a wide variety of methods for rendering and coloring a molecule: simple points and lines, CPK spheres and cylinders, licorice bonds, backbone tubes and ribbons, cartoon drawings, and others. VMD can be used to animate and analyze the trajectory of a molecular dynamics (MD) simulation. In particular, VMD can act as a graphical front end for an external MD program by displaying and animating a molecule undergoing simulation on a remote computer.

`Theoretical and Computational BioPhysics <https://www.ks.uiuc.edu/Research/vmd/>`_

Console::

   $ singularity shell --nv /app/vmd1.9.4.sif
   Singularity> vmd
   rlwrap: Command not found.
   Info) VMD for LINUXAMD64, version 1.9.4a44 (June 22, 2020)
   Info) http://www.ks.uiuc.edu/Research/vmd/
   Info) Email questions and bug reports to vmd@ks.uiuc.edu
   Info) Please include this reference in published work using VMD:
   Info)    Humphrey, W., Dalke, A. and Schulten, K., `VMD - Visual
   Info)    Molecular Dynamics', J. Molec. Graphics 1996, 14.1, 33-38.
   Info) -------------------------------------------------------------
   Info) Multithreading available, 256 CPUs detected.
   Info)   CPU features: SSE2 AVX AVX2 FMA
   Info) Free system memory: 980GB (97%)
   Info) Creating CUDA device pool and initializing hardware...
   Info) Unable to load NVML library, GPU-CPU affinity unavailable.
   Info) Detected 8 available CUDA accelerators, 28 P2P links, 1 island:
   Info) [0-7] NVIDIA A100-SXM4-40GB 108 SM_8.0 1.4 GHz, 40GB RAM AE3 ZC
   Info) Detected 8 available TachyonL/OptiX ray tracing accelerators
   Info)   Compiling 1 OptiX shaders on 8 target GPUs...
   Info) Dynamically loaded 3 plugins in directory:
   Info) /usr/local/lib/vmd/plugins/LINUXAMD64/molfile
   vmd >

