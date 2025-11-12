component_directive
===================

.. py:module:: component_directive

.. autoapi-nested-parse::

   A directive to generate the list of all the built-in components.

   Read the content of the component folder and generate a list of all the components.
   This list will display some informations about the component and a link to the
   GitHub file.

   ..
       !! processed by numpydoc !!


Attributes
----------

.. autoapisummary::

   component_directive.logger


Classes
-------

.. autoapisummary::

   component_directive.ComponentListDirective


Functions
---------

.. autoapisummary::

   component_directive.setup


Module Contents
---------------

.. py:class:: ComponentListDirective(name, arguments, options, content, lineno, content_offset, block_text, state, state_machine)

   Bases: :py:obj:`sphinx.util.docutils.SphinxDirective`


   
   A directive to generate the list of all the built-in components.

   Read the content of the component folder and generate a list of all the components.
   This list will display some informations about the component and a link to the
   GitHub file.















   ..
       !! processed by numpydoc !!

   .. py:method:: run()

      
      Create the list.
















      ..
          !! processed by numpydoc !!


   .. py:attribute:: final_argument_whitespace
      :value: True


      
      May the final argument contain whitespace?
















      ..
          !! processed by numpydoc !!


   .. py:attribute:: has_content
      :value: True


      
      May the directive have content?
















      ..
          !! processed by numpydoc !!


   .. py:attribute:: name
      :value: 'component-list'



   .. py:attribute:: optional_arguments
      :value: 0


      
      Number of optional arguments after the required arguments.
















      ..
          !! processed by numpydoc !!


   .. py:attribute:: required_arguments
      :value: 0


      
      Number of required directive arguments.
















      ..
          !! processed by numpydoc !!


.. py:function:: setup(app)

   
   Add custom configuration to sphinx app.

   :param app: the Sphinx application

   :returns: the 2 parallel parameters set to ``True``.















   ..
       !! processed by numpydoc !!

.. py:data:: logger

