Extreme-scale Scientific Software Stack (E4S)
==============================================

The Extreme-scale Scientific Software Stack (E4S) Project is supported by the US Department of Energy Advanced Scientific Computing Research Office and is a legacy of Exascale Computing Project (ECP). The packages distributed with E4S contain contributions from hundreds of open source community developers. The top-level packages are listed on the E4S :-

`Information Page  <https://e4s-project.github.io/DocPortal.html>`_

Run with Container
------------------
E4S can be used at MAI by Singularity containver image :- 


.. code-block:: console

   $ singularity run --nv /app/e4s-cuda80-x86_64-24.02.sif  

List available pageckage (133 at date of writting April 8, 2024)

.. code-block:: console

   $ module av

Support we want run paraview

.. code-block:: console

   $ module load paraview
   $ paraview

Parallel Electronic Simulation
------------------------------
To run Xyce Spice-compatible Parallel Electronic Simulation
   
.. code-block:: console

   $ more cir.nlist
   Simple Example of .RESULT capability with .STEP
   R1 a b 10.0
   R2 b 0 2.0
   .GLOBAL_PARAM v_amplitude=2.0
   Va a 0 sin (5.0 {v_amplitude} 1.0 0.0 0.0)
   .PRINT TRAN v(b) {v(b)*v(b)/2}
   .TRAN 0 0.75
   .STEP R2 1.0 2.0 1.0
   .STEP v_amplitude 1.0 2.0 1.0
   .RESULT {v(b)}
   .RESULT {v(b)*v(b)/2}
   .END

   $ Xyce  cir.nlist

