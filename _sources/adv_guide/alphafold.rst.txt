AlphaFold 3: The Inference Pipeline
================================================================

AlphaFold3 represents a significant advancement in the field of protein structure prediction, building on the success of its predecessors. This model excels in predicting the 3D structures of protein-protein complexes directly from their sequences, offering deeper insights into biomolecular interactions. AlphaFold3 synergizes with other methods to predict the effects of mutations on protein interactions, providing a more comprehensive understanding of binding energies. Despite its advancements, AlphaFold3 still faces challenges in modeling full atomic details, which are better addressed by force field methods. Future integration of these approaches could enhance the accuracy of predictions. This breakthrough has far-reaching implications for protein engineering and drug discovery. [1]

The Nobel Prize in Chemistry 2024 was awarded to:

David Baker (University of Washington, USA) for his work on computational protein design. He has successfully created entirely new kinds of proteins, which can be used in pharmaceuticals, vaccines, nanomaterials, and sensors.

Demis Hassabis and John Jumper (Google DeepMind, UK) for their development of AlphaFold2, an AI model that predicts protein structures from amino acid sequences. This breakthrough has solved a 50-year-old problem and has been used to predict the structure of nearly all known proteins, aiding in scientific research and applications like understanding antibiotic resistance and creating enzymes to decompose plastic.

These discoveries highlight the incredible potential of proteins as chemical tools and open up vast possibilities for future scientific advancements.

Beyond AlphaFold 2, Google recently released AlphaFold 3 as a service. Access to the model is restricted: "you may only use AlphaFold 3 model parameters if received directly from Google". The package became available as of November 2024 based on the GitHub repository. [3][4]


Dataset
-------
AlphaFold 3 needs multiple genetic (sequence) protein and RNA databases to run:

- BFD small
- MGnify
- PDB (structures in the mmCIF format)
- PDB seqres
- UniProt
- UniRef90
- NT
- RFam
- RNACentral

.. important::

   These datasets are available on the local cluster at ``/cm/shared/dataset/alphafold3``.

ALPHAFOLD 3 MODEL PARAMETERS TERMS OF USE
------------------------------------------
AlphaFold3 is described as 'open source', but this is not fully the case — model weights can only be accessed upon request, and the code may only be used for non-commercial applications. [4] You must agree to the `ALPHAFOLD 3 MODEL PARAMETERS TERMS OF USE <https://github.com/google-deepmind/alphafold3/blob/main/WEIGHTS_TERMS_OF_USE.md>`_ before use.

.. important::

   Model parameters are available on the local cluster at ``/cm/shared/models/alphafold3``.

Step 0: Clone AlphaFold 3 Source Code
--------------------------------------
First, clone the source code to run the pipeline.
Assume you are on an allocated compute node with one or more GPUs.

.. code-block:: console

   $ salloc -t 1:0:0 -c 32 --mem=64GB  --gres=gpu:1
   $ ssh <allocated node>
   $ cd $HOME
   $ git clone https://github.com/google-deepmind/alphafold3.git


Step 1: Create AlphaFold 3 Input
----------------------------------
To predict a structure, prepare the input sequence file in JSON format: ``fold_input.json``.


.. code-block:: console

   $ cd alphafold3

   $ mkdir af_input af_output

   $ vi fold_input.json

   {

     "name": "2PV7",

     "sequences": [

       {

         "protein": {

            "id": ["A", "B"],

            "sequence": "GMRESYANENQFGFKTINSDIHKIVIVGGYGKLGGLFARYLRASGYPISILDREDWAVAESILANADVVIVSVPINLTLETIERLKPYLTENMLLADLTSVKREPLAKMLEVHTGAVLGLHPMFGADIASMAKQVVVRCDGRFPERYEWLLEQIQIWGAKIYQTNATEHDHNMTYIQALRHFSTFANGLHLSKQPINLANLLALSSPIYRLELAMIGRLFAQDAELYADIIMDKSENLAVIETLKQTYDEALTFFENNDRQGFIDAFHKVRDWFGDYSEQFLKESRQLLQQANDLKQG"

         }

       }

     ],

    "modelSeeds": [1],

    "dialect": "alphafold3",

    "version": 1

   }

This creates two folders: ``af_input`` for input files and ``af_output`` for results.


Step 2: Run AlphaFold 3 in Singularity Container
--------------------------------------------------
A Singularity image is pre-built at ``/app``. The following command runs structure prediction on the input sequence.


.. code-block:: console

   $ ~/alphafold3$ singularity exec \
     --nv \
     -B /home/snit.san/alphafold3/af_input:/root/af_input \
     -B /home/snit.san/alphafold3/af_output:/root/af_output \
     -B /cm/shared/models/alphafold3:/root/models \
     -B /cm/shared/dataset/alphafold3:/root/public_databases \
     /app/alphafold3.sif \
     python /home/snit.san/alphafold3/run_alphafold.py \
     --json_path=/root/af_input/fold_input.json \
     --model_dir=/root/models \
     --db_dir=/root/public_databases \
     --output_dir=/root/af_output

For testing, this will take time. Batch job submission is covered in the SLURM guide.

Step 3: View Output
--------------------
AlphaFold 3 writes results to ``af_output``. CIF structure files are placed inside that directory. Use ChimeraX to visualize the predicted structure.

.. code-block:: console

   $ singularity shell /app/chimerax.sif


References
----------

1. `Press release. NobelPrize.org. Nobel Prize Outreach AB 2024. Fri. 15 Nov 2024. <https://www.nobelprize.org/prizes/chemistry/2024/press-release/>`_

2. `Abramson, J., Adler, J., Dunger, J. et al. Accurate structure prediction of biomolecular interactions with AlphaFold 3. Nature 630, 493–500 (2024). <https://www.nature.com/articles/s41586-024-07487-w>`_

3. `AlphaFold 3 Package: GitHub <https://github.com/google-deepmind/alphafold3>`_

4. `Nature: AI protein-prediction tool AlphaFold 3 is now more open <https://www.nature.com/articles/d41586-024-03708-4>`_
