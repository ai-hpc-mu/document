profile
=======

.. py:module:: profile

.. autoapi-nested-parse::

   Script to profile the build of the test site with py-spy.

   This can be called with `python tools/profile.py` and will profile the build of the test
   site.
   You can additionally configure the number of extra pages to add to the build with the
   `-n` flag and the output file with the `-o` flag.

   $ python tools/profile.py -n 100 -o profile.svg

   If running within tox (recommended) this can be run with:

   $ tox -e profile-docs -- -n 100 -o profile.svg

   ..
       !! processed by numpydoc !!


Attributes
----------

.. autoapisummary::

   profile.parser


Functions
---------

.. autoapisummary::

   profile.profile_docs


Module Contents
---------------

.. py:function:: profile_docs(output = 'profile.svg', n_extra_pages = 50)

   
   Add a bunch of extra pages to the test site and profile the build with py-spy.

   :param output: The output filename for generated chart, defaults to output.svg.
   :type output: str
   :param n_extra_pages: The number of extra pages to add to the build, defaults to
   :type n_extra_pages: int
   :param 50.:















   ..
       !! processed by numpydoc !!

.. py:data:: parser

