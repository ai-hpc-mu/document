tests.test_playwright
=====================

.. py:module:: tests.test_playwright

.. autoapi-nested-parse::

   Build minimal test sites with sphinx_build_factory and test them with Playwright.
   When adding new tests to this file, remember to also add the corresponding test site
   to `tests/sites/` or use an existing one.

   ..
       !! processed by numpydoc !!


Attributes
----------

.. autoapisummary::

   tests.test_playwright.UnsupportedOperation
   tests.test_playwright.playwright
   tests.test_playwright.repo_path
   tests.test_playwright.test_sites_dir


Classes
-------

.. autoapisummary::

   tests.test_playwright.TestCollapseSidebarButton


Functions
---------

.. autoapisummary::

   tests.test_playwright._build_test_site
   tests.test_playwright._check_test_site
   tests.test_playwright._is_overflowing
   tests.test_playwright.test_article_toc_syncing
   tests.test_playwright.test_breadcrumb_expansion
   tests.test_playwright.test_breadcrumbs_everywhere
   tests.test_playwright.test_colors
   tests.test_playwright.test_version_switcher_highlighting


Module Contents
---------------

.. py:class:: TestCollapseSidebarButton

   
   Group the tests for the collapse sidebar button.
















   ..
       !! processed by numpydoc !!

   .. py:method:: test_collapse_sidebar_button(sphinx_build_factory, page, url_base)

      
      Test basic functionality of the collapse sidebar button.

      Clicking the button should collapse the sidebar. Clicking again should expand.















      ..
          !! processed by numpydoc !!


   .. py:method:: test_collapse_sidebar_button_not_in_mobile(sphinx_build_factory, page, url_base)

      
      Collapse button should not appear in mobile sidebar.
















      ..
          !! processed by numpydoc !!


   .. py:method:: test_no_collapse_sidebar_button(sphinx_build_factory, page, url_base)

      
      No sidebar -> no collapse button.
















      ..
          !! processed by numpydoc !!


   .. py:attribute:: site_name
      :value: 'sidebars'



.. py:function:: _build_test_site(site_name, sphinx_build_factory)

   
   Helper function for building simple test sites (with no `confoverrides`).
















   ..
       !! processed by numpydoc !!

.. py:function:: _check_test_site(site_name, site_path, test_func)

   
   Make the built test site available to Playwright, then run `test_func` on it.
















   ..
       !! processed by numpydoc !!

.. py:function:: _is_overflowing(element)

   
   Check if an element is being shortened via CSS due to text-overflow property.

   We can't check the rendered text because we can't easily get that; all we can get
   is the text as it exists in the DOM (prior to its truncation/elision). Thus we must
   directly compare the rendered clientWidth to the scrollWidth required to display the
   text.















   ..
       !! processed by numpydoc !!

.. py:function:: test_article_toc_syncing(sphinx_build_factory, page, url_base)

   
   Test that the secondary sidebar TOC highlights the correct entry.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_breadcrumb_expansion(sphinx_build_factory, page, url_base)

   
   Test breadcrumb text-overflow.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_breadcrumbs_everywhere(sphinx_build_factory, page, url_base)

   
   Test breadcrumbs truncate properly when placed in various parts of the layout.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_colors(sphinx_build_factory, page, url_base)

   
   Test that things get colored the way we expect them to.

   Note: this is not comprehensive! Please feel free to add to this test by editing
   `../sites/colors/index.rst` and adding more `expect` statements below.















   ..
       !! processed by numpydoc !!

.. py:function:: test_version_switcher_highlighting(sphinx_build_factory, page, url_base)

   
   In sidebar and topbar - version switcher should apply highlight color to currently
   selected version.
















   ..
       !! processed by numpydoc !!

.. py:data:: UnsupportedOperation

.. py:data:: playwright

.. py:data:: repo_path

.. py:data:: test_sites_dir

