Cryogenic electron microscopy
=================================

Cryogenic electron microscopy (cryoEM) is a cryomicroscopy technique applied on samples cooled to cryogenic temperatures. For biological specimens, the structure is preserved by embedding in an environment of vitreous ice. 
`Cryogenic electron microscopy <https://en.wikipedia.org/wiki/Cryogenic_electron_microscopy#:~:text=Cryogenic%20electron%20microscopy%20(cryoEM)%20is,an%20environment%20of%20vitreous%20ice.>`_

relion-4.0 for cryo-EM structure determination
-----------------------------------------------
Relion-4 cover  the entire single-particle analysis workflow in relion-4.0: beam-induced motion-correction, CTF estimation; automated particle picking; particle extraction; 2D class averaging; automated 2D class selection; SGD-based initial model generation; 3D classification; high-resolution 3D refinement; CTF refinement and higher-order aberration correction; the processing of movies from direct-electron detectors; and final map sharpening and local-resolution estimation. 
`RELION 4.0 Document  <https://relion.readthedocs.io/en/release-4.0/SPA_tutorial/Introduction.html>`_

Relion 3 or 4 on Exascale Cluster with Singularity
--------------------------------------------------
This is very simple guide to run Relion on a DGX100, more effective multinodes should be explore futher.
Assume you allocate resource on one of our compute nodes by salloc command.
.. code-block:: console

   $ salloc -w omega -t 1:0:0 --gres=gpu:1

Download Data
-------------
You can download data from Takayuki Kato from the Namba group at Osaka university, Japan. It was collected on a JEOL CRYO ARM 200 microscope.The data and our precalculated results may be downloaded and unpacked using the commands below.

.. code-block:: console

   cd ~/
   mkdir relion/tutorial/
   wget ftp://ftp.mrc-lmb.cam.ac.uk/pub/scheres/relion30_tutorial_data.tar
   wget ftp://ftp.mrc-lmb.cam.ac.uk/pub/scheres/relion40_tutorial_precalculated_results.tar.gz
   tar -xf relion30_tutorial_data.tar
   tar -zxf relion40_tutorial_precalculated_results.tar.gz


Signle particle tutorial
-------------------------
.. code-block:: console
  
   $ singularity shell --nv /app/relion4_gui_cufftw.sif
   Singularity> relion &

.. image:: images/relion.png

This image is NOT the best one which we will improve Singularity definition file to run on multi-nodes with Slurm scheduling.


`RELION Single particle tutorial  <https://relion.readthedocs.io/en/release-4.0/SPA_tutorial/index.html>`_
