tests.test_build
================

.. py:module:: tests.test_build

.. autoapi-nested-parse::

   All the tests performed in the pydata-sphinx-theme test suite.

   ..
       !! processed by numpydoc !!


Attributes
----------

.. autoapisummary::

   tests.test_build.COMMON_CONF_OVERRIDES
   tests.test_build.all_edits
   tests.test_build.bad_custom
   tests.test_build.bad_edits
   tests.test_build.good_custom
   tests.test_build.good_custom_with_provider
   tests.test_build.good_edits
   tests.test_build.providers
   tests.test_build.slash_edits
   tests.test_build.switcher_files


Functions
---------

.. autoapisummary::

   tests.test_build.test_analytics
   tests.test_build.test_build_html
   tests.test_build.test_deprecated_build_html
   tests.test_build.test_dont_shorten_link
   tests.test_build.test_edit_page_url
   tests.test_build.test_empty_templates
   tests.test_build.test_footer
   tests.test_build.test_icon_links
   tests.test_build.test_included_toc
   tests.test_build.test_local_announcement_banner
   tests.test_build.test_logo_alt_text
   tests.test_build.test_logo_basic
   tests.test_build.test_logo_external_image
   tests.test_build.test_logo_external_link
   tests.test_build.test_logo_missing_image
   tests.test_build.test_logo_no_image
   tests.test_build.test_logo_template_rejected
   tests.test_build.test_logo_two_images
   tests.test_build.test_math_header_item
   tests.test_build.test_navbar_align
   tests.test_build.test_navbar_header_dropdown
   tests.test_build.test_navbar_header_dropdown_button
   tests.test_build.test_navbar_no_in_page_headers
   tests.test_build.test_plausible
   tests.test_build.test_primary_logo_is_dark_when_default_mode_is_dark
   tests.test_build.test_primary_logo_is_light_when_default_mode_is_light
   tests.test_build.test_primary_logo_is_light_when_default_mode_is_set_to_auto
   tests.test_build.test_primary_logo_is_light_when_no_default_mode
   tests.test_build.test_pygments_fallbacks
   tests.test_build.test_remote_announcement_banner
   tests.test_build.test_render_secondary_sidebar_dict
   tests.test_build.test_render_secondary_sidebar_dict_glob_subdir
   tests.test_build.test_render_secondary_sidebar_dict_multiple_glob_matches
   tests.test_build.test_render_secondary_sidebar_list
   tests.test_build.test_role_main_for_search_highlights
   tests.test_build.test_shorten_link
   tests.test_build.test_show_nav_level
   tests.test_build.test_sidebar_secondary_templates_all_empty
   tests.test_build.test_sidebars_captions
   tests.test_build.test_sidebars_level2
   tests.test_build.test_sidebars_nested_page
   tests.test_build.test_sidebars_show_nav_level0
   tests.test_build.test_sticky_header
   tests.test_build.test_theme_switcher
   tests.test_build.test_toc_visibility
   tests.test_build.test_translations
   tests.test_build.test_version_switcher_error_states


Module Contents
---------------

.. py:function:: test_analytics(sphinx_build_factory, provider, tags)

   
   Check the Google analytics.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_build_html(sphinx_build_factory, file_regression)

   
   Test building the base html template and config.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_deprecated_build_html(sphinx_build_factory, file_regression)

   
   Test building the base html template with all the deprecated configs.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_dont_shorten_link(sphinx_build_factory, file_regression)

   
   Regression test for setting shorten_urls to false .
















   ..
       !! processed by numpydoc !!

.. py:function:: test_edit_page_url(sphinx_build_factory, html_context, edit_text_and_url)

   
   Test the edit this page generated link.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_empty_templates(sphinx_build_factory)

   
   If a template is empty (e.g., via a config), it should be removed.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_footer(sphinx_build_factory)

   
   Test for expected footer contents.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_icon_links(sphinx_build_factory, file_regression)

   
   Test that setting icon links are rendered in the documentation.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_included_toc(sphinx_build_factory)

   
   Test that Sphinx project containing TOC (.. toctree::) included via .. include::
   can be successfully built.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_local_announcement_banner(sphinx_build_factory)

   
   If announcement is not a URL, it should be rendered at build time.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_logo_alt_text(sphinx_build_factory, confoverrides, expected_alt_text)

   
   Test our alt-text fallback mechanism.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_logo_basic(sphinx_build_factory)

   
   Test that the logo is shown by default, project title if no logo.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_logo_external_image(sphinx_build_factory)

   
   Test that the logo link is correct for external URLs.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_logo_external_link(sphinx_build_factory)

   
   Test that the logo link is correct for external URLs.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_logo_missing_image(sphinx_build_factory)

   
   Test that a missing image will raise a warning.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_logo_no_image(sphinx_build_factory)

   
   Test that the text is shown if no image specified.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_logo_template_rejected(sphinx_build_factory)

   
   Test that dynamic Sphinx templates are not accepted as logo files.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_logo_two_images(sphinx_build_factory)

   
   Test that the logo image / text is correct when both dark / light given.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_math_header_item(sphinx_build_factory, file_regression)

   
   Regression test for math items in a header title.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_navbar_align(align, klass, sphinx_build_factory)

   
   The navbar items align with the proper part of the page.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_navbar_header_dropdown(sphinx_build_factory, n_links)

   
   Test whether dropdown appears based on number of header links + config.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_navbar_header_dropdown_button(sphinx_build_factory, dropdown_text)

   
   Test whether dropdown button text is configurable.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_navbar_no_in_page_headers(sphinx_build_factory, file_regression)

   
   Test navbar elements did not change (regression test).
















   ..
       !! processed by numpydoc !!

.. py:function:: test_plausible(sphinx_build_factory)

   
   Test the Plausible analytics.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_primary_logo_is_dark_when_default_mode_is_dark(sphinx_build_factory)

   
   Test that the primary logo image is dark when default mode is set to dark.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_primary_logo_is_light_when_default_mode_is_light(sphinx_build_factory)

   
   Test that the primary logo image is light when default mode is set to light.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_primary_logo_is_light_when_default_mode_is_set_to_auto(sphinx_build_factory)

   
   Test that the primary logo image is light when default is set to auto.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_primary_logo_is_light_when_no_default_mode(sphinx_build_factory)

   
   Test that the primary logo image is light when no default mode is set.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_pygments_fallbacks(sphinx_build_factory, style_names, keyword_colors)

   
   Test that setting color themes works.

   NOTE: the expected keyword colors for fake_foo and fake_bar are the colors
   from the fallback styles (tango and monokai, respectively).















   ..
       !! processed by numpydoc !!

.. py:function:: test_remote_announcement_banner(sphinx_build_factory)

   
   If announcement is a URL, it should not be rendered at build time.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_render_secondary_sidebar_dict(sphinx_build_factory)

   
   Test that the secondary sidebar can be built with a dict of templates.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_render_secondary_sidebar_dict_glob_subdir(sphinx_build_factory)

   
   Test that the secondary sidebar can be built with a dict of templates that globs a
   subdir.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_render_secondary_sidebar_dict_multiple_glob_matches(sphinx_build_factory)

   
   Test that the secondary sidebar builds with a template dict with two conflicting
   globs.

   The last specified glob pattern should win, but a warning should be emitted with the
   offending pattern and affected pagenames.















   ..
       !! processed by numpydoc !!

.. py:function:: test_render_secondary_sidebar_list(sphinx_build_factory)

   
   Test that the secondary sidebar can be built with a list of templates.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_role_main_for_search_highlights(sphinx_build_factory)

   
   Sphinx searchtools.js looks for [role="main"], so make sure it's there.

   This is a regression test. See #1676.















   ..
       !! processed by numpydoc !!

.. py:function:: test_shorten_link(sphinx_build_factory, file_regression)

   
   Regression test for "edit on <provider>" link shortening.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_show_nav_level(sphinx_build_factory)

   
   The navbar items align with the proper part of the page.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_sidebar_secondary_templates_all_empty(sphinx_build_factory)

   
   Test that the secondary sidebar is removed if all templates are empty.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_sidebars_captions(sphinx_build_factory, file_regression)

   
   Test that the captions are rendered.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_sidebars_level2(sphinx_build_factory, file_regression)

   
   Test sidebars in a second-level page w/ children.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_sidebars_nested_page(sphinx_build_factory, file_regression)

   
   Test that nested pages are shown in the sidebar.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_sidebars_show_nav_level0(sphinx_build_factory)

   
   Regression test for show_nav_level:0 when the toc is divided into parts.

   Testing both home page and a subsection page for correct elements.















   ..
       !! processed by numpydoc !!

.. py:function:: test_sticky_header(sphinx_build_factory)

   
   Regression test, see #1630. Sticky header should be direct descendant of body.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_theme_switcher(sphinx_build_factory, file_regression)

   
   Regression test for the theme switcher button.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_toc_visibility(sphinx_build_factory)

   
   Test that setting TOC level visibility works as expected.
















   ..
       !! processed by numpydoc !!

.. py:function:: test_translations(sphinx_build_factory)

   
   Test that basic translation functionality works.

   This will build our test site with the French language, and test
   that a few phrases are in French.

   We use this test to catch regressions if we change wording without
   changing the translation files.















   ..
       !! processed by numpydoc !!

.. py:function:: test_version_switcher_error_states(sphinx_build_factory, file_regression, url)

   
   Regression test the version switcher dropdown HTML.

   Note that a lot of the switcher HTML gets populated by JavaScript,
   so we will not test the final behavior. This just tests for the basic
   structure.

   TODO: Find a way to test Javascript's behavior in populating the HTML.















   ..
       !! processed by numpydoc !!

.. py:data:: COMMON_CONF_OVERRIDES

.. py:data:: all_edits

.. py:data:: bad_custom

.. py:data:: bad_edits

.. py:data:: good_custom

.. py:data:: good_custom_with_provider

.. py:data:: good_edits

.. py:data:: providers

.. py:data:: slash_edits

.. py:data:: switcher_files
   :value: ['switcher.json', 'http://a.b/switcher.json', 'missing_url.json']


