conf
====

.. py:module:: conf

.. autoapi-nested-parse::

   Configuration file for the Sphinx documentation builder.

   This file only contains a selection of the most common options. For a full
   list see the documentation:
   https://www.sphinx-doc.org/en/master/usage/configuration.html

   ..
       !! processed by numpydoc !!


Attributes
----------

.. autoapisummary::

   conf.author
   conf.autoapi_dirs
   conf.autoapi_keep_files
   conf.autoapi_member_order
   conf.autoapi_root
   conf.autoapi_type
   conf.autodoc_member_order
   conf.autodoc_typehints
   conf.autosummary_generate
   conf.bad_classes
   conf.blog_authors
   conf.blog_path
   conf.copybutton_exclude
   conf.copybutton_selector
   conf.copyright
   conf.exclude_patterns
   conf.extensions
   conf.favicons
   conf.graphviz_output_format
   conf.html_baseurl
   conf.html_context
   conf.html_css_files
   conf.html_favicon
   conf.html_js_files
   conf.html_last_updated_fmt
   conf.html_logo
   conf.html_sidebars
   conf.html_sourcelink_suffix
   conf.html_static_path
   conf.html_theme
   conf.html_theme_options
   conf.inheritance_graph_attrs
   conf.intersphinx_mapping
   conf.json_url
   conf.jupyterlite_config
   conf.language
   conf.linkcheck_allowed_redirects
   conf.linkcheck_anchors_ignore
   conf.linkcheck_ignore
   conf.linkcheck_report_timeouts_as_broken
   conf.linkcheck_retries
   conf.linkcheck_timeout
   conf.myst_enable_extensions
   conf.myst_heading_anchors
   conf.myst_substitutions
   conf.nitpick_ignore_regex
   conf.nitpicky
   conf.project
   conf.rediraffe_redirects
   conf.release
   conf.templates_path
   conf.todo_include_todos
   conf.togglebutton_hint
   conf.togglebutton_hint_hide
   conf.version_match
   conf.version_match


Functions
---------

.. autoapisummary::

   conf.setup
   conf.setup_to_main


Module Contents
---------------

.. py:function:: setup(app)

   
   Add custom configuration to sphinx app.

   :param app: the Sphinx application

   :returns: the 2 parallel parameters set to ``True``.















   ..
       !! processed by numpydoc !!

.. py:function:: setup_to_main(app, pagename, templatename, context, doctree)

   
   Add a function that jinja can access for returning an "edit this page" link
   pointing to `main`.
















   ..
       !! processed by numpydoc !!

.. py:data:: author
   :value: 'PyData Community'


.. py:data:: autoapi_dirs
   :value: ['../src/pydata_sphinx_theme']


.. py:data:: autoapi_keep_files
   :value: True


.. py:data:: autoapi_member_order
   :value: 'groupwise'


.. py:data:: autoapi_root
   :value: 'api'


.. py:data:: autoapi_type
   :value: 'python'


.. py:data:: autodoc_member_order
   :value: 'groupwise'


.. py:data:: autodoc_typehints
   :value: 'description'


.. py:data:: autosummary_generate
   :value: True


.. py:data:: bad_classes
   :value: ('.*abc def.*', 'api_sample\\.RandomNumberGenerator', 'bs4\\.BeautifulSoup',...


.. py:data:: blog_authors

.. py:data:: blog_path
   :value: 'examples/blog/index'


.. py:data:: copybutton_exclude
   :value: '.linenos, .gp'


.. py:data:: copybutton_selector
   :value: ':not(.prompt) > div.highlight pre'


.. py:data:: copyright
   :value: '2019, PyData Community'


.. py:data:: exclude_patterns
   :value: ['_build', 'Thumbs.db', '.DS_Store', '**.ipynb_checkpoints']


.. py:data:: extensions
   :value: ['sphinx.ext.napoleon', 'sphinx.ext.autodoc', 'sphinx.ext.autosummary', 'sphinx.ext.todo',...


.. py:data:: favicons

.. py:data:: graphviz_output_format
   :value: 'svg'


.. py:data:: html_baseurl

.. py:data:: html_context

.. py:data:: html_css_files
   :value: ['custom.css']


.. py:data:: html_favicon
   :value: '_static/logo.svg'


.. py:data:: html_js_files

.. py:data:: html_last_updated_fmt
   :value: ''


.. py:data:: html_logo
   :value: '_static/logo.svg'


.. py:data:: html_sidebars

.. py:data:: html_sourcelink_suffix
   :value: ''


.. py:data:: html_static_path
   :value: ['_static']


.. py:data:: html_theme
   :value: 'pydata_sphinx_theme'


.. py:data:: html_theme_options

.. py:data:: inheritance_graph_attrs

.. py:data:: intersphinx_mapping

.. py:data:: json_url
   :value: 'https://pydata-sphinx-theme.readthedocs.io/en/latest/_static/switcher.json'


.. py:data:: jupyterlite_config
   :value: 'jupyterlite_config.json'


.. py:data:: language
   :value: 'en'


.. py:data:: linkcheck_allowed_redirects

.. py:data:: linkcheck_anchors_ignore
   :value: ['\\/.*']


.. py:data:: linkcheck_ignore
   :value: ['https://github.com.+?#.*', 'https://www.sphinx-doc.org/en/master/*/.+?#.+?',...


.. py:data:: linkcheck_report_timeouts_as_broken
   :value: True


.. py:data:: linkcheck_retries
   :value: 1


.. py:data:: linkcheck_timeout
   :value: 5


.. py:data:: myst_enable_extensions
   :value: ['colon_fence', 'linkify', 'substitution']


.. py:data:: myst_heading_anchors
   :value: 2


.. py:data:: myst_substitutions

.. py:data:: nitpick_ignore_regex

.. py:data:: nitpicky
   :value: True


.. py:data:: project
   :value: 'PyData Theme'


.. py:data:: rediraffe_redirects

.. py:data:: release
   :value: '0.16.1'


.. py:data:: templates_path
   :value: ['_templates']


.. py:data:: todo_include_todos
   :value: True


.. py:data:: togglebutton_hint
   :value: ''


.. py:data:: togglebutton_hint_hide
   :value: ''


.. py:data:: version_match

.. py:data:: version_match
   :value: 'dev'


