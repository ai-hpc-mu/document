
Apptainer/Singularity
==============
Apptainer (formerly known as Singularity) is a free and open-source container platform that allows you to create and run applications in isolated images (also called “containers”) in a simple, portable, fast, and secure manner. It performs operating system level virtualization known as containerization. Many container platforms are available, but Apptainer is designed to bring containers and reproducibility to the scientific community and High-Performance Computing (HPC) use cases. Using Apptainer, developers can work in reproducible environments of their choice and design, and these complete environments can be easily copied and executed on other platforms.

Basic Usage
---------------------
...

Build Apptainer Image without root privilage
-------------------------------------------

Let’s install dependencies to your PC, using root privilege 

On your own PC::

sudo apt-get install -y \
    build-essential \
    libseccomp-dev \
    pkg-config \
    uidmap \
    squashfs-tools \
    squashfuse \
    fuse2fs \
    fuse-overlayfs \
    fakeroot \
    cryptsetup \
    curl wget git \
    openssl libssl-dev \
    uuid-dev  uuid  \
    seccomp gperf


Next, install Go::

$ export GOVERSION=1.19.6 OS=linux ARCH=amd64  # change this as you need
$ wget -O /tmp/go${GOVERSION}.${OS}-${ARCH}.tar.gz \
  https://dl.google.com/go/go${GOVERSION}.${OS}-${ARCH}.tar.gz
$ sudo tar -C /usr/local -xzf /tmp/go${GOVERSION}.${OS}-${ARCH}.tar.gz

Clone the repo::

git clone https://github.com/apptainer/apptainer.git
cd apptainer
git checkout release-1.2


Compiling Apptainer:
export  PKG_CONFIG_PATH=/usr/lib/x86_64-linux-gnu/pkgconfig/
./mconfig --without-suid --prefix=/home/snit/apptainer && \
make -C ./builddir && \
make -C ./builddir install

Archive apptainer to be ready for transfer to HPC cluster::
$ cd ~
$ tar zcvf apptainer.tar.gz apptainer
$ scp to HPC cluster from your box
$ scp apptainer.tar.gz snit.san@aim3.mahidol.ac.th:/home/snit.san
$ tar xvfz apptainer.tar.gz

and setup environmental variables::
$ echo 'export PATH=~/apptainer/bin:$PATH' >> ~/.bashrc && \
$ source ~/.bashrc
$ apptainer --version


Building SIF
Create lolcow.def as described below on your own box::

BootStrap: docker

From: ubuntu:22.04%post
apt-get -y update
apt-get -y install fortune cowsay lolcat%environment
export LC_ALL=C
export PATH=/usr/games:$PATH%runscript
fortune | cowsay | lolcat

Compiling Apptainer on PC BOX
You can configure, build, and install Apptainer using the following commands::

$ ./mconfig
$ cd ./builddir
$ make
$ sudo make install

And that's it! Now you can check your Apptainer version by running::

$ apptainer --version

Running SIF on Compute node zeta
Let’s run SIF using non-root version of Apptainer! 

Install addition package on compute node::

$ sudo apt-get install squashfuse fuse2fs

Wait until now bug on Zeta then install others nodes::

$  apptainer run lolcow.sif
