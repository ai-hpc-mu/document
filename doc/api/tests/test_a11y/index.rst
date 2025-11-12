tests.test_a11y
===============

.. py:module:: tests.test_a11y

.. autoapi-nested-parse::

   Using Axe-core, scan the Kitchen Sink pages for accessibility violations.
   Note that in contrast with the rest of our tests, the accessibility tests in this file
   are run against a build of our PST documentation, not purposedly-built test sites.

   ..
       !! processed by numpydoc !!


Attributes
----------

.. autoapisummary::

   tests.test_a11y.playwright


Functions
---------

.. autoapisummary::

   tests.test_a11y.filter_ignored_violations
   tests.test_a11y.format_violations
   tests.test_a11y.test_axe_core
   tests.test_a11y.test_code_block_tab_stop
   tests.test_a11y.test_notebook_ipywidget_output_tab_stop
   tests.test_a11y.test_notebook_output_tab_stop
   tests.test_a11y.test_search_as_you_type


Module Contents
---------------

.. py:function:: filter_ignored_violations(violations, url_pathname)

   
   Filter out ignored axe-core violations.

   In some tests, we wish to ignore certain accessibility violations that we
   won't ever fix or that we don't plan to fix soon.















   ..
       !! processed by numpydoc !!

.. py:function:: format_violations(violations)

   
   Return a pretty string representation of Axe-core violations.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_axe_core(page, url_base, theme, url_pathname, selector)

   
   Should have no Axe-core violations at the provided theme and page section.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_code_block_tab_stop(page, url_base)

   
   Code blocks that have scrollable content should be tab stops.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_notebook_ipywidget_output_tab_stop(page, url_base)

   
   Notebook ipywidget outputs that have scrollable content should be tab stops.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_notebook_output_tab_stop(page, url_base)

   
   Notebook outputs that have scrollable content should be tab stops.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_search_as_you_type(page, url_base)

   
   Search-as-you-type feature should support keyboard navigation.

   When the search-as-you-type (inline search results) feature is enabled,
   pressing Tab after entering a search query should focus the first inline
   search result.















   ..
       !! processed by numpydoc !!

.. py:data:: playwright

