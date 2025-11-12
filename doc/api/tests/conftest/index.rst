tests.conftest
==============

.. py:module:: tests.conftest

.. autoapi-nested-parse::

   Configuration of the pytest session.

   ..
       !! processed by numpydoc !!


Attributes
----------

.. autoapisummary::

   tests.conftest.docs_build_path
   tests.conftest.pytest_plugins
   tests.conftest.repo_path
   tests.conftest.tests_path


Classes
-------

.. autoapisummary::

   tests.conftest.SphinxBuild


Functions
---------

.. autoapisummary::

   tests.conftest.escape_ansi
   tests.conftest.sphinx_build_factory
   tests.conftest.url_base


Module Contents
---------------

.. py:class:: SphinxBuild(app, src)

   
   Helper class to build a test documentation.
















   ..
       !! processed by numpydoc !!

   .. py:method:: build(no_warning = True)

      
      Build the application.
















      ..
          !! processed by numpydoc !!


   .. py:method:: html_tree(*path)

      
      Returns the html tree of the current build.
















      ..
          !! processed by numpydoc !!


   .. py:attribute:: app


   .. py:property:: outdir
      :type: pathlib.Path


      
      Returns the output directory of the current build.
















      ..
          !! processed by numpydoc !!


   .. py:attribute:: src


   .. py:property:: status
      :type: str


      
      Returns the status of the current build.
















      ..
          !! processed by numpydoc !!


   .. py:property:: warnings
      :type: str


      
      Returns the warnings raised by the current build.
















      ..
          !! processed by numpydoc !!


.. py:function:: escape_ansi(string)

   
   Helper function to remove ansi coloring from sphinx warnings.
















   ..
       !! processed by numpydoc !!

.. py:function:: sphinx_build_factory(make_app, tmp_path, request)

   
   Return a factory builder pointing to the tmp directory.
















   ..
       !! processed by numpydoc !!

.. py:function:: url_base()

   
   Start local server on built docs and return the localhost URL as the base URL.
















   ..
       !! processed by numpydoc !!

.. py:data:: docs_build_path

.. py:data:: pytest_plugins
   :value: 'sphinx.testing.fixtures'


.. py:data:: repo_path

.. py:data:: tests_path

