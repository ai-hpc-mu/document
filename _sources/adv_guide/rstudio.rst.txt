Mathematics and Statistics Tools
#################################

MATLAB singularity with License server enabled
==============================================

At allocated compute node; activate singularity and run MATLAB image 

.. code-block:: console

   $module load singularity
   $singularity run /app/matlab2023bLic.sif
   or
   $singularity run /scratch/matlab2023bLic.sif

This software license is depended on MUIT MATLAB license.


RStudio on Jupyter with The Rocker Project
==========================================

Without complicated setup, we can run container and work on jupyter notebook environment.

How to
******

 On any node:  activate singularity

.. code-block:: console

  $ module load singularity
  $ singularity run /app/rstudio.4.4.2.sif

 Connect to RStudio Server via browser::
        http://compute_node.mahidol.ac.th:port

Reference:
`The Rocker Project  <https://rocker-project.org/images/>`_

RStudio Server(Optin II)
==============


One time setup::


Create the required directories first::

  $ TMPDIR=~/rstudio-tmp                                                                                                                    
  $ mkdir -p $TMPDIR/var/lib
  $ mkdir -p $TMPDIR/var/run
  $ mkdir -p $TMPDIR/tmp
  $ mkdir -p $TMPDIR/var/lib/rstudio-server
  $ mkdir -p $TMPDIR/var/run/rstudio-server

Generate a secure cookie key (often the missing piece)::

$ uuid > $TMPDIR/tmp/rstudio-server/secure-cookie-key 2>/dev/null || python3 -c "import uuid; print(uuid.uuid4())" > $TMPDIR/tmp/rstudio-server/secure-cookie-key
$ mkdir -p $TMPDIR/tmp/rstudio-server
$ chmod 600 $TMPDIR/tmp/rstudio-server/secure-cookie-key

Create an rsession.conf and database.conf,  rsession.conf (can be empty or minimal)::
$ touch $TMPDIR/rsession.conf

The database.conf - tells RStudio to use SQLite in a writable location::

$ echo "provider=sqlite directory=$TMPDIR/var/lib/rstudio-server" > $TMPDIR/database.conf

  
Run application with Singularity
--------------------------------------
Allocate resource(without gpu)::

        $ salloc -w node_name -t 1:0:0 


Allocate resource(with gpu)::

        $ salloc -w node_name -t 1:0:0 --gres=gpu:1


Troubleshouting Rstudio::
=========================
Check Hostname::

$hostname
⎿  zeta  

Check RStudio Server::

$ singularity exec /app/geospatial_latest.sif which rserver 2>&1
⎿  /usr/local/bin/rserver 

Check if port 8989 is already in use::

$ ss -tlnp 2>/dev/null | grep 8989 || netstat -tlnp 2>/dev/null | grep 8989 || echo "Port 8989 appears free (or no permissi…)
  ⎿  Port 8989 appears free (or no permission to check)

Check for stale rstudio lock/pid files::

$ ls -la ~/rstudio-tmp/var/run/rstudio-rserver/ 2>&1

stalled files::
                                                                        
srw-rw-rw- 1 snit.san snit.san    0 Feb 13 14:18 session-server-rpc.socket                                                      
                                                                                  
There's a stale socket file from the previous run. Let me also check the rstudio server logs and try a clean run.

Check for any rstudio log files::

$ find ~/rstudio-tmp -name "*.log" -o -name "*.err" 2>/dev/null; ls ~/rstudio-tmp/tmp/rstudio-server/ 2>&1
  ⎿  secure-cookie-key

Clean Stal files::
====================
The fix:  cleaned up the stale files::
                                                                                         
  $ rm -f ~/rstudio-tmp/var/run/rstudio-rserver/session-server-rpc.socket                                                              
  $ rm -f ~/rstudio-tmp/var/lib/rstudio-os.sqlite*  

Start container ::
==================
Singularity run command::

  $ TMPDIR=~/rstudio-tmp && singularity exec -B $TMPDIR/var/lib:/var/lib/rstudio-server -B $TMPDIR/var/run:/var/run/rstudio-server -B $TMPDIR/tmp:/tmp -B $TMPDIR/database.conf:/etc/rstudio/database.conf -B $TMPDIR/rsession.conf:/etc/rstudio/rsession.conf /app/rstudio_4.4.2.sif rserver --www-address=0.0.0.0 --server-user=$USER --www-port=8989 --auth-none=1 --server-data-dir=$TMPDIR/var/run/rstudio-server    --secure-cookie-key-file=$TMPDIR/tmp/rstudio-server/secure-cookie-key

Don't care about following message for now!::
  TTY detected. Printing informational message about logging configuration. Logging configuration loaded from '/etc/rstudio/logging.conf'. Logging to 'syslog'.

Reonnect to RStudio Server via browser::

        http://compute_node.mahidol.ac.th:port


RStudio Customization Library
==============================

*Author: Snit Sanghlao and Claude Code (Anthropic)*

Install RStudio Server in user space on Ubuntu-based HPC cluster nodes,
expose it via Jupyter proxy, and run it alongside a GPU-enabled Conda environment.

Step 1: Download and Extract the Ubuntu Package
------------------------------------------------

Create a private software folder and unpack the RStudio Server binaries locally
(no ``sudo`` or root privileges required).

.. code-block:: bash

   # 1.1  Create your permanent software directory and a temporary working folder
   mkdir -p ~/software/rstudio-server
   mkdir -p ~/software/temp-rstudio
   cd ~/software/temp-rstudio

   # 1.2  Download the Ubuntu 22.04 (Jammy) RStudio Server .deb package
   #      Check https://posit.co/download/rstudio-server/ for the latest link.
   wget https://download2.rstudio.org/server/jammy/amd64/rstudio-server-2026.01.1-403-amd64.deb

   # 1.3  Extract the .deb file locally (no root required)
   dpkg -x rstudio-server-2026.01.1-403-amd64.deb .

   # 1.4  Move the core binaries to your permanent folder and clean up
   mv usr/lib/rstudio-server/* ~/software/rstudio-server/
   cd ~/software
   rm -rf temp-rstudio

Step 2: Create Your Personal Modulefile
----------------------------------------

Create the ``~/privatemodules/rstudio/`` directory and write a modulefile so
that the Environment Modules system can expose the ``rserver`` binary.

.. code-block:: bash

   # 2.1  Create the modulefile directory
   mkdir -p ~/privatemodules/rstudio

   # 2.2  Create the modulefile
   nano ~/privatemodules/rstudio/2026.01.1

Paste the following Tcl content into the file, then save with
``Ctrl+O`` → ``Enter`` and exit with ``Ctrl+X``:

.. code-block:: tcl

   #%Module1.0
   proc ModulesHelp { } {
       puts stderr "Loads RStudio Server 2026.01.1 for Jupyter Proxy"
   }

   module-whatis "RStudio Server (User Space)"

   set RSTUDIO_DIR /home/snit.san/software/rstudio-server

   # Add the binary to your PATH so Jupyter proxy can find 'rserver'
   prepend-path PATH $RSTUDIO_DIR/bin

Step 3: Create the Conda Environment
--------------------------------------

Install JupyterLab, Jupyter Server Proxy, and the RStudio proxy extension via
Conda. The ``rstudio`` Conda package is intentionally omitted because the
user-space binary installed in Step 1 is used instead.

.. code-block:: bash

   # 3.1  Create the GPU-enabled Conda environment
   conda create -n rstudio_gpu -c conda-forge \
       python=3.10 \
       r-base=4.3 \
       r-essentials \
       r-hdf5r \
       jupyterlab \
       jupyter-server-proxy \
       jupyter-rsession-proxy

Step 4: Request a Compute Node and Launch Jupyter
--------------------------------------------------

**4.1 Load the Slurm module:**

.. code-block:: bash

   module load slurm

**4.2 Request an interactive GPU node:**

.. code-block:: bash

   srun --partition=defq --gres=gpu:1 -t 0:1:0 --pty bash

**4.3 On the compute node, set up the environment:**

.. code-block:: bash

   # Tell the cluster where your private modules live
   module use ~/privatemodules

   # Load your custom RStudio module (adds rserver to PATH)
   module load rstudio/2026.01.1

   # Activate the Conda environment
   conda activate rstudio_gpu

   # Force the Conda environment's bin directory to the front of PATH
   export PATH=$CONDA_PREFIX/bin:$PATH

**4.4 Verify that Jupyter resolves correctly:**

.. code-block:: bash

   which jupyter

**4.5 Confirm the proxy extensions are registered:**

.. code-block:: bash

   jupyter server extension list

**4.6 Launch JupyterLab:**

.. code-block:: bash

   jupyter lab --no-browser --ip=$(hostname -i)

Open the URL printed in your terminal in a local browser (you may need an SSH
tunnel). In the JupyterLab Launcher, click the **RStudio** button. The proxy
will locate the ``rserver`` binary from Step 1, connect it to the Conda R 4.3
environment, and start your RStudio session.

