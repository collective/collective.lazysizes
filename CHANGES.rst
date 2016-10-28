Changelog
=========

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
