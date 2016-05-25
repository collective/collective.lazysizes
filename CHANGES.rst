Changelog
=========

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
