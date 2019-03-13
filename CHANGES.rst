Changelog
=========

4.1.6 (2019-03-12)
------------------

- Update lazysizes to v4.1.6.
  [hvelarde]

- Add support for Plone 5.2 and Python 3.
  [hvelarde]

- Drop explicit support for Plone 5.0.
  [hvelarde]

- Code clean up.
  [hvelarde]


4.1.4 (2018-10-11)
------------------

- Upgrade lazysizes to v4.1.4.
  [hvelarde]

- Set webpack ``output.libraryTarget`` to ``var`` and do not import the UMD version of lazysizes to avoid ``Mismatched anonymous define() module`` error in Plone 5 (refs. `#67 <https://github.com/collective/collective.lazysizes/issues/67>`_).
  [thet, rodfersou]

- Update Brazilian Portuguese and Spanish translations.
  [hvelarde]


4.1.2 (2018-10-01)
------------------

- Set webpack ``output.libraryExport`` to ``default`` to avoid ``Mismatched anonymous define() module`` error (fixes `#67 <https://github.com/collective/collective.lazysizes/issues/67>`_).
  [rodfersou, hvelarde]

- Upgrade lazysizes to v4.1.2.
  [thet]

- Add browser layer to ``collective.lazysizes.resources`` viewlet registration;
  this avoids showing the viewlet when the package is not yet installed (fixes `#69 <https://github.com/collective/collective.lazysizes/issues/69>`_).
  [erral]


4.1.1.1 (2018-09-10)
--------------------

- Avoid ``ImportError`` while running upgrade step v10 (fixes `#63 <https://github.com/collective/collective.lazysizes/issues/63>`_).
  [hvelarde]


4.1.1 (2018-09-06)
------------------

- Deprecate resource registries;
  instead, we now use a viewlet in ``plone.htmlhead`` to load JavaScript code.
  This simplifies maintainance of the add-on among multiple Plone versions.
  [hvelarde]

- Upgrade lazysizes to v4.1.1.
  [hvelarde]

- Add lazysizes print plugin;
  this plugin will automatically unveil all elements as soon as a print is detected even if the given lazyload image isn't in the viewport (fixes `#50 <https://github.com/collective/collective.lazysizes/issues/50>`_).
  [thet, hvelarde]

- Remove unused ``collective.lazysizes.ImageScales`` vocabulary.
  [hvelarde]

- Process static resources using webpack.
  [rodfersou]

- Avoid ``ValueError`` when upgrading from profile version 3 (fixes `#46 <https://github.com/collective/collective.lazysizes/issues/46>`_).
  [hvelarde]


4.0.1 (2017-11-20)
------------------

- Upgrade lazysizes to v4.0.1. Twitter plugin is now CommonJS compatible.
  [hvelarde]

- Require plone.app.registry >=1.5. Refs #42
  [erral]


3.1 (2017-10-02)
----------------

- Add German translations.
  [thet]

- Add explicit i18n message ids instead of implicit based on the translation string.
  [thet]

- Fix Plone 5 compatibility.
  [thet]

- Extend the ``uninstall`` profile with more de-registrations.
  [thet]

- Fix the blacklist XPath selector to also match elements with the class directly set on it.
  [thet]

- Add configlet option to enable lazy loading for authenticated users.
  [hvelarde]

- Avoid possible overriding of ``css_class_blacklist`` while upgrading.
  [hvelarde]

- Avoid possible ``ConfigurationConflictError`` on upgrade step registration.
  [hvelarde]


3.0.0 (2017-03-09)
------------------

- Update lazySizes to v3.0.0.
  [hvelarde]

- Remove respimg polyfill plugin.
  [hvelarde]

- Fix ``UnicodeEncodeError`` on logger.
  [hvelarde]


2.0.5rc1 (2016-10-28)
---------------------

- Clean up configlet;
  the ``image_candidates`` field was removed as the intended functionality will be included in Plone's core in the near future (see `PLIP 1483 <https://github.com/plone/Products.CMFPlone/issues/1483>`_).
  [hvelarde]

- Remove dependency on five.grok.
  [hvelarde]

- Update lazysizes to v2.0.5.
  [hvelarde]

- Pin version of Products.ResourceRegistries >=2.2.12 to fix upgrade step.
  [rodfersou, hvelarde]


2.0.0b1 (2016-08-11)
--------------------

- lazysizes was upgraded to version 2.0.0 and we are using now the AMD module (closes `#20`_).
  [rodfersou]

- Do not raise an exception in case Twitter's embed code was somehow modified (closes `#17`_).
  [hvelarde]


1.5.0b1 (2016-05-25)
--------------------

- Embedded tweets are now also lazy loaded (closes `#15`_).
  [aFarkas, rodfersou, hvelarde]

- Package is now compatible with Plone 5.0 and Plone 5.1.
  [hvelarde]


1.5.0a1 (2016-04-07)
--------------------

- Use data URI scheme for image placeholder to save one additional request (closes `#8`_).
  [hvelarde]

- Brazilian Portuguese and Spanish translations were added.
  [hvelarde]

- Deal better with <img> tags with no `src` attribute;
  log an error message with the request URL (closes `#11`_).
  [hvelarde]

- Package is now compatible with Plone 5.
  [hvelarde]

- Remove dependency on Products.CMFQuickInstallerTool.
  [hvelarde]

- Update lazysizes and respimg polyfill extension to v1.5.0.
  [hvelarde]


1.4.0a1 (2016-02-23)
--------------------

- Add option to list class identifiers that will not be processed for lazy loading.
  `<img>` and `<iframe>` elements with that class directly applied to them, or to a parent element, will be skiped (closes `#5`_).
  [rodfersou, hvelarde]

- Update lazysizes and respimg polyfill extension to v1.4.0.
  [hvelarde]

- Use a blank image instead of a spinner as placeholder.
  [hvelarde]

- Logging now uses `debug` level instead of `info`.
  [hvelarde]


1.0a1 (2016-01-05)
------------------

- Initial release.

.. _`#5`: https://github.com/collective/collective.lazysizes/issues/5
.. _`#8`: https://github.com/collective/collective.lazysizes/issues/8
.. _`#11`: https://github.com/collective/collective.lazysizes/issues/11
.. _`#15`: https://github.com/collective/collective.lazysizes/issues/15
.. _`#17`: https://github.com/collective/collective.lazysizes/issues/17
.. _`#20`: https://github.com/collective/collective.lazysizes/issues/20
