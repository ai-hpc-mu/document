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

Amber:
------

Amber is the collective name for a suite of programs that allow users to carry out molecular dynamics simulations, particularly on biomolecules. The Amber software suite is divided into two parts: AmberTools23, a collection of freely available programs mostly under the GPL license, and Amber22, which is centered around the pmemd simulation  program, and which continues to be licensed as before, under a more restrictive license.

AmberTools is a set of programs for biomolecular simulation and analysis. They are designed to work well with each other, and with the “regular” Amber suite of programs. You can perform many simulation tasks with AmberTools, and you can do more extensive simulations with the combination of AmberTools and Amber itself. Most components of AmberTools are released under the GNU General Public License (GPL). A few components
are in the public domain or have other open-source licenses.

`The Ameber Chemistry through a Computational Lens <https://ambermd.org/index.php>`_

`Running Molecular Dynamics on Exascale AI/HPC Mahidol University Cluster with AMBER <https://snitgit.github.io/MolecularSim-Amber-lesson/>`_

Console::

   $ singularity shell --nv /app/amber22T23.sif
   Singularity> source /opt/amber22/amber.sh
   Singularity> tleap -f leaprc.protein.ff19SB
   -I: Adding /opt/amber22/dat/leap/prep to search path.
   -I: Adding /opt/amber22/dat/leap/lib to search path.
   -I: Adding /opt/amber22/dat/leap/parm to search path.
   -I: Adding /opt/amber22/dat/leap/cmd to search path.
   -f: Source leaprc.protein.ff19SB.

   Welcome to LEaP!
   (no leaprc in search path)
   Sourcing: /opt/amber22/dat/leap/cmd/leaprc.protein.ff19SB
   Log file: ./leap.log
   Loading parameters: /opt/amber22/dat/leap/parm/parm19.dat
   Reading title:
   PARM99 + frcmod.ff99SB + frcmod.parmbsc0 + OL3 for RNA + ff19SB
   Loading parameters: /opt/amber22/dat/leap/parm/frcmod.ff19SB
   Reading force field modification type file (frcmod)
   Reading title:
   ff19SB AA-specific backbone CMAPs for protein 07/25/2019
   Loading library: /opt/amber22/dat/leap/lib/amino19.lib
   Loading library: /opt/amber22/dat/leap/lib/aminoct12.lib
   Loading library: /opt/amber22/dat/leap/lib/aminont12.lib
   > s = loadpdb protein.pdb
   Loading PDB file: ./protein.pdb
   -- residue 20: duplicate [ CG] atoms (total 2)
   -- residue 20: duplicate [ OD1] atoms (total 2)
   -- residue 20: duplicate [ OD2] atoms (total 2)
   -- residue 43: duplicate [ CD2] atoms (total 2)
   -- residue 43: duplicate [ CE1] atoms (total 2)
   -- residue 43: duplicate [ CG] atoms (total 2)
   -- residue 43: duplicate [ ND1] atoms (total 2)
   -- residue 43: duplicate [ NE2] atoms (total 2)
   -- residue 90: duplicate [ OG] atoms (total 2)

   Warning: Atom names in each residue should be unique.
        (Same-name atoms are handled by using the first
         occurrence and by ignoring the rest.
         Many instances of duplicate atom names usually come
         from alternate conformations in the PDB file.)

     total atoms in file: 830
    Leap added 811 missing atoms according to residue templates:
       811 H / lone pairs
   > set {s.20 s.26} name "ASH"
   > savepdb s protonated.pdb
   Writing pdb file: protonated.pdb

   Warning:  Converting N-terminal residue name to PDB format: NMET -> MET

   Warning:  Converting C-terminal residue name to PDB format: CVAL -> VAL
   > quit
   Exiting LEaP: Errors = 0; Warnings = 3; Notes = 0.
   Singularity>

`License <https://ambermd.org/GetAmber.php>`_
   Getting Amber22 for commerical use
The license above is valid for both commerical and non-commerical usage. Only the license fee is different from commerical use. Commerical users should fill out this application for a commerical license. This will generate a license form that you can sign, and will contain information about how to pay the license fee.

VMD:
----

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
   vmd > mol new protein.pdb
   Info) Using plugin pdb for structure file protein.pdb
   Info) Using plugin pdb for coordinates from file protein.pdb
   Info) Determining bond structure from distance search ...
   Info) Analyzing structure ...
   Info)    Atoms: 830
   Info)    Bonds: 846
   Info)    Angles: 0  Dihedrals: 0  Impropers: 0  Cross-terms: 0
   Info)    Bondtypes: 0  Angletypes: 0  Dihedraltypes: 0  Impropertypes: 0
   Info)    Residues: 105
   Info)    Waters: 0
   Info)    Segments: 1
   Info)    Fragments: 1   Protein: 1   Nucleic: 0
   Info) Finished with coordinate file protein.pdb.
   vmd > set s [atomselect top "resid 20 26"]
   atomselect0
   vmd > $s set resname ASH
   vmd > set s [atomselect top all]
   atomselect1
   vmd > $s writepdb protonated.pdb
   Info) Opened coordinate file protonated.pdb for writing.
   Info) Finished with coordinate file protonated.pdb.
   vmd > quit
   Info) VMD for LINUXAMD64, version 1.9.4a44 (June 22, 2020)
   Info) Exiting normally.
   Singularity>

