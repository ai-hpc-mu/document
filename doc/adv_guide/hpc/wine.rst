=========================
Wine: Windows Application 
#########################
MS Excel  are outstanding tool for data analytics event organization investment yearly analysis, parameter optimization with VBA Macro on excel files. What if they run 1x PCs for whole night in computer lab, then HPC CPUs.
`Wine on HPC cluster  <https://www.osc.edu/resources/available_software/software_list/wine>`_

Excel Macro Runner Docker 
------------------------------
This Singularity container provides a solution to run Excel macros using Python win32 on a Wine and Office environment.
`Excel Macro Runner Docker <https://github.com/xeden3/docker-excel-macro-run>`_

GitHub Installation

1. Clone the repository:

.. code-block:: console

   $ git clone https://github.com/xeden3/docker-excel-macro-run.git
   $ cd docker-excel-macro-run

2. Build the Docker image:

.. code-block:: console

   $ docker build -t docker-excel-macro-run:v1 . 

3. Usage

.. code-block:: console

   $ docker run -v ./example.xlsm:/opt/wineprefix/drive_c/test.xlsm --rm docker-excel-macro-run:v1 test.xlsm ThisWorkbook.WriteDataToSheet1

4. Singularity?
