Changelog
=========

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
