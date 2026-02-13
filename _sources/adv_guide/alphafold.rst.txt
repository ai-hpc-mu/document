AlphaFold 3 :  The inference pipeline 
================================================================

AlphaFold3 represents a significant advancement in the field of protein structure prediction, building on the success of its predecessors. This model excels in predicting the 3D structures of protein-protein complexes directly from their sequences, offering deeper insights into biomolecular interactions. AlphaFold3 synergizes with other methods to predict the effects of mutations on protein interactions, providing a more comprehensive understanding of binding energies. Despite its advancements, AlphaFold3 still faces challenges in modeling full atomic details, which are better addressed by force field methods. Future integration of these approaches could enhance the accuracy of predictions. This breakthrough has far-reaching implications for protein engineering and drug discovery.[1]

The Nobel Prize in Chemistry 2024 was awarded to:

David Baker (University of Washington, USA) for his work on computational protein design. He has successfully created entirely new kinds of proteins, which can be used in pharmaceuticals, vaccines, nanomaterials, and sensors.

Demis Hassabis and John Jumper (Google DeepMind, UK) for their development of AlphaFold2, an AI model that predicts protein structures from amino acid sequences. This breakthrough has solved a 50-year-old problem and has been used to predict the structure of nearly all known proteins, aiding in scientific research and applications like understanding antibiotic resistance and creating enzymes to decompose plastic.
These discoveries highlight the incredible potential of proteins as chemical tools and open up vast possibilities for future scientific advancements.

Beyond AlphaFold 2, recently Google release AlphaFold 3 as service. We have to access to model and service that is avavailabel on provider resources.
Surprisingly that "you may only use AlphaFold 3 model parameters if received directly from Google". The pacakge is available about 10 November, 2024 based on Github repository.[3][4]


Dataset 
------
AlphaFold 3 needs multiple genetic (sequence) protein and RNA databases to run:

BFD small
MGnify
PDB (structures in the mmCIF format)
PDB seqres
UniProt
UniRef90
NT
RFam
RNACentral

.. important:: 
I uploaded those on our local cluster at '/cm/shared/dataset/alphafold3'

ALPHAFOLD 3 MODEL PARAMETERS TERMS OF USE
-----------------------------------------
AlphaFold3 is now ‘open source’. This is not the case, as weights for the model can only be accessed upon request, and the code can only be used for non-commercial applications[4]. We have to agree up on how to use this model, `ALPHAFOLD 3 MODEL PARAMETERS TERMS OF USE<https://github.com/google-deepmind/alphafold3/blob/main/WEIGHTS_TERMS_OF_USE.md>`_

.. important:: 
I uploaded model parameters on our local cluster at '/cm/shared/models/alphafold3'.

Step 0: Clone Alphafold 3 source code
-------------------------------------
Firt we need source code to run pipeline.
Assumed you are on allocated compute node with gpu or gpus.

.. code-block:: console

   $ salloc -t 1:0:0 -c 32 --mem=64GB  --gres=gpu:1
   $ ssh <allocated node>
   $ cd $HOME
   $ git clone https://github.com/google-deepmind/alphafold3.git


Step 1: Create Alphafold 3 input 
----------------------------------
To predict structure, we need input sequence file in JSON format: fold_input.json


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

We create two folders for 'af_input' and 'af_output'.


Step 2: Run Alphafold 3 in container, Singularity
-----------------------------------------
We build singularity image on /app folder. The following is sample parameter for predicting input the sequence.



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



  For testing, this is take time. Later, we will submit batch job. Figure out how to reduce prediction time.

Step 3: View oupput
-------------------
Alphafold 3 generates output to 'af_output'. Inside that directory, CIFs are  placed. You can use 'Chimerax' for verify structure.

.. code-block:: console

   $ singularity shell /app/chimerax.sif


Reference:
----------

   1. `Press release. NobelPrize.org. Nobel Prize Outreach AB 2024. Fri. 15 Nov 2024. <https://www.nobelprize.org/prizes/chemistry/2024/press-release/>`_

   2. `Abramson, J., Adler, J., Dunger, J. et al. Accurate structure prediction of biomolecular interactions with AlphaFold 3. Nature 630, 493–500 (2024). https://doi.org/10.1038/s41586-024-07487-w <https://https://www.nature.com/articles/s41586-024-07487-w>`_

   3. `AlphaFold 3 Package: github <https://github.com/google-deepmind/alphafold3>`_
   4. `Nature: AI protein-prediction tool AlphaFold3 is now more open<https://www.nature.com/articles/d41586-024-03708-4>`_

