# Contribution Guide

Welcome to the user documentation of the Mahidol Unversity AI and high performance computing (HPC), also called AI/HPC for Research. The MAI HPC cluster is managed by ICT network and system  team (Faculty of Information and Communication Technology). This documentation is maintained by ICT team and the user community. It is a living document that you can update and add to. 


How-To: Contribute to this Document
====================================

The document, user guide and source code is managed using Git and is hosted on GitHub. The recommended way for new contributors to submit information  to MAI document is to fork this repository and submit a pull request after committing changes to their fork. The pull request will then need to be approved by one of the core members before it is merged into the main repository.
If you feel uncomfortable or uncertain about an issue or your changes, feel free to email the mai@mahidol.ac.th.

These are the basic steps needed to start developing on Sphinx.

#. Install Sphinx on Conda Environment

.. code-block:: console

  $ conda create --name workshop 

  $  conda activate workshop 

  $  conda install sphinx 

  $ pip install sphinx-rtd-theme  


Verify version: 

.. code-block:: console

  $ sphinx-build --version 
 

Clone github project

.. code-block:: console

  $ git clone https://github.com/ai-hpc-mu/document.git 

  $ cd document/doc 

Setup project and theme

.. code-block:: console

  $ vi conf.py  
   html_theme = 'sphinx_rtd_theme'

#. Create an account on GitHub. 
#. Fork the repository and add your changes (`more details: <https://docs.github.com/en/github/getting-started-with-github/fork-a-repo>`_) 
#. Learn how to use `Sphinx <https://sublime-and-sphinx-guide.readthedocs.io/en/latest/lists.html#ordered-lists>`_
#. Add a pull request
