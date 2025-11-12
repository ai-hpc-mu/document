gallery_directive
=================

.. py:module:: gallery_directive

.. autoapi-nested-parse::

   A directive to generate a gallery of images from structured data.

   Generating a gallery of images that are all the same size is a common
   pattern in documentation, and this can be cumbersome if the gallery is
   generated programmatically. This directive wraps this particular use-case
   in a helper-directive to generate it with a single YAML configuration file.

   It currently exists for maintainers of the pydata-sphinx-theme,
   but might be abstracted into a standalone package if it proves useful.

   ..
       !! processed by numpydoc !!


Attributes
----------

.. autoapisummary::

   gallery_directive.GRID_CARD
   gallery_directive.TEMPLATE_GRID
   gallery_directive.logger


Classes
-------

.. autoapisummary::

   gallery_directive.GalleryGridDirective


Functions
---------

.. autoapisummary::

   gallery_directive.setup


Module Contents
---------------

.. py:class:: GalleryGridDirective(name, arguments, options, content, lineno, content_offset, block_text, state, state_machine)

   Bases: :py:obj:`sphinx.util.docutils.SphinxDirective`


   
   A directive to show a gallery of images and links in a Bootstrap grid.

   The grid can be generated from a YAML file that contains a list of items, or
   from the content of the directive (also formatted in YAML). Use the parameter
   "class-card" to add an additional CSS class to all cards. When specifying the grid
   items, you can use all parameters from "grid-item-card" directive to customize
   individual cards + ["image", "header", "content", "title"].

   .. danger::

      This directive can only be used in the context of a Myst documentation page as
      the templates use Markdown flavored formatting.















   ..
       !! processed by numpydoc !!

   .. py:method:: run()

      
      Create the gallery grid.
















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
      :value: 'gallery-grid'



   .. py:attribute:: option_spec
      :type:  ClassVar[dict[str, Any]]

      
      Mapping of option names to validator functions.
















      ..
          !! processed by numpydoc !!


   .. py:attribute:: optional_arguments
      :value: 1


      
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

.. py:data:: GRID_CARD
   :value: Multiline-String

   .. raw:: html

      <details><summary>Show Value</summary>

   .. code-block:: python

      """
      ````{{grid-item-card}} {title}
      {options}
      
      {content}
      ````
      """

   .. raw:: html

      </details>



.. py:data:: TEMPLATE_GRID
   :value: Multiline-String

   .. raw:: html

      <details><summary>Show Value</summary>

   .. code-block:: python

      """
      `````{{grid}} {columns}
      {options}
      
      {content}
      
      `````
      """

   .. raw:: html

      </details>



.. py:data:: logger

