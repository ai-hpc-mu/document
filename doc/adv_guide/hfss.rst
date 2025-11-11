Ansys HFSS
==========
Welcome to our HPC environment. If your work involves **Ansys HFSS**, you are likely tackling some of the most computationally demanding challenges in electronics design. As a leading 3D electromagnetic (EM) simulator for high-frequency products like antennas, RF components, and high-speed PCBs, HFSS simulations can easily exhaust the memory and processing power of a standard workstation. By running your HFSS simulations on our cluster, you can leverage high-core-count nodes and significant memory resources to solve larger, more complex models, run extensive design sweeps, and drastically reduce your time-to-solution.

Steps to use HFSS on cluster

Create tmp and design folders.
------------------------------

.. code-block:: console 

   $ mkdir tmp
   $ mkdir ansys/hfss

At allocated compute node.

Activate singularity and run hfss image
----------------------------------------

.. code-block:: console

   $ module load singularity

   $ singularity instance start -B /home/<user>/tmp:/tmp -B /home/<user>/ansys/hfss:/root/Ansysoft  hfss_vnc.sif hfss_instance 


This software license is depended on MUIT `Ansys license.  <https://muit.mahidol.ac.th/documents/userguide/install-programs/ansys-MU-Installation-Setup-Tutorial.pdf>`_

Xterminal with ssh tunnelling will build window of Electrotronics Desktop.

Stop singularity instance
-------------------------
$ singularity instance stop hfss_instance
