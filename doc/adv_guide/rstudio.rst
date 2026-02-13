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
  ⎿  total 8                                                                                                                         
     drwxrwxrwt 2 snit.san snit.san 4096 Feb 13 14:18 .                                                                              
     drwxrwxrwt 5 snit.san snit.san 4096 Jul 22  2025 ..                                                                             
     srw-rw-rw- 1 snit.san snit.san    0 Feb 13 14:18 session-server-rpc.socket                                                      
                                                                                  
There's a stale socket file from the previous run. Let me also check the rstudio server logs and try a clean run.

Check for any rstudio log files::

$ find ~/rstudio-tmp -name "*.log" -o -name "*.err" 2>/dev/null; ls ~/rstudio-tmp/tmp/rstudio-server/ 2>&1)                      
  ⎿  secure-cookie-key

Clean Stal files::
====================
The fix: I cleaned up the stale files::
                                                                                         
  $ rm -f ~/rstudio-tmp/var/run/rstudio-rserver/session-server-rpc.socket                                                              
  $ rm -f ~/rstudio-tmp/var/lib/rstudio-os.sqlite*  

Start container ::
==================
Singularity run command::

  $ TMPDIR=~/rstudio-tmp && singularity exec -B $TMPDIR/var/lib:/var/lib/rstudio-server -B $TMPDIR/var/run:/var/run/rstudio-server -B $TMPDIR/tmp:/tmp -B $TMPDIR/database.conf:/etc/rstudio/database.conf -B $TMPDIR/rsession.conf:/etc/rstudio/rsession.conf /app/rstudio_4.4.2.sif rserver --www-address=$(hostname -I | awk '{print $1}')--server-user=$USER --www-port=8989 --auth-none=1 --server-data-dir=$TMPDIR/var/run/rstudio-server    --secure-cookie-key-file=$TMPDIR/tmp/rstudio-server/secure-cookie-key

Don't care about following message for now!::
  TTY detected. Printing informational message about logging configuration. Logging configuration loaded from '/etc/rstudio/logging.conf'. Logging to 'syslog'.

Reonnect to RStudio Server via browser::

        http://compute_node.mahidol.ac.th:port

