

RStudio Server
==============


One time setup
---------------------
Console::

$ TMPDIR=~/rstudio-tmp # your choice
$ mkdir -p $TMPDIR/tmp/rstudio-server
$ uuidgen > $TMPDIR/tmp/rstudio-server/secure-cookie-key
$ chmod 600 $TMPDIR/tmp/rstudio-server/secure-cookie-key
$ mkdir -p $TMPDIR/var/{lib,run}

Run application with Singularity
--------------------------------------
Allocate resource::

        $ salloc -w node_name -t 1:0:0

or
Use browser with remote desktop on exascale web portal::

$ TMPDIR=~/rstudio-tmp && singularity exec    -B $TMPDIR/var/lib:/var/lib/rstudio-server     -B $TMPDIR/var/run:/var/run/rstudio-server     -B $TMPDIR/tmp:/tmp    /app/geospatial_latest.sif   rserver --www-address=$(hostname -I | awk '{print $1}') --server-user=$USER --www-port=8989

Port Modification
-----------------------
Port : If port has been already used, change it.

Connect to RStudio Server via browser::
        http://compute_node.mahidol.ac.th:port

