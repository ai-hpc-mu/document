tests.utils.check_warnings
==========================

.. py:module:: tests.utils.check_warnings

.. autoapi-nested-parse::

   Check the list of warnings produced by a doc build.

   ..
       !! processed by numpydoc !!


Attributes
----------

.. autoapisummary::

   tests.utils.check_warnings.file


Functions
---------

.. autoapisummary::

   tests.utils.check_warnings.check_warnings


Module Contents
---------------

.. py:function:: check_warnings(file)

   
   Check the list of warnings produced by a doc build.

   Raise errors if there are unexpected ones and/or if some are missing.

   :param file: the path to the generated warning.txt file from
                the CI build

   :returns: 0 if the warnings are all there
             1 if some warning are not registered or unexpected















   ..
       !! processed by numpydoc !!

.. py:data:: file

